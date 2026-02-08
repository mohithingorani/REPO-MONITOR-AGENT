from agent.graph import graph
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig



from langgraph.types import Command

from langchain.messages import HumanMessage
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig

prompt = "Tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK"
config: RunnableConfig = {"configurable": {"thread_id": "1"}}

response = graph.invoke(
    {"messages": [HumanMessage(content=prompt)]},
    config
)

def askHuman():
    state = graph.get_state(config)
    print(state)
    res = input(f"Are you fine with these files?").lower()
    if "yes" in res:
        return True
    else:
        return False


print(response["__interrupt__"][0].value)
    # val = askHuman()

graph.invoke(Command(resume=False),config)


print(graph.get_state_history(config))
print("\nFinal Response")
print(response["messages"][-1].content)
