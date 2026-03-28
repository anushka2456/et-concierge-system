from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from agents.gatekeeper import Gatekeeper
from db.sqlite_db import init_db

init_db()
app = FastAPI()
gatekeeper = Gatekeeper()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(input: ChatInput):
    return {"response": gatekeeper.handle_chat(input.message)}

@app.post("/voice")
async def voice(file: UploadFile = File(...)):
    try:
        result = gatekeeper.handle_voice(file)
        return {"persona": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/roadmap")
async def roadmap():
    return gatekeeper.get_roadmap()

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/debug/memory")
def debug_memory():
    from services.memory import get_messages
    return get_messages(1)


@app.get("/debug/persona")
def debug_persona():
    from services.memory import get_persona
    return get_persona(1)


@app.get("/debug/resources")
def debug_resources(q: str):
    from agents.librarian import Librarian
    lib = Librarian()
    return lib.search(q)

@app.get("/")
def health():
    return {"status": "AI Concierge Backend Running"}