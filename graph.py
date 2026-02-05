# Defining State
import os
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from typing_extensions import  Literal
from langchain.messages import AnyMessage
from pydantic_types import  MessageState
from utils.github import get_repo_files, get_file_content, is_issue_in_file,get_important_files,parse_repo
from langchain.messages import SystemMessage, HumanMessage,ToolMessage
from langgraph.graph import StateGraph,START,END

from dotenv import load_dotenv
load_dotenv()






#  Building the Agent
agent_builder = StateGraph(state_schema=MessageState)
agent_builder.add_node("parse_repo",parse_repo)
agent_builder.add_node("get-all-files",get_repo_files)
agent_builder.add_node("important-files",get_important_files)


agent_builder.add_edge(START,"parse_repo")
agent_builder.add_edge("parse_repo","get-all-files")
agent_builder.add_edge("get-all-files","important-files")
agent_builder.add_edge("important-files",END)

# Compile the agent
agent = agent_builder.compile()


# Invoking the Agent
agent.invoke({"messages":[HumanMessage(content="tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK")]})
