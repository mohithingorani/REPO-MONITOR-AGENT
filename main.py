from agent.graph import graph
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
# Invoking the Agent
def invoke_agent(prompt:str):
    response = graph.invoke({"messages":[HumanMessage(content=prompt)]},config)
    print("\n\n\n\n\n\n\n\n Final Response")
    print(response.get("messages")[-1].content)

    # Get latest state snapshot
    output = graph.get_state(config)
    print("\nOutput = ",output)

    # Get state history
    history = list(graph.get_state_history(config))
    print("\n\n\nHistory = ",history)

    # Get initial state
    print("\n\nInitial State = ",history[-1])

config:RunnableConfig = {"configurable":{"thread_id":"1"}}

if(__name__=="__main__"):
    invoke_agent("Tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK")



