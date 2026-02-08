from typing import Literal
from langgraph.types import interrupt, Command
from models.state import MessageState


def approval_node(state: MessageState) -> Command[Literal["get_metadata", "important_files"]]:
    is_approved = interrupt({
        "question": "Do you want to proceed with this action?",
        "details": state.files
    })
    if not is_approved:
        return Command(goto="important_files")  
    else:
        
        return Command(goto="get_metadata")