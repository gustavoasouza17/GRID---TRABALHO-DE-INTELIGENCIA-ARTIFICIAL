import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Programas-20260922"))

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


def frontend_grid_to_backend(grid: List[List[int]]) -> List[List[int]]:
    backend_map = []
    for row in grid:
        backend_row = []
        for cell in row:
            if cell == 1:
                backend_row.append(9)
            else:
                backend_row.append(0)
        backend_map.append(backend_row)
    return backend_map


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
    parts = coord_str.split(",")
    return (int(parts[0]), int(parts[1]))


@app.post("/resolver")
def resolver(request: ResolverRequest):
    origem = parse_coord(request.origem)
    destino = parse_coord(request.destino)
    metodo = request.metodo

    nx = len(request.grid)
    ny = len(request.grid[0]) if nx > 0 else 0

    backend_map = frontend_grid_to_backend(request.grid)

    caminho = None
    custo = 0

    if metodo == "BFS":
        resultado = buscaNP().amplitude_grid(origem, destino, nx, ny, backend_map)
        if resultado is not None:
            caminho = resultado
    elif metodo == "DFS":
        resultado = buscaNP().profundidade_grid(origem, destino, nx, ny, backend_map)
        if resultado is not None:
            caminho = resultado
    elif metodo == "ASTAR":
        resultado = buscaP().a_estrela_grid(origem, destino, backend_map, nx, ny)
        if resultado is not None:
            caminho, custo = resultado
    else:
        return {"caminho": "Método desconhecido", "grid": request.grid}

    if caminho is None:
        grid_frontend = backend_grid_to_frontend(
            backend_map, None, origem, destino
        )
        return {"caminho": "Caminho não encontrado", "grid": grid_frontend}

    grid_frontend = backend_grid_to_frontend(
        backend_map, caminho, origem, destino
    )

    caminho_str = " -> ".join([f"({x},{y})" for x, y in caminho])

    return {
        "caminho": f"{caminho_str} | Custo: {custo} | Nós: {len(caminho)}",
        "grid": grid_frontend,
    }


@app.get("/")
def root():
    return {"status": "Labirinto IA API", "endpoints": ["/resolver (POST)"]}
