from typing import Literal
from types import MessageState
from langgraph.graph import END
def should_continue(state:MessageState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    if state["messages"][-1].tool_calls:
        return "tool_node"
    else:
        return END
    
