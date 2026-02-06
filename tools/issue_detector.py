from models.outputs import isIssue
from langchain.messages import SystemMessage,HumanMessage

from llm.ollama import llm

def is_issue_in_file(content:str,file_name:str) -> isIssue:
    """Analyze the content of a file to determine if it describes an issue."""
    llm_with_structured_output = llm.with_structured_output(isIssue)
    response = llm_with_structured_output.invoke([
        SystemMessage(content="You analyze the content of a file and determine if it is an issue or not.Consider even a suggestion as issue in that specific file.Give name of the file in issue_description."),
        HumanMessage(content=f"Here is the content of the file:\n{content}\nBased on this content, is there an issue described in the file? If so, provide a brief description of the issue. If not, indicate that it is not an issue.")
    ])
    return response

