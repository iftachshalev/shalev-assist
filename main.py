# === Imports ===
import os
import json
import subprocess
import sys

import openai
from openai import OpenAI
from duckduckgo_search import DDGS

from config import OPENAI_API_KEY, MODEL_NAME, PLAYGROUND_PATH

from dotenv import load_dotenv
load_dotenv()

# === OpenAI Client Setup ===
client = OpenAI(api_key=OPENAI_API_KEY)


# === Tool Functions ===
def search_web(query: str, max_results: int = 5) -> str:
    """Searches the web using DuckDuckGo and returns a list of formatted results."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region="wt-wt", safesearch="Moderate", max_results=max_results):
            results.append(f"{r['title']}\n{r['href']}\n{r['body']}")
    return "\n\n".join(results)


def read_local_files(path: str) -> str:
    """Reads all readable .txt, .md, .py, .log, .json files from a directory."""
    if not os.path.isdir(path):
        return f"Error: '{path}' is not a valid directory."

    result = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path) and file.endswith(('.txt', '.md', '.py', '.log', '.json')):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    result.append(f"### {file}\n{content}")
            except Exception as e:
                result.append(f"### {file}\n[Error reading file: {e}]")

    return "\n\n".join(result) or "No readable files found in the folder."


def run_python_code(code: str) -> str:
    try:
        local_vars = {}
        global_vars = {}
        exec(code, global_vars, local_vars)
        # Return last expression's value if possible
        if '_result' in local_vars:
            return str(local_vars['_result'])
        else:
            return str(local_vars)
    except Exception as e:
        return f"Error executing code: {e}"


def install_package(package_name: str) -> str:
    """Installs a Python package using pip."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return f"Package `{package_name}` installed successfully."
        return f"Error installing `{package_name}`:\n{result.stderr.strip()}"
    except Exception as e:
        return f"Error during installation: {e}"


def edit_file(file_name: str, content: str) -> str:
    """Replaces the content of a file or creates it in the playground folder."""
    file_path = os.path.join(PLAYGROUND_PATH, file_name)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File `{file_name}` edited successfully."
    except Exception as e:
        return f"Error editing file `{file_name}`: {e}"


def run_shell_commands(commands: str) -> str:
    """Runs a shell command after user permission, in the playground directory."""
    confirm = input(f"⚠️  Permission required to run shell command:\n    `{commands}`\nAllow? (y/n): ").strip().lower()
    if confirm not in {"y", "yes"}:
        return "Command execution cancelled by user."

    try:
        result = subprocess.run(commands, shell=True, cwd=PLAYGROUND_PATH, capture_output=True, text=True)
        output = result.stdout.strip() or result.stderr.strip()
        return output or "Command ran successfully but produced no output."
    except Exception as e:
        return f"Error running command: {e}"

# === Tool Function Definitions ===


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Searches the web for up-to-date information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."},
                    "max_results": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_local_files",
            "description": "Reads all readable text files from a folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The folder path with text files (e.g., './docs')"
                    }
                },
                "required": ["path"],
                "default": {"path": PLAYGROUND_PATH}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_code",
            "description": "Executes a Python code snippet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The Python code to run."}
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "install_package",
            "description": "Installs a Python package using pip.",
            "parameters": {
                "type": "object",
                "properties": {
                    "package_name": {"type": "string", "description": "The package to install."}
                },
                "required": ["package_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edits or creates a file and sets its content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {"type": "string", "description": "File name to create/edit."},
                    "content": {"type": "string", "description": "The content to write into the file."}
                },
                "required": ["file_name", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell_commands",
            "description": "Runs a shell commands for windows after getting user permission.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commands": {
                        "type": "string",
                        "description": "The shell command to run (e.g., 'cd directory' or 'dir')."
                    }
                },
                "required": ["command"]
            }
        }
    }
]

# === Main Chat Loop ===


def main():
    os.makedirs(PLAYGROUND_PATH, exist_ok=True)  # Create playground folder if missing
    print("[MCP Tool Chat] GPT-3.5 with Web Search Tool\nType 'exit' to quit.\n")
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use available tools if needed to answer accurately."}
    ]

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        messages.append({"role": "user", "content": user_input})

        # Step 1: Let GPT decide
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message
        messages.append(msg)

        # Step 2: If tool was called
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"\n🔧 Tool Call: {name} with args {args}")

                # Dispatch tool call
                if name == "search_web":
                    output = search_web(**args)
                elif name == "read_local_files":
                    output = read_local_files(**args)
                elif name == "run_python_code":
                    output = run_python_code(**args)
                elif name == "install_package":
                    output = install_package(**args)
                elif name == "edit_file":
                    output = edit_file(**args)
                elif name == "run_shell_commands":
                    output = run_shell_commands(**args)
                else:
                    output = f"Unknown tool: {name}"

                print(f"\n🔧 Tool Output:\n{output}\n")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": output
                })

            # Step 3: Respond based on tool output
            final = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages
            )
            answer = final.choices[0].message.content
            print(f"\nAssistant:\n{answer}\n")
            messages.append({"role": "assistant", "content": answer})

        else:
            # Direct reply from GPT
            print(f"\nAssistant:\n{msg.content}\n")


if __name__ == "__main__":
    main()
