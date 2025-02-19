from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import os
from .Tama import Tama


app = FastAPI()
tama = Tama()

_pkg_dir = os.path.dirname(__file__)
www_dir = os.path.join(_pkg_dir, "www")
app.mount("/www", StaticFiles(directory=www_dir))
templates = Jinja2Templates(directory=www_dir)

@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/video")
async def websocket_screen(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json(
             {
                  "matrix": tama.matrix(),
                  "icon": tama.icon(),
                  "runs": tama.runs(),
             }
        )
        await asyncio.sleep(1/6)

@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({"freq": tama.freq()})
        await asyncio.sleep(1/100)

@app.post("/rom")
async def flash_rom(file: UploadFile = File(...)):

@app.get("/rom")
async def dump_rom():
    return tama.dump()

@app.post("/cpu")
async def load_cpu(file: UploadFile = File(...)):

@app.get("/cpu")
async def save_cpu():
    return tama.save()