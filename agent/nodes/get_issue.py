from models.state import MessageState,ObservationState
from tools.issue_detector import is_issue_in_file

def get_issue(state: MessageState) -> MessageState:
    obs = state.curr_observation
    file_name = state.files[state.curr_index]
    response = is_issue_in_file(obs)
    
    new_observatvations = []

    if response.is_issue and response.issue_description:
        obs = ObservationState(file=file_name,severity=response.severity,issue=response.issue_description)
        new_observatvations.append(obs)
    
    return MessageState(
        messages=[],                 
        files=state.files,
        owner=state.owner,
        repo=state.repo,
        curr_index=state.curr_index+1,
        curr_observation="",                     
        observations = new_observatvations,
        issue_called=state.issue_called + (1 if response.is_issue else 0),
        llm_calls=state.llm_calls,
        path=state.path,
    )


