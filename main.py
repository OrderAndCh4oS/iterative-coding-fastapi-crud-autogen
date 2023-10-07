import autogen
import os

# from autogen import GroupChat, GroupChatManager

seed = 666
working_dir = f'out_{seed}'
master_plan_file = 'master-plan.txt'
main_script_file = 'main.py'
n_code_iterations = 10

llm_model = 'gpt-3.5-turbo-0613'
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
        directory += f'/v{version}'
    os.makedirs(directory, exist_ok=True)


create_directories_if_not_exist()


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading file.")


def write_file(txt, name):
    with open(f'{working_dir}/{name}', "w") as plan_file:
        plan_file.write(txt)


# initial_prompt = """We're building a RESTful API for managing customer data.
# We will handle POST and GET requests to /customer and GET, PUT, DELETE /customer/:uuid requests.
# Customers will have uuid, email, username, createdAt, updatedAt fields.
# We will write all of the tests for each endpoint before we write the handlers.
# We must test the body response data before we test http status codes in unit tests, this is vitally important.
# We will run tests the tests individually as we go to prove the api works as expected.
# We must prove the api endpoint works by running our unittest testing suite.
# We will use Fastapi, unittest and uuidv7 time-ordered UUID.
# We will update an in-memory db on create, update and delete requests.
# We must never run the server directly, this is very important.
# We must make sure the fastapi app has all of the routes defined correctly.
# We must not create a venv or any other virtual environment.
# Start by planning the application step by step, then implement each step."""

initial_prompt = """We're building a RESTful API for managing customer data. 
We will handle POST and GET requests to /customer and GET, PUT, DELETE /customer/:uuid requests.
Customers will have uuid, email, username, createdAt, updatedAt fields.
We will write all of the tests for each endpoint before we write the handlers.
We must test the body response data before we test http status codes in unit tests, this is vitally important.
We will run tests the tests individually as we go to prove the api works as expected.
We must prove the api endpoint works by running our unittest testing suite. 
We will use Fastapi, unittest and uuidv7 time-ordered UUID. 
We will update an in-memory db on create, update and delete requests.
We must never run the server directly, this is very important. 
We must make sure the fastapi app has all of the routes defined correctly.
We must not create a venv or any other virtual environment.
Start by planning the application step by step, then implement each step."""

write_file(initial_prompt, 'initial-prompt.txt')


dev_consultant = autogen.AssistantAgent(
    name="dev_consultant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant. You suggest coding and reasoning steps for another AI assistant to accomplish a task. Do not suggest concrete code. For any action beyond writing code or reasoning, convert it to a step which can be implemented by writing code. For example, the action of browsing the web can be implemented by writing code which reads and prints the content of a web page. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If the execution is wrong, analyze the error and suggest a fix. Never run a server for any tasks, either run code directly or run the tests.",
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
        ],
    },
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": working_dir},
    function_map={"ask_dev_consultant": ask_dev_consultant},
)

# user_proxy.initiate_chat(
#     assistant,
#     message=initial_prompt
# )

# TODO: review the final code by providing agents with the project structure and
#       a way to inspect any file they want to read.

def get_files_in_directory(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        if root != working_dir:
            continue
        for file in files:
            file_list.append(file)
    return file_list


def open_file(filename):
    try:
        with open(f'{working_dir}/{filename}', 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "File not found."
    except IOError:
        return "Error reading file."


def write_todos(message):
    write_file(message, 'todos.txt')


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

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": working_dir},
    function_map={"open_file": open_file, "write_todos": write_todos},
)

project_structure = get_files_in_directory(working_dir)

user_proxy.initiate_chat(
    quality_assurance,
    message=f"""The dev team had the following task

{initial_prompt}

This is the project structure

{project_structure}

You task is to open these files and inspect the quality of the dev teams work.
Open all the files to read and adjudicate them.
Make a todo list of any outstanding work the dev team may be required to complete to accomplish the task.
Be sure to include the names of the files that need to be edited to accomplish any given todo.
"""
)


