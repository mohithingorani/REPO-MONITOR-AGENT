from fastapi import FastAPI
from api.chat import router as chat_router
from api.core.logging import setup_logging
from fastapi.middleware.cors import CORSMiddleware

setup_logging()
app = FastAPI(
    title="Agent API",
    version="1.0.0"
)
origins = [
    "http://127.0.0.1:3000", 
        "http://localhost:3000",
    "https://yourproductiondomain.com", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


app.include_router(chat_router)


@app.get("/health")
def health():
    return {"status":"ok"}