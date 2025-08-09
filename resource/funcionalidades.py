import csv
from models.Gastos import Gastos
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

def ler_gastos_csv():
    lista_gastos = []
    if CSV_PATH.exists():
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lista_gastos.append(Gastos(
                    dono=row['dono'],
                    cartao=row['cartao'],
                    vigencia=row['vigencia'],
                    valor=float(row['valor'])
                ))
    return lista_gastos


def adicionar_gasto_csv(gasto: Gastos):
    file_exists = CSV_PATH.exists()
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['dono', 'cartao', 'vigencia', 'valor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'dono': gasto.dono,
            'cartao': gasto.cartao,
            'vigencia': gasto.vigencia,
            'valor': gasto.valor
        })