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
from types import SimpleNamespace

app = FastAPI(
    docs_url="/swagger",
    openapi_url="/openapi.json",
)
game = {}

_pkg_dir = os.path.dirname(__file__)
www_dir = os.path.join(_pkg_dir, "www")
app.mount("/www", StaticFiles(directory=www_dir))
templates = Jinja2Templates(directory=www_dir)

@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    user = request.headers.get("x-user-sub")
    print("Authentified user: " + str(user))

    if user not in game:
        game[user] = SimpleNamespace()
        game[user].tama = Tama()
        game[user].care = Carebot(game[user].tama)
        asyncio.create_task(game[user].care.run())

    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    user = websocket.headers.get("x-user-sub")
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(
                {
                    "matrix": await game[user].tama.matrix(),
                    "icons": await game[user].tama.icons(),
                    "runs": await game[user].tama.runs(),
                    "care": game[user].care.active,
                    "background": game[user].tama.version if game[user].tama.version is not None else "p1"
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
    user = websocket.headers.get("x-user-sub")
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({"freq": await game[user].tama.freq()})
            await asyncio.sleep(1 / 20)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=1011)

@app.post("/rom")
async def Load_ROM(request: Request, file: UploadFile = File()):
    user = request.headers.get("x-user-sub")
    try:
        content = await file.read()
        await game[user].tama.load("ROM", content)
        game[user].care.stop()
        game[user].care.reset()
        return {"posted": "rom"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rom")
async def Dump_ROM(request: Request):
    user = request.headers.get("x-user-sub")
    try:
        data = await game[user].tama.dump("ROM")
        return Response(
            content=data,
            media_type="application/octet-stream",
            headers={"Content-Disposition": 'attachment; filename="rom.bin"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/rom")
async def Delete_ROM(request: Request):
    user = request.headers.get("x-user-sub")
    try:
        await game[user].tama.reset("ROM")
        game[user].care.stop()
        return {"deleted": "rom"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cpu")
async def Load_CPU(request: Request, file: UploadFile = File()):
    user = request.headers.get("x-user-sub")
    try:
        content = await file.read()
        await game[user].tama.load("CPU", content)
        game[user].care.stop()
        return {"posted": "cpu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cpu")
async def Dump_CPU(request: Request):
    user = request.headers.get("x-user-sub")
    try:
        data = await game[user].tama.dump("CPU")
        return Response(
            content=data,
            media_type="application/octet-stream",
            headers={"Content-Disposition": 'attachment; filename="cpu.bin"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/cpu")
async def Delete_CPU(request: Request):
    user = request.headers.get("x-user-sub")
    try:
        await game[user].tama.reset("CPU")
        game[user].care.stop()
        return {"deleted": "cpu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/manage")
async def Manage(request: Request, do: str):
    user = request.headers.get("x-user-sub")
    match do:
        case "start":
            await game[user].tama.start()
            return {"manage": "Tama started"}
        case "stop":
            await game[user].tama.stop()
            game[user].care.stop()
            return {"manage": "Tama stopped"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid manage action")

@app.post("/click")
async def click(request: Request, button: str):
    user = request.headers.get("x-user-sub")
    match button:
        case "A":
            await game[user].tama.click("A", .1)
            return {"clicked": "A"}
        case "B":
            await game[user].tama.click("B", .1)
            return {"clicked": "B"}
        case "C":
            await game[user].tama.click("C", .1)
            return {"clicked": "C"}
        case "AC":
            await game[user].tama.click(["A","C"], .5)
            return {"clicked": "A+C"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid click action")
        
@app.post("/force_version")
async def Force_specific_version(request: Request, version: str = "p1"):
    user = request.headers.get("x-user-sub")
    match version:
        case "p1":
            game[user].tama.version = "p1"
            return {"background": "p1 theme"}
        case "p2":
            game[user].tama.version = "p2"
            return {"background": "p2 theme"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid version")

@app.post("/carebot")
async def Care(request: Request, do: str):
    user = request.headers.get("x-user-sub")
    match do:
        case "start":
            game[user].care.start()
            return {"carebot": "started"}
        case "stop":
            game[user].care.stop()
            return {"carebot": "stopped"}
        case "reset":
            game[user].care.reset()
            return {"carebot": "reset"}
        case _:
            raise HTTPException(status_code=400, detail = "Invalid carebot action")
        
@app.post("/param_carebot")
async def Param_Carebot(request: Request, disc: bool = True, check_every: float = 5*60):
    user = request.headers.get("x-user-sub")
    game[user].care.parameterize(
        disc = disc, 
        check_every = check_every
    )
    return {"param": game[user].care.param}

@app.post("/p2")
async def Switch_to_P2(request: Request):
    user = request.headers.get("x-user-sub")
    try:
        await p2(game[user].tama)
        return {"P2": "Conversion succesful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/secret")
async def Secret_character(request: Request):
    user = request.headers.get("x-user-sub")
    try:
        await secret(game[user].tama)
        return {"secret": "Conversion succesful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

