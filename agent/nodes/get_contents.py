from tools.github import get_file_content
from models.state import MessageState

def get_contents_of_file(state:MessageState) -> str:
    """Get content of the current file"""
    owner = state.owner
    repo = state.repo
    currIndex = state.curr_index
    file = state.files[currIndex]
    content = get_file_content.invoke({
        "owner": owner,
        "repo": repo,
        "file_path": file
    })
    return MessageState(
        messages=[],
        curr_index=state.curr_index+1,
        files=state.files,
        owner=state.owner,
        repo=state.repo,
        curr_observation=content,
        observations_added=state.observations_added,
        llm_calls=state.llm_calls,
        path=state.path,
    )
