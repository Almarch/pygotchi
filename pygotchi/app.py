from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, File, UploadFile, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import os
from .Tama import Tama

app = FastAPI()
tama = Tama()
background = "p1"

_pkg_dir = os.path.dirname(__file__)
www_dir = os.path.join(_pkg_dir, "www")
app.mount("/www", StaticFiles(directory=www_dir))
templates = Jinja2Templates(directory=www_dir)

@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(
                {
                    "matrix": tama.matrix(),
                    "icons": tama.icons(),
                    "runs": tama.runs(),
                    "background": background,
                }
            )
            await asyncio.sleep(1 / 5)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=1011)

@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({"freq": tama.freq()})
            await asyncio.sleep(1 / 20)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=1011)

@app.post("/rom")
async def Load_ROM(file: UploadFile = File()):
    try:
        content = await file.read()
        tama.load("ROM", content)
        return {"posted": "rom"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rom")
async def Dump_ROM():
    try:
        data = tama.dump("ROM")
        return Response(
            content=data,
            media_type="application/octet-stream",
            headers={"Content-Disposition": 'attachment; filename="rom.bin"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/rom")
async def Delete_ROM():
    try:
        tama.reset("ROM")
        return {"deleted": "rom"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cpu")
async def Load_CPU(file: UploadFile = File()):
    try:
        content = await file.read()
        tama.load("CPU", content)
        return {"posted": "rom"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cpu")
async def Dump_CPU():
    try:
        data = tama.dump("CPU")
        return Response(
            content=data,
            media_type="application/octet-stream",
            headers={"Content-Disposition": 'attachment; filename="cpu.bin"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/cpu")
async def Delete_CPU():
    try:
        tama.reset("CPU")
        return {"deleted": "cpu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/manage")
async def Manage(do: str):
    match do:
        case "start":
            tama.start()
            return {"manage": "Tama started"}
        case "stop":
            tama.stop()
            return {"manage": "Tama stopped"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid manage action")

@app.post("/click")
async def click(button: str):
    match button:
        case "A":
            tama.click("A", .1)
            return {"clicked": "A"}
        case "B":
            tama.click("B", .1)
            return {"clicked": "B"}
        case "C":
            tama.click("C", .1)
            return {"clicked": "C"}
        case "AC":
            tama.click(["A","C"], .5)
            return {"clicked": "A+C"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid click action")
        
@app.post("/background")
async def Change_background(theme: str):
    match theme:
        case "p1":
            background = "p1"
            return {"background": "p1 theme"}
        case "p2":
            background = "p2"
            return {"background": "p2 theme"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid background")
