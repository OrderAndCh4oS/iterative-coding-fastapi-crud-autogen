from random import randint

import autogen
import os


def main(seed=42):
    working_dir = f"out_{seed}"
    config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    llm_config = {"config_list": config_list, "seed": seed}
    model = "gpt-3.5-turbo-0613"

    def create_directories_if_not_exist(version=None):
        directory = working_dir
        if version and version > 0:
            directory += f"/v{version}"
        os.makedirs(directory, exist_ok=True)

    create_directories_if_not_exist()

    def read_file(file_path):
        try:
            with open(f"{working_dir}/{file_path}", "r") as file:
                contents = file.read()
            return contents
        except FileNotFoundError:
            print("File not found.")
        except IOError:
            print("Error reading file.")

    def write_file(txt, name):
        with open(f"{working_dir}/{name}", "w") as plan_file:
            plan_file.write(txt)

    def delete_file(name):
        if os.path.exists(name):
            try:
                os.remove(name)
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}.")

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
        ignored_files = {"todo.txt", "initial_prompt.txt"}
        for root, dirs, files in os.walk(directory):
            if ".pytest_cache" in root or "__pycache__" in root:
                continue
            for file in files:
                if file in ignored_files:
                    continue
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, directory)
                file_list.append(relative_path)
        return file_list

    def get_project_structure():
        return get_files_in_directory(working_dir)

    def write_todos(message):
        write_file(message, "todos.txt")

    api_spec = """Write A RESTful API for managing product data:
It will use Fastapi for the app, Pydantic for validation and unittest for testing.
It will have an in-memory db with wrapper functions to query the database.
It will have a Products table with uuid (string), name, description, createdAt, updatedAt columns.
Each product must have getDetail, getList, createOne, updateOne, deleteOne request handlers.
It must define each products request handlers, unit tests and data models etc. in separate files. eg product_handlers.py, product_tests.py, product_models.py.
It will use separate Pydantic classes for the stored products, any requests and responses. For example Product, CreateProductRequest, UpdateProductRequest, ProductResponse."""
    assistant_rules = f"""You must test the body response data as a dict with assertDictEqual, this will make it easier to debug errors.
You must test response data before testing the http response codes in unit tests, as status code errors do not provide useful debugging information in tests. 
You must only use the unittest testing suite to prove the api endpoints work correctly. 
You must never run the server and do not install uvicorn, wsgi or anything else like that, this is very important. 
You must not create a venv or any other virtual environment.
Work with the dev consultant to plan this project step by step and implement the steps."""
    write_file(api_spec, "initial_prompt.txt")
    dev_consultant = autogen.AssistantAgent(
        name="dev_consultant",
        llm_config=llm_config,
        system_message="You are a helpful AI assistant. You suggest coding and reasoning steps for another AI assistant to accomplish a task. Do not suggest concrete code. For any action beyond writing code or reasoning, convert it to a step which can be implemented by writing code. For example, the action of browsing the web can be implemented by writing code which reads and prints the content of a web page. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If the execution is wrong, analyze the error and suggest a fix. It is very important that we never run a server for any tasks. Never suggest installing uvicorn or wsgi for example",
    )

    def ask_dev_consultant(message):
        dev_user.initiate_chat(dev_consultant, message=message)
        return dev_user.last_message()["content"]

    assistant = autogen.AssistantAgent(
        name="assistant",
        code_execution_config={},
        system_message=f"{autogen.AssistantAgent.DEFAULT_SYSTEM_MESSAGE}\n\n{assistant_rules}",
        llm_config={
            "temperature": 0,
            "request_timeout": 600,
            "seed": seed,
            "model": model,
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

    dev_user = autogen.UserProxyAgent(
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

    quality_assurance = autogen.AssistantAgent(
        name="quality_assurance",
        code_execution_config={},
        llm_config={
            "temperature": 0,
            "request_timeout": 600,
            "seed": seed,
            "model": model,
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
    qa_user = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        code_execution_config={"work_dir": working_dir},
        system_message="""Your task is to inspect the project structure to determine what has already been implemented and what work is still outstanding.
Open the files to inspect the scope and quality of the dev teams work.
You must run all test files to make sure the existing code is working as expected.
Make a todo list of any work that the dev team needs complete to accomplish the task or will improve the quality of the codebase.
If any todos relate to existing files, be sure to include the names of the files that need to be edited to accomplish the task.
Do not request work that's already been completed.
You're not obligated to find fault, if everything is up to spec respond with TERMINATE""",
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
        if len(project_structure) == 0:
            dev_user.initiate_chat(assistant, message=api_spec)
    except:
        pass

    try:
        qa_user.initiate_chat(
            quality_assurance,
            message=f"""The dev team has been tasked with implementing the following project spec:

{api_spec}

inspect the project structure, read the files and run any tests to determine what the remaining todos are.""",
        )

        if read_file("todos.txt"):
            dev_user.initiate_chat(
                assistant,
                message=f"""You have been tasked with implementing the following project spec

Project spec:
{read_file("initial_prompt.txt")}

Discuss the project spec and remaining todos with the dev consultant and implement the plan.
You must reject all todo requests that are not aligned with the project spec.
You must run the tests and fix any remaining errors.

Remaining Todos:
{read_file("todos.txt")}""",
            )
        else:
            "No todos.txt has been generated, project complete"
    except:
        pass

    delete_file("todo.txt")


if __name__ == "__main__":
    main(340)
    # main(randint(1, 2048))
