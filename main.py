from agent.graph import agent
from langchain.messages import HumanMessage

# Invoking the Agent
def invoke_agent(prompt:str):
    response = agent.invoke({"messages":[HumanMessage(content=prompt)]})
    print("\n\n\n\n\n\n\n\n Final Response")
    print(response.get("messages")[-1].content)



if(__name__=="__main__"):
    invoke_agent("Tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK")
    