from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from main import invoke_agent

class PromptRequest(BaseModel):
    prompt:str

app = FastAPI()


@app.post("/chat")
def chat(prompt:PromptRequest):
    try:
        response = invoke_agent(prompt.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))