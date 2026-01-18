from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from graph import run_chat_workflow
import os

app = FastAPI(title="Study Guidance Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    message: str
    thread_id: str = "default_thread"

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Study Guidance Bot API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(input_data: ChatInput):
    try:
        response_text = await run_chat_workflow(input_data.message, input_data.thread_id)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Trigger reload 4
