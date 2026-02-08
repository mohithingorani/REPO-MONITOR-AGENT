from pydantic import BaseModel,Field

class PromptRequest(BaseModel):
    prompt:str = Field(...,min_length=1,max_length=500, description="The prompt to send to the agent")

