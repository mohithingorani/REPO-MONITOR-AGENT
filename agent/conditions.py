from models.state import MessageState
from typing_extensions import Literal

def should_continue(state:MessageState) -> Literal["tool_node", "summarizer"]:

    currIndex = state.curr_index
    if(currIndex >= len(state.files)):
        return "summarizer"
    return "get_issue"
