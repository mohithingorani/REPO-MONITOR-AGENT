from models.state import MessageState
from models.outputs import ImportantFilesOutput
from langchain.messages import SystemMessage,HumanMessage,ToolMessage

from llm.ollama import llm


def get_important_files(state: MessageState)->MessageState:
    
    files = state.files
    llm_with_structured_output:ImportantFilesOutput = llm.with_structured_output(ImportantFilesOutput)
    system_message = SystemMessage(
        content=(
            "You analyze a GitHub repository and identify files that are important for understanding the project. "
            "Include core source files (e.g. .py, .js, .ts, .java) and key documentation (README, docs). "
            "Exclude config files, environment files, editor settings, dependencies, build artifacts, and "
            "non-essential utilities or helper components. Give at most 10 important files. If the repository has fewer than 10 files, return all of them"
        )
    )
    human_message = HumanMessage(content=f"Here is a list of files in the repository: {files}. Please identify the important files from this list.")
    response = llm_with_structured_output.invoke([system_message, human_message])
    # testing with small files
    important = response.important_files
    return MessageState(
        owner=state.owner,
        repo=state.repo,
        llm_calls=state.llm_calls+1,
        files=important,
        messages=[ToolMessage(content=f"Identified {len(important)} important files from the repo", tool_call_id="get_important_files")],
        path="",
        curr_index=state.curr_index,
        observations=[]
    )
    
