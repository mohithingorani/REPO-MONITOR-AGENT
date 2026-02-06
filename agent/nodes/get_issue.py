from models.state import MessageState
from tools.issue_detector import is_issue_in_file

def get_issue(state: MessageState) -> MessageState:
    obs = state.curr_observation
    file_name = state.files[state.curr_index]
    response = is_issue_in_file(obs, file_name)
    new_observations = ""

    if response.is_issue and response.issue_description:
        new_observations = response.issue_description
    
    return MessageState(
        messages=[],                 
        files=state.files,
        owner=state.owner,
        repo=state.repo,
        curr_index=state.curr_index,
        curr_observation="",                     # reset
        observations=[new_observations] if new_observations else [],           # append-safe
        issue_called=state.issue_called + (1 if response.is_issue else 0),
        observations_added=state.observations_added,
        llm_calls=state.llm_calls,
        path=state.path,
    )


