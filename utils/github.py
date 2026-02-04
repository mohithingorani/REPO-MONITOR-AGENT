from typing import Annotated, List
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage, HumanMessage
GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json"
}
from models import ImportantFilesOutput, IsUssueOutput

# repo example https://github.com/mohithingorani/RAG-CHAIN-FOR-AI-ARTICLE


def get_repo_files(owner: str, repo: str, path: str = "") -> List[str]:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    items = response.json()
    files = []

    for item in items:
        if item["type"] == "file":
            files.append(item["path"])
        elif item["type"] == "dir":
            files.extend(get_repo_files(owner, repo, item["path"]))
    return files





def get_important_files(files: List[str]) -> List[str]:
    llm_with_structured_output = llm.with_structured_output(ImportantFilesOutput)
    system_message = SystemMessage(
        content=(
            "You analyze a GitHub repository and identify files that are important for understanding the project. "
            "Include core source files (e.g. .py, .js, .ts, .java) and key documentation (README, docs). "
            "Exclude config files, environment files, editor settings, dependencies, build artifacts, and "
            "non-essential utilities or helper components."
        )
    )
    human_message = HumanMessage(content=f"Here is a list of files in the repository: {files}. Please identify the important files from this list.")
    response = llm_with_structured_output.invoke([system_message, human_message])
    return response.important_files


# Get Content for for important files
def get_file_content(owner: str, repo: str, file_path: str) -> str:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    file_info = response.json()
    if 'content' in file_info:
        import base64
        content = base64.b64decode(file_info['content']).decode('utf-8')
        return content
    return ""






# get_repo_files("mohithingorani", "RAG-CHAIN-FOR-AI-ARTICLE")
# https://github.com/mohithingorani/Portfolio
# content = get_file_content("mohithingorani", "Portfolio", "README.md")
# https://github.com/mohithingorani/Rç


all_files = get_repo_files("mohithingorani", "RAG-CHAIN-FOR-AI-ARTICLE")
print("All Files:", all_files)
important_files = get_important_files(all_files)
print("Important Files:", important_files)

# content = get_file_content("mohithingorani", "RAG-CHAIN-FOR-AI-ARTICLE", file)


def is_issue_in_file(content:str) -> IsUssueOutput:
    """Analyze the content of a file to determine if it describes an issue."""
    llm_with_structured_output = llm.with_structured_output(IsUssueOutput)
    response = llm_with_structured_output.invoke([
        SystemMessage(content="You analyze the content of a file and determine if it is an issue or not. An issue typically contains a description of a problem, steps to reproduce, expected vs actual behavior, and may include labels or comments."),
        HumanMessage(content=f"Here is the content of the file:\n{content}\nBased on this content, is there an issue described in the file? If so, provide a brief description of the issue. If not, indicate that it is not an issue.")
    ])
    return response