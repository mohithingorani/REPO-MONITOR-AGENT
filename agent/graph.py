# Defining State
from typing_extensions import  Literal
from langchain.messages import AnyMessage
from agent.conditions import should_continue
from agent.nodes.get_issue import get_issue
from agent.nodes.get_contents import get_contents_of_file
from agent.nodes.important_files import get_important_files
from agent.nodes.summarize import summarization_node
from agent.nodes.get_repo_files import get_repo_files
from models.state import  MessageState
from tools.parse_repo import parse_repo
from tools.github import  get_file_content
from langgraph.graph import StateGraph,START,END
from llm.ollama import llm
from dotenv import load_dotenv
from pydantic import BaseModel
import operator
from typing import Annotated
from langchain_core.tools import tool
from utils.image_show import show_image
load_dotenv()


llm_with_tools = llm.bind_tools([get_file_content])



#  Building the Agent
agent_builder = StateGraph(state_schema=MessageState)
agent_builder.add_node("parse_repo",parse_repo)
agent_builder.add_node("get-all-files",get_repo_files)
agent_builder.add_node("important-files",get_important_files)
agent_builder.add_node("get_contents",get_contents_of_file)
agent_builder.add_node("get_issue",get_issue)
agent_builder.add_node("summarizer",summarization_node)

agent_builder.add_edge(START,"parse_repo")
agent_builder.add_edge("parse_repo","get-all-files")
agent_builder.add_edge("get-all-files","important-files")
agent_builder.add_edge("important-files","get_contents")
# agent_builder.add_conditional_edges("get_contents",should_continue,["get_issue","summarizer"])
# agent_builder.add_edge("get_issue","get_contents")
agent_builder.add_edge("get_contents","get_issue")
agent_builder.add_conditional_edges("get_issue",should_continue,["get_contents","summarizer"])
agent_builder.add_edge("summarizer",END)


# Compile the agent
agent = agent_builder.compile()
show_image(agent)


