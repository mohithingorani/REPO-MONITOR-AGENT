from fastapi import APIRouter,HTTPException
from api.schemas.chat import PromptRequest
from main import invoke_agent


router = APIRouter(prefix="/chat",tags=["chat"])

@router.post("/")
async def chat(request:PromptRequest):
    try:
        response = invoke_agent(request.prompt)
        return {"response":response}
    except Exception as e:
        raise HTTPException(status_code=500,detail="Agent execution failed")