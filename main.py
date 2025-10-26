from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from api import upload, chat  # your routers

app = FastAPI()

# Mount routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

# Mount static files
app.mount("/static", StaticFiles(directory="static", html = True), name="static")

# Serve index.html at root

@app.get("/") 
async def root():
    return FileResponse(Path("static/index.html"))
