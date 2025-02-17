from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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
