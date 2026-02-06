from langchain.messages import ToolMessage
import requests
from models.state import MessageState
from tools.github import GITHUB_API
from config.github import HEADERS

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

