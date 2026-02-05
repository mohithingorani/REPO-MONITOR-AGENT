# Defining State
import os
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from typing_extensions import Annotated, Literal, TypedDict
from langchain.messages import AnyMessage
from models import ImportantFilesOutput, MessageState
from utils import show_image
from utils.github import get_repo_files, get_file_content, is_issue_in_file
from langchain.messages import SystemMessage, HumanMessage,ToolMessage
from langgraph.graph import StateGraph,START,END
from typing import List
llm = ChatOllama(model="gpt-oss:20b",temperature=0)

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
def should_continue(state:MessageState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    if state["messages"][-1].tool_calls:
        return "tool_node"
    else:
        return END
    
def show_image(agent):
    png_bytes = agent.get_graph(xray=True).draw_mermaid_png()
    with open("agent_graph.png", "wb") as f:
        f.write(png_bytes)
    os.system("open agent_graph.png")

agent_builder = StateGraph(state_schema=MessageState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node",END]
)

agent_builder.add_edge("tool_node","llm_call")

agent = agent_builder.compile()
show_image(agent)