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



def should_continue(state:MessageState) -> Literal["tool_node", "summarizer"]:

    currIndex = state.curr_index
    if(currIndex >= len(state.files)):
        return "summarizer"
    return "get_issue"


llm_with_tools = llm.bind_tools([get_file_content])

class LLMWithTools(BaseModel):
    messages: Annotated[list[AnyMessage], operator.add]
    curr_index: int = 0



# # i dont need llm_call to get content of file
# def llm_call(state:MessageState) -> MessageState:
#     """LLM decide whether to call a tool or not"""
#     owner = state.owner
#     repo = state.repo
#     currIndex = state.curr_index
#     file = state.files[currIndex]
#     response = llm_with_tools.invoke([
#            SystemMessage(
#             content=(
#                 "You MUST call the get_file_content tool.\n"
#                 "Do not answer in text.\n"
#                 "Only call the tool with valid JSON arguments."
#             )
#         ),
#        HumanMessage(
#     content=(
#         f"owner: {owner}\n"
#         f"repo: {repo}\n"
#         f"file_path: {file}\n\n"
#         "After fetching the file, decide if it contains an issue."
#     )
# )
#     ])
#     return MessageState(messages=[response], curr_index=state.curr_index+1, files=state.files, owner=state.owner, repo=state.repo,llm_calls=state.llm_calls+1)

def get_contents_of_file(state:MessageState) -> str:
    """Get content of the current file"""
    owner = state.owner
    repo = state.repo
    currIndex = state.curr_index
    file = state.files[currIndex]
    content = get_file_content.invoke({
        "owner": owner,
        "repo": repo,
        "file_path": file
    })
    return MessageState(
        messages=[],
        curr_index=state.curr_index+1,
        files=state.files,
        owner=state.owner,
        repo=state.repo,
        curr_observation=content,
        observations_added=state.observations_added,
        llm_calls=state.llm_calls,
        path=state.path,
    )


# def tool_node(state: MessageState) -> MessageState:
#     """Performs the tool call"""

#     obs = ""
#     tool_messages = []
#     for tool_call in state.messages[-1].tool_calls:
#         observation = get_file_content.invoke(tool_call["args"])
#         tool_messages.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
#         obs += observation + "\n"
#     return MessageState(messages= tool_messages, curr_index=state.curr_index, files=state.files, owner=state.owner,observations=[], repo=state.repo,curr_observation=obs,observations_added=state.observations_added+1)


def summarization_tool(state:MessageState):
    observations = state.observations

    response = llm.invoke(
        [SystemMessage(content="You are a code review expert. Analyze a list of issue descriptions found in repository files. Summarize them by grouping similar issues, identifying patterns, and prioritizing by severity (Critical, High, Medium, Low). Output in structured markdown with categories, counts, and actionable recommendations. Do not use tools or function calls."),
        HumanMessage(content=f"""Summarize these issues found across the repository files:

        {observations}

        Provide:
        1. Top 3 issue categories by frequency
        2. Critical issues (security/bugs blocking functionality) 
        3. Overall severity distribution
        4. One key recommendation per major category""")])
    
    return MessageState(
        messages=[response],                 
        files=state.files,
        owner=state.owner,
        repo=state.repo,
        curr_index=state.curr_index,
        curr_observation="",                    
        observations=[],
        issue_called=state.issue_called,
        observations_added=state.observations_added,
        llm_calls=state.llm_calls,
        path=state.path,
    )


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



#  Building the Agent
agent_builder = StateGraph(state_schema=MessageState)
agent_builder.add_node("parse_repo",parse_repo)
agent_builder.add_node("get-all-files",get_repo_files)
agent_builder.add_node("important-files",get_important_files)
# agent_builder.add_node("llm_call",llm_call)
agent_builder.add_node("get_contents",get_contents_of_file)
# agent_builder.add_node("tool_node",tool_node)
agent_builder.add_node("get_issue",get_issue)
agent_builder.add_node("summarizer",summarization_tool)

agent_builder.add_edge(START,"parse_repo")
agent_builder.add_edge("parse_repo","get-all-files")
agent_builder.add_edge("get-all-files","important-files")
agent_builder.add_edge("important-files","get_contents")
agent_builder.add_conditional_edges("get_contents",should_continue,["get_issue","summarizer"])
# agent_builder.add_edge("tool_node", "llm_call")
# agent_builder.add_edge("tool_node","get_issue")
agent_builder.add_edge("get_issue","get_contents")
agent_builder.add_edge("summarizer",END)


# Compile the agent
agent = agent_builder.compile()
show_image(agent)


# Invoking the Agent
response = agent.invoke({"messages":[HumanMessage(content="tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK")]})

print("\n\n\n\n\n\n\n\n Final Response")
print(response.get("messages")[-1].content)