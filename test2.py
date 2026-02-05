from models import ImportantFilesOutput,MessageState
from langchain.messages import HumanMessage,SystemMessage
from langchain_ollama import ChatOllama
llm = ChatOllama(model="gpt-oss:20b",temperature=0)

def get_important_files(state: MessageState):
    files = state.files
    llm_with_structured_output:ImportantFilesOutput = llm.with_structured_output(ImportantFilesOutput)
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
    return { 
        "owner": state.owner,
        "repo": state.repo,
        "llm_calls":state.llm_calls+1,
        "files":response.important_files,
        "messages":[],
        "path":"",
        
    }
    


# state = {
#  "files":  [".gitignore",".python-version","README.md","main.py","pyproject.toml","requirements.txt","uv.lock"]
# }
# print(state["files"])

# important_files = get_important_files(state)
# print(important_files)