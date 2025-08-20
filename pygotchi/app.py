from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, File, UploadFile, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import os
from .Tama import Tama
from .Carebot import Carebot
from .p2 import p2
from .secret import secret

app = FastAPI(
    docs_url="/swagger",
    openapi_url="/openapi.json",
)
tama = Tama()
carebot = Carebot(tama)

_pkg_dir = os.path.dirname(__file__)
www_dir = os.path.join(_pkg_dir, "www")
app.mount("/www", StaticFiles(directory=www_dir))
templates = Jinja2Templates(directory=www_dir)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(carebot.run())

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
                    "matrix": await tama.matrix(),
                    "icons": await tama.icons(),
                    "runs": await tama.runs(),
                    "care": carebot.active,
                    "background": tama.version if tama.version is not None else "p1"
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
            await websocket.send_json({"freq": await tama.freq()})
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
        await tama.load("ROM", content)
        carebot.stop()
        carebot.reset()
        return {"posted": "rom"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rom")
async def Dump_ROM():
    try:
        data = await tama.dump("ROM")
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
        await tama.reset("ROM")
        carebot.stop()
        return {"deleted": "rom"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cpu")
async def Load_CPU(file: UploadFile = File()):
    try:
        content = await file.read()
        await tama.load("CPU", content)
        carebot.stop()
        return {"posted": "cpu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cpu")
async def Dump_CPU():
    try:
        data = await tama.dump("CPU")
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
        await tama.reset("CPU")
        carebot.stop()
        return {"deleted": "cpu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/manage")
async def Manage(do: str):
    match do:
        case "start":
            await tama.start()
            return {"manage": "Tama started"}
        case "stop":
            await tama.stop()
            carebot.stop()
            return {"manage": "Tama stopped"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid manage action")

@app.post("/click")
async def click(button: str):
    match button:
        case "A":
            await tama.click("A", .1)
            return {"clicked": "A"}
        case "B":
            await tama.click("B", .1)
            return {"clicked": "B"}
        case "C":
            await tama.click("C", .1)
            return {"clicked": "C"}
        case "AC":
            await tama.click(["A","C"], .5)
            return {"clicked": "A+C"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid click action")
        
@app.post("/force_version")
async def Force_specific_version(version: str = "p1"):
    match version:
        case "p1":
            tama.version = "p1"
            return {"background": "p1 theme"}
        case "p2":
            tama.version = "p2"
            return {"background": "p2 theme"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid version")

@app.post("/carebot")
async def Care(do: str):
    match do:
        case "start":
            carebot.start()
            return {"carebot": "started"}
        case "stop":
            carebot.stop()
            return {"carebot": "stopped"}
        case "reset":
            carebot.reset()
            return {"carebot": "reset"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid carebot action")
        
@app.post("/param_carebot")
async def Param_Carebot(disc: bool = True, check_every: float = 5*60):
    carebot.parameterize(
        disc = disc, 
        check_every = check_every
    )
    return {"param": carebot.param}

@app.post("/p2")
async def Switch_to_P2():
    try:
        await p2(tama)
        return {"P2": "Conversion succesful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/secret")
async def Secret_character():
    try:
        await secret(tama)
        return {"secret": "Conversion succesful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

