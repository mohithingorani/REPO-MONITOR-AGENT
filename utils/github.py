import requests
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage, HumanMessage
from pydantic_types import isIssue, ImportantFilesOutput, MessageState
from langchain_core.tools import tool
GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json"
}
from langchain.messages import ToolMessage
from pydantic_types import ImportantFilesOutput, MessageState
import re

from model import llm

def get_repo_files(state: MessageState) -> MessageState:
    # Normalize MessageState → dict
    if not isinstance(state, dict):
        state = dict(state)

    owner = state["owner"]
    repo = state["repo"]
    path = state.get("path", "")

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    items = response.json()
    files = state.get("files", [])

    for item in items:
        if item["type"] == "file":
            files.append(item["path"])
        elif item["type"] == "dir":
            new_state = {
                **state,
                "path": item["path"],
                "files": files,
            }
            child_state = get_repo_files(MessageState(**new_state))
            files.extend(child_state.files)

    response = {
        **state,
        "files": files,
        "path": "", 
        "messages": [ToolMessage(content=f"Fetched {len(files)} files from repo", tool_call_id="get_repo_files")]
    }
    final_state = MessageState(**response)
    return final_state





# Get Content for for important files
@tool
def get_file_content(owner: str, repo: str, file_path: str) -> str:
    """
    Docstring for get_file_content
    
    :param owner: Description
    :type owner: str
    :param repo: Description
    :type repo: str
    :param file_path: Description
    :type file_path: str
    :return: Description
    :rtype: str
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    file_info = response.json()
    if 'content' in file_info:
        import base64
        content = base64.b64decode(file_info['content']).decode('utf-8')
        return content
    return ""


def is_issue_in_file(content:str,file_name:str) -> isIssue:
    """Analyze the content of a file to determine if it describes an issue."""
    llm_with_structured_output = llm.with_structured_output(isIssue)
    response = llm_with_structured_output.invoke([
        SystemMessage(content="You analyze the content of a file and determine if it is an issue or not.Consider even a suggestion as issue in that specific file.Give name of the file in issue_description."),
        HumanMessage(content=f"Here is the content of the file:\n{content}\nBased on this content, is there an issue described in the file? If so, provide a brief description of the issue. If not, indicate that it is not an issue.")
    ])
    return response




def get_important_files(state: MessageState)->MessageState:
    files = state.files
    llm_with_structured_output:ImportantFilesOutput = llm.with_structured_output(ImportantFilesOutput)
    system_message = SystemMessage(
        content=(
            "You analyze a GitHub repository and identify files that are important for understanding the project. "
            "Include core source files (e.g. .py, .js, .ts, .java) and key documentation (README, docs). "
            "Exclude config files, environment files, editor settings, dependencies, build artifacts, and "
            "non-essential utilities or helper components. Give at most 10 important files. If the repository has fewer than 10 files, return all of them"
        )
    )
    human_message = HumanMessage(content=f"Here is a list of files in the repository: {files}. Please identify the important files from this list.")
    response = llm_with_structured_output.invoke([system_message, human_message])
    # testing with small files
    important = response.important_files
    return MessageState(
        owner=state.owner,
        repo=state.repo,
        llm_calls=state.llm_calls+1,
        files=important,
        messages=[ToolMessage(content=f"Identified {len(important)} important files from the repo", tool_call_id="get_important_files")],
        path="",
        curr_index=state.curr_index
    )
    


def parse_repo(state:dict):
    text="https://github.com/mohithingorani/RAG-CHAIN-FOR-AI-ARTICLE"
    text = state.messages[0].content
    match = re.search(r"https?://github\.com/[^\s]+", text)
    if not match:
        return None

    url = match.group(0).rstrip("/")

    clean = re.sub(r"^https?://github\.com/", "", url)
    parts = clean.split("/")

    return {
        "owner": parts[0] if len(parts) > 0 else None,
        "repo": parts[1] if len(parts) > 1 else None,
        "llm_calls":0,
        "files":[],
        "messages":[],
        "path":"",
        "curr_index":0
    }
