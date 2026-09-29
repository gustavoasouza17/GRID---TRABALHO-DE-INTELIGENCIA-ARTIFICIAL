import sys
import os

# A pasta Algorithms contem o codigo original fornecido. Nao e modificado.
ALG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Algorithms")
if os.path.isdir(ALG_DIR):
    sys.path.insert(0, ALG_DIR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Tuple

from buscaNP import buscaNP
from BuscaP import buscaP

app = FastAPI(title="Labirinto IA - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResolverRequest(BaseModel):
    origem: str
    destino: str
    metodo: str
    grid: List[List[int]]


# ---------------------------------------------------------------------------
# TRADUCAO DE FORMATO
# A interface usa 1 = parede. O codigo do professor usa 9 = parede.
# Estas duas funcoes sao a unica ponte entre os dois formatos.
# ---------------------------------------------------------------------------

def frontend_grid_to_backend(grid: List[List[int]]) -> List[List[int]]:
    return [[9 if cell == 1 else 0 for cell in row] for row in grid]


def backend_grid_to_frontend(
    backend_map: List[List[int]],
    caminho: Optional[List[Tuple[int, int]]],
    origem: Tuple[int, int],
    destino: Tuple[int, int],
) -> List[List[int]]:
    path_set = set()
    if caminho:
        for pos in caminho:
            path_set.add((pos[0], pos[1]))

    frontend_grid = []
    for i, row in enumerate(backend_map):
        frontend_row = []
        for j, cell in enumerate(row):
            if (i, j) == origem:
                frontend_row.append(2)
            elif (i, j) == destino:
                frontend_row.append(3)
            elif (i, j) in path_set:
                frontend_row.append(4)
            elif cell == 9:
                frontend_row.append(1)
            else:
                frontend_row.append(0)
        frontend_grid.append(frontend_row)
    return frontend_grid


def parse_coord(coord_str: str) -> Tuple[int, int]:
    parts = coord_str.replace(" ", "").split(",")
    if len(parts) < 2:
        raise ValueError("Coordenada invalida. Use o formato X,Y (exemplo: 0,0)")
    return (int(parts[0]), int(parts[1]))


def validate_coord(coord: Tuple[int, int], nx: int, ny: int, mapa: List[List[int]]):
    """O codigo do professor valida a origem e o destino antes de buscar."""
    x, y = coord
    if not (0 <= x < nx and 0 <= y < ny):
        raise ValueError(f"Coordenada ({x},{y}) fora do grid {nx}x{ny}")
    if mapa[x][y] != 0:
        raise ValueError(f"Coordenada ({x},{y}) e uma parede. Escolha uma celula livre.")


# ---------------------------------------------------------------------------
# SELECTOR DE METODOS
# Traduz a sigla do frontend para a chamada correspondente no codigo do
# professor. A logica dos algoritmos NAO e alterada.
# ---------------------------------------------------------------------------

def executar_busca(metodo: str, origem: Tuple[int, int], destino: Tuple[int, int],
                   nx: int, ny: int, backend_map: List[List[int]]):
    caminho = None
    custo = 0

    if metodo == "BFS":
        caminho = buscaNP().amplitude_grid(origem, destino, nx, ny, backend_map)
    elif metodo == "DFS":
        caminho = buscaNP().profundidade_grid(origem, destino, nx, ny, backend_map)
    elif metodo == "PROF_LIMITADA":
        caminho = buscaNP().prof_limitada_grid(origem, destino, nx, ny, backend_map, 3)
    elif metodo == "APROF_ITERATIVO":
        caminho = buscaNP().aprof_iterativo_grid(origem, destino, nx, ny, backend_map, nx + ny)
    elif metodo == "BIDIRECIONAL":
        caminho = buscaNP().bidirecional_grid(origem, destino, nx, ny, backend_map)
    elif metodo == "CUSTO_UNIFORME":
        resultado = buscaP().custo_uniforme_grid(origem, destino, backend_map, nx, ny)
        if resultado is not None:
            caminho, custo = resultado
    elif metodo == "GREEDY":
        resultado = buscaP().greedy_grid(origem, destino, backend_map, nx, ny)
        if resultado is not None:
            caminho, custo = resultado
    elif metodo == "ASTAR":
        resultado = buscaP().a_estrela_grid(origem, destino, backend_map, nx, ny)
        if resultado is not None:
            caminho, custo = resultado
    elif metodo == "AIA_ESTRELA":
        resultado = buscaP().aia_estrela_grid(origem, destino, backend_map, nx, ny)
        if resultado is not None:
            caminho, custo = resultado
    else:
        raise ValueError(f"Metodo desconhecido: {metodo}")

    return caminho, custo


# ---------------------------------------------------------------------------
# ENDPOINT
# ---------------------------------------------------------------------------

@app.post("/resolver")
def resolver(request: ResolverRequest):
    if not request.grid or not request.grid[0]:
        return {"caminho": "Grid vazio", "grid": request.grid}

    nx = len(request.grid)
    ny = len(request.grid[0])

    try:
        origem = parse_coord(request.origem)
        destino = parse_coord(request.destino)
    except ValueError as e:
        return {"caminho": f"Erro: {e}", "grid": request.grid}

    backend_map = frontend_grid_to_backend(request.grid)

    # Mesma validacao usada nos scripts de consola do professor.
    try:
        validate_coord(origem, nx, ny, backend_map)
        validate_coord(destino, nx, ny, backend_map)
    except ValueError as e:
        return {"caminho": f"Erro: {e}", "grid": request.grid}

    try:
        caminho, custo = executar_busca(request.metodo, origem, destino, nx, ny, backend_map)
    except ValueError as e:
        return {"caminho": f"Erro: {e}", "grid": request.grid}

    if caminho is None:
        grid_frontend = backend_grid_to_frontend(backend_map, None, origem, destino)
        return {"caminho": "Caminho nao encontrado", "grid": grid_frontend}

    grid_frontend = backend_grid_to_frontend(backend_map, caminho, origem, destino)
    caminho_str = " -> ".join([f"({x},{y})" for x, y in caminho])

    return {
        "caminho": f"{caminho_str} | Custo: {custo} | Nos: {len(caminho)}",
        "grid": grid_frontend,
    }


@app.get("/")
def root():
    return {
        "status": "Labirinto IA API",
        "metodos": [
            "BFS", "DFS", "PROF_LIMITADA", "APROF_ITERATIVO", "BIDIRECIONAL",
            "CUSTO_UNIFORME", "GREEDY", "ASTAR", "AIA_ESTRELA",
        ],
        "endpoints": ["/resolver (POST)"],
    }
