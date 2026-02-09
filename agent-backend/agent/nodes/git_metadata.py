from models.state import MessageState,RepoMetaData
from llm.ollama import llm
from langchain.messages import SystemMessage,HumanMessage


llm_with_structured_output = llm.with_structured_output(RepoMetaData)

def get_metadata(state:MessageState):
    response = llm_with_structured_output.invoke([
        SystemMessage(content="""You analyze a GitHub repository at a high level. 
                "Infer tech stack, languages, frameworks, license, 
                "and project maturity based on file names, structure, 
                "README content, and dependencies."""),
        HumanMessage(content=f""" Repository Files
                     {state.files}
                    """)
    ])
    return MessageState(
      repo_metadata=response,
      llm_calls=state.llm_calls+1,
      files=state.files,
      owner = state.owner,
      repo=state.repo,
      messages=[]
    )