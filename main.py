from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from httpx import request
from models.Gastos import Gastos

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Início"})

@app.get("/", response_class=HTMLResponse)
async def mostrar_gastos(request: Request):
    lista_gastos = [
        Gastos(dono="Matheus", cartao="5256", vigencia="Mar-2025", valor=11.90),
        Gastos(dono="Gabriella", cartao="4897", vigencia="Mar-2025", valor=45.00),
    ]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "gastos": lista_gastos
    })

@app.get("/sobre", response_class=HTMLResponse)
async def sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request, "title": "Sobre"})
