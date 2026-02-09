from models.state import MessageState
from typing_extensions import Literal

def should_continue(state:MessageState) -> Literal["get_contents", "summarizer"]:

    currIndex = state.curr_index
    if(currIndex >= len(state.files)):
        return "summarizer"
    return "get_contents"
