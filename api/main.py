from fastapi import FastAPI
from api.chat import router as chat_router
from api.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Agent API",
    version="1.0.0"
)

app.include_router(chat_router)


@app.get("health")
def health():
    return {"status":"ok"}