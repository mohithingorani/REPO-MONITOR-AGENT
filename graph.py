# Defining State
from typing_extensions import  Literal
from langchain.messages import AnyMessage
from pydantic_types import  MessageState,isIssue
from utils.github import get_repo_files, get_file_content, get_important_files,parse_repo
from langchain.messages import SystemMessage, HumanMessage,ToolMessage
from langgraph.graph import StateGraph,START,END
from model import llm
from dotenv import load_dotenv
from pydantic import BaseModel
import operator
from typing import Annotated
from langchain_core.tools import tool
load_dotenv()



def should_continue(state:MessageState) -> Literal["tool_node", END]:

    currIndex = state.curr_index
    if(currIndex >= len(state.messages)):
        return END
    return "get-file-content"


llm_with_tools = llm.bind_tools([get_file_content])

class LLMWithTools(BaseModel):
    messages: Annotated[list[AnyMessage], operator.add]


def llm_call(state:MessageState) -> LLMWithTools:
    """LLM decide whether to call a tool or not"""
    owner = state.owner
    repo = state.repo
    currIndex = state.curr_index
    file = state.files[currIndex]
    response = llm_with_tools.invoke([
        HumanMessage(content=f"Is there an issue in the following content? If yes, describe the issue. If not, just say it's not an issue. Owner = {owner} and repo = {repo}\n\nContent:\n" + file ),
    ])
    return LLMWithTools(messages=[response])


def tool_node(state: LLMWithTools) -> dict:
    """Performs the tool call"""

    result = []
    for tool_call in state.messages[-1].tool_calls:
        observation = get_file_content.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    
    return {"messages": result}

#  Building the Agent
agent_builder = StateGraph(state_schema=MessageState)
agent_builder.add_node("parse_repo",parse_repo)
agent_builder.add_node("get-all-files",get_repo_files)
agent_builder.add_node("important-files",get_important_files)
agent_builder.add_node("llm_call",llm_call)
agent_builder.add_node("tool_node",tool_node)
agent_builder.add_edge(START,"parse_repo")
agent_builder.add_edge("parse_repo","get-all-files")
agent_builder.add_edge("get-all-files","important-files")
agent_builder.add_edge("important-files","llm_call")
agent_builder.add_edge("llm_call","tool_node")

# Compile the agent
agent = agent_builder.compile()


# Invoking the Agent
agent.invoke({"messages":[HumanMessage(content="tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK")]})
