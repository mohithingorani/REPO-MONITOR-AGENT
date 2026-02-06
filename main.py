from agent.graph import agent
from langchain.messages import HumanMessage

# Invoking the Agent
response = agent.invoke({"messages":[HumanMessage(content="tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK")]})

print("\n\n\n\n\n\n\n\n Final Response")
print(response.get("messages")[-1].content)