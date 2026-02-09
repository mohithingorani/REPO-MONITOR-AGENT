import logging
from fastapi import APIRouter,HTTPException
from api.schemas.chat import PromptRequest
from main import invoke_agent
from starlette.concurrency import run_in_threadpool 

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat",tags=["chat"])

@router.post("/")
async def chat(request:PromptRequest):
    try:
        response = await run_in_threadpool(invoke_agent,request.prompt)
        return {"response":response}
    
    except ValueError as e:
        logger.warning(f"Invalid Input: {e}")
        raise HTTPException(status_code=400,detail=str(e))
    
    except Exception as e:
        logger.exception("Agent Failed")
        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"
        )