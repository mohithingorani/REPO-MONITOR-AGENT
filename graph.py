# Defining State
import operator
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from typing_extensions import Annotated, TypedDict
from langchain.messages import AnyMessage
from utils.github import get_repo_files, get_important_files, get_file_content, is_issue_in_file
from langchain.messages import SystemMessage, HumanMessage,ToolMessage
class FileState(BaseModel):
    file_path : str

class MessageState(BaseModel):
    messages : Annotated[list[AnyMessage],operator.add]
    llm_calls : int = 0
    files: list[FileState] | None = None

llm = ChatOllama(model="gpt-oss:20b",temperature=0)


tools = [get_repo_files, get_important_files, get_file_content, is_issue_in_file]
tools_by_name = {tool.__name__:tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


def llm_call(state:dict):
    """LLM decides next action using tool calls or final answer based on current state."""

    return {
        "messages":[
            llm_with_tools.invoke([
                SystemMessage(content="You are an AI agent that helps analyze GitHub repositories. Based on the current state, decide the next action to take using the available tools or provide a final answer."),
            ])
            + state["messages"] + state.get("files", [])
        ],
        "llm_calls": state["llm_calls"] + 1
    }