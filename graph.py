# Defining State
from typing_extensions import  Literal
from langchain.messages import AnyMessage
from pydantic_types import  MessageState,isIssue
from utils.github import get_repo_files, get_file_content, get_important_files,parse_repo,is_issue_in_file
from langchain.messages import SystemMessage, HumanMessage,ToolMessage
from langgraph.graph import StateGraph,START,END
from model import llm
from dotenv import load_dotenv
from pydantic import BaseModel
import operator
from typing import Annotated
from langchain_core.tools import tool
from utils.image_show import show_image
load_dotenv()



def should_continue(state:MessageState) -> Literal["tool_node", END]:

    currIndex = state.curr_index
    if(currIndex >= len(state.files)):
        return END
    return "tool_node"


llm_with_tools = llm.bind_tools([get_file_content])

class LLMWithTools(BaseModel):
    messages: Annotated[list[AnyMessage], operator.add]
    curr_index: int = 0


def llm_call(state:MessageState) -> MessageState:
    """LLM decide whether to call a tool or not"""
    owner = state.owner
    repo = state.repo
    currIndex = state.curr_index
    file = state.files[currIndex]
    response = llm_with_tools.invoke([
           SystemMessage(
            content=(
                "You MUST call the get_file_content tool.\n"
                "Do not answer in text.\n"
                "Only call the tool with valid JSON arguments."
            )
        ),
       HumanMessage(
    content=(
        f"owner: {owner}\n"
        f"repo: {repo}\n"
        f"file_path: {file}\n\n"
        "After fetching the file, decide if it contains an issue."
    )
)
    ])
    return MessageState(messages=[response], curr_index=state.curr_index+1, files=state.files, owner=state.owner, repo=state.repo,observations=state.observations)


def tool_node(state: MessageState) -> MessageState:
    """Performs the tool call"""

    obs = ""
    result = []
    for tool_call in state.messages[-1].tool_calls:
        observation = get_file_content.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        obs += observation + "\n"
    return MessageState(messages=state.messages + result, curr_index=state.curr_index, files=state.files, owner=state.owner, repo=state.repo,curr_observation=obs)

def get_issue(state:MessageState)->MessageState:
    obs = state.curr_observation
    response = is_issue_in_file(obs)
    if response.is_issue:
        return MessageState(**{
            **state.model_dump(),
            "observations":[response.issue_description]
        })
    return state

#  Building the Agent
agent_builder = StateGraph(state_schema=MessageState)
agent_builder.add_node("parse_repo",parse_repo)
agent_builder.add_node("get-all-files",get_repo_files)
agent_builder.add_node("important-files",get_important_files)
agent_builder.add_node("llm_call",llm_call)
agent_builder.add_node("tool_node",tool_node)
agent_builder.add_node("get_issue",get_issue)

agent_builder.add_edge(START,"parse_repo")
agent_builder.add_edge("parse_repo","get-all-files")
agent_builder.add_edge("get-all-files","important-files")
agent_builder.add_edge("important-files","llm_call")
agent_builder.add_conditional_edges("llm_call",should_continue,["tool_node",END])
# agent_builder.add_edge("tool_node", "llm_call")
agent_builder.add_edge("tool_node","get_issue")
agent_builder.add_edge("get_issue","llm_call")


# Compile the agent
agent = agent_builder.compile()
show_image(agent)


# Invoking the Agent
response = agent.invoke({"messages":[HumanMessage(content="tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK")]})
print(response)