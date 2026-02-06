from models.state import MessageState
from langchain.messages import SystemMessage,HumanMessage

from llm.ollama import llm

def summarization_node(state:MessageState):
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
        llm_calls=state.llm_calls,
        path=state.path,
    )