from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from models.Gastos import Gastos
from src.funcionalidades import ler_gastos_csv, adicionar_gasto_csv

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Início"})

@app.get("/gastos", response_class=HTMLResponse)
async def mostrar_gastos(request: Request):
    lista_gastos = ler_gastos_csv()
    return templates.TemplateResponse("gastos.html", {
        "request": request,
        "gastos": lista_gastos
    })

@app.post("/gastos/adicionar")
async def adicionar_gasto(
    request: Request,
    dono: str = Form(...),
    cartao: str = Form(...),
    vigencia: str = Form(...),
    valor: float = Form(...)
):
    novo_gasto = Gastos(
        dono=dono, 
        cartao=cartao, 
        vigencia=vigencia, 
        valor=valor
    )
    adicionar_gasto_csv(novo_gasto)
    return RedirectResponse(url="/gastos", status_code=303)

@app.get("/sobre", response_class=HTMLResponse)
async def sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request, "title": "Sobre"})
