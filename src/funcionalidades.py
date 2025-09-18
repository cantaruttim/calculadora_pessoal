import csv
from models.Gastos import Gastos
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "gastos.csv"


def limpar_valor(valor_str: str) -> float:
    valor_str = valor_str.replace("R$", "").replace(" ", "").strip()
    valor_str = valor_str.replace(".", "")  # remove pontos de milhar
    valor_str = valor_str.replace(",", ".") # transforma vírgula em ponto decimal
    try:
        return float(valor_str)
    except ValueError:
        return 0.0

def ler_gastos_csv():
    lista_gastos = []
    if CSV_PATH.exists():
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lista_gastos.append(Gastos(
                    dono=row['Dono'],
                    cartao=row['Cartão'],
                    vigencia=row['Vigência'],
                    valor=limpar_valor(row['Valor'])
                ))
    return lista_gastos


def adicionar_gasto_csv(gasto: Gastos):
    file_exists = CSV_PATH.exists()

    valor_limpo = limpar_valor(str(gasto.valor))
    valor_formatado = f"{valor_limpo:.2f}" 

    # Garante quebra de linha ao final do arquivo, se necessário
    if file_exists:
        with open(CSV_PATH, 'rb+') as f:
            f.seek(-1, 2)
            last_char = f.read(1)
            if last_char != b'\n':
                f.write(b'\n')
    with open(CSV_PATH, 'a', encoding='utf-8') as csvfile:
        fieldnames = ['Dono', 'Cartão', 'Vigência', 'Valor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'Dono': gasto.dono,
            'Cartão': gasto.cartao,
            'Vigência': gasto.vigencia,
            'Valor': valor_formatado
        })