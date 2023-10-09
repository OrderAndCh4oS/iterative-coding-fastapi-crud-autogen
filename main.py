import autogen
import os

seed = 10101
working_dir = f"out_{seed}"
main_script_file = "main.py"
n_code_iterations = 10

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {"config_list": config_list, "seed": seed}
gpt_config = {
    "seed": seed,
    "temperature": 0,
    "config_list": config_list,
    "request_timeout": 120,
}


def create_directories_if_not_exist(version=None):
    directory = working_dir
    if version and version > 0:
        directory += f"/v{version}"
    os.makedirs(directory, exist_ok=True)


create_directories_if_not_exist()


def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading file.")


def write_file(txt, name):
    with open(f"{working_dir}/{name}", "w") as plan_file:
        plan_file.write(txt)


def open_file(filename):
    try:
        with open(f"{working_dir}/{filename}", "r") as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "File not found."
    except IOError:
        return "Error reading file."


def get_files_in_directory(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        if root != working_dir:
            continue
        for file in files:
            file_list.append(file)
    return file_list


def get_project_structure():
    return get_files_in_directory(working_dir)


def write_todos(message):
    write_file(message, "todos.txt")


api_spec = """A RESTful API for managing customer data. 
It will use Fastapi, Pydantic and unittest.
It will update an in-memory db on create, update and delete requests.
It will have a Customers table with uuid (string), email, username, createdAt, updatedAt columns.
It will handle POST and GET requests to /customer and GET, PUT, DELETE /customer/:uuid requests.
It will use separate Pydantic classes for the stored customers, any requests and responses. For example Customer, CreateCustomerRequest, UpdateCustomerRequest, CustomerResponse."""

assistant_rules = f"""You must test the body response data as a dict with assertDictEqual, this will make it easier to debug errors.
You must test response data before testing the http response codes in unit tests, as status code errors do not provide useful debugging information in tests. 
You will run each test individually as we go to prove each endpoint works as expected eg `python tests.py Tests.createEntityTest` or `python tests.py Tests.getEntityTest`.
You must prove the api endpoint works by running the unittest testing suite only. 
You must never run the server and do not install uvicorn, wsgi or anything else like that, this is very important. 
You must not create a venv or any other virtual environment.
Work with the dev consultant to plan this project step by step and implement the steps."""

write_file(api_spec, "initial-prompt.txt")

dev_consultant = autogen.AssistantAgent(
    name="dev_consultant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant. You suggest coding and reasoning steps for another AI assistant to accomplish a task. Do not suggest concrete code. For any action beyond writing code or reasoning, convert it to a step which can be implemented by writing code. For example, the action of browsing the web can be implemented by writing code which reads and prints the content of a web page. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If the execution is wrong, analyze the error and suggest a fix. It is very important that we never run a server for any tasks. Never suggest installing uvicorn or wsgi for example",
)

dev_consultant_user = autogen.UserProxyAgent(
    name="dev_consultant_user",
    max_consecutive_auto_reply=0,  # terminate without auto-reply
    human_input_mode="NEVER",
)


def ask_dev_consultant(message):
    dev_consultant_user.initiate_chat(dev_consultant, message=message)
    return dev_consultant_user.last_message()["content"]


assistant = autogen.AssistantAgent(
    name="assistant",
    code_execution_config={},
    system_message=f"{autogen.AssistantAgent.DEFAULT_SYSTEM_MESSAGE}\n\n{assistant_rules}",
    llm_config={
        "temperature": 0,
        "request_timeout": 600,
        "seed": seed,
        "model": "gpt-3.5-turbo-0613",
        "config_list": config_list,
        "functions": [
            {
                "name": "ask_dev_consultant",
                "description": "ask dev consultant to: 1. get a plan for finishing a task, 2. verify the execution result of the plan and potentially suggest new plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "question to ask dev consultant. Make sure the question include enough context, such as the code and the execution result. The planner does not know the conversation between you and the user, unless you share the conversation with the planner.",
                        },
                    },
                    "required": ["message"],
                },
            },
            {
                "name": "get_project_structure",
                "description": "Inspect the files in the project directory, returns a list of files",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
            {
                "name": "open_file",
                "description": "Inspect an existing file if you need to read the contents for debugging or editing purposes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "The name of the file you want to open",
                        },
                    },
                    "required": ["filename"],
                },
            },
        ],
    },
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
    if x.get("content", "")
    else False,
    code_execution_config={"work_dir": working_dir},
    function_map={
        "ask_dev_consultant": ask_dev_consultant,
        "open_file": open_file,
        "get_project_structure": get_project_structure,
    },
)

# TODO: review the final code by providing agents with the project structure and
#       a way to inspect any file they want to read.

quality_assurance = autogen.AssistantAgent(
    name="quality_assurance",
    code_execution_config={},
    llm_config={
        "temperature": 0,
        "request_timeout": 600,
        "seed": seed,
        "model": "gpt-3.5-turbo-0613",
        "config_list": config_list,
        "functions": [
            {
                "name": "get_project_structure",
                "description": "Inspect the files in the project directory, returns a list of files",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
            {
                "name": "open_file",
                "description": "Read an existing file so that you can determine what else may need to be done",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "The name of the file you want to open",
                        },
                    },
                    "required": ["filename"],
                },
            },
            {
                "name": "write_todos",
                "description": "Saves your final report by writing a todos.txt file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Your final report containing the todos",
                        },
                    },
                    "required": ["message"],
                },
            },
        ],
    },
)

user_proxy_review = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": working_dir},
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
    if x.get("content", "")
    else False,
    function_map={
        "get_project_structure": get_project_structure,
        "open_file": open_file,
        "write_todos": write_todos,
    },
)

project_structure = get_files_in_directory(working_dir)

try:
    user_proxy.initiate_chat(
        assistant, message=read_file(f"{working_dir}/initial-prompt.txt")
    )
except:
    pass

user_proxy_review.initiate_chat(
    quality_assurance,
    message=f"""The dev team had the following task

{api_spec}

You task is to inspect the project structure and open the files to inspect the quality of the dev teams work.
Make a todo list of any outstanding work the dev team may be required to complete to accomplish the task.
You're not obligated to find fault, if everything is up to spec respond TERMINATE
Be sure to include the names of the files that need to be edited to accomplish any given todo.""",
)

user_proxy.initiate_chat(
    assistant,
    message=f"""We have already attempted to implement this project spec:

{read_file(f"{working_dir}/initial-prompt.txt")}

This is the project structure:

{project_structure}

You can open any files you need to, to inspect them.

We've now received feedback from QA and need to review their suggested todos and implement their suggestions where appropriate. 
We can push back if we believe they are mistaken, but we should document the rationale behind rejecting their requests.

{read_file(f"{working_dir}/todos.txt")}

Once there are no todos to address respond TERMINATE
""",
)
