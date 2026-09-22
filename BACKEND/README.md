# Backend - Labirinto IA

API FastAPI para resolução de labirintos usando algoritmos de busca em grid.

## Requisitos

- Python 3.13+
- numpy, fastapi, uvicorn (instalar via `pip install -r requirements.txt`)

## Como executar

```bash
cd BACKEND
& "BACKEND\venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Ou usar o venv existente:
```bash
& "BACKEND\venv\Scripts\uvicorn.exe" main:app --host 127.0.0.1 --port 8000
```

## Endpoints

### POST /resolver

Recebe configuração do labirinto e retorna o caminho encontrado.

**Body:**
```json
{
  "origem": "0,0",
  "destino": "9,9",
  "metodo": "BFS",
  "grid": [[0,0,...], ...]
}
```

**Campos:**
- `origem`: coordenada X,Y do nó inicial
- `destino`: coordenada X,Y do nó objetivo
- `metodo`: `"BFS"` (Largura), `"DFS"` (Profundidade), `"ASTAR"` (A-Star)
- `grid`: array 10x10 — 0=livre, 1=parede

**Resposta:**
```json
{
  "caminho": "(0,0) -> (0,1) -> ... | Custo: X | Nós: Y",
  "grid": [[0,0,...], ...]
}
```

## Estrutura

- `main.py` — API FastAPI
- `Programas-20260922/` — Código original de algoritmos de grid (sem modificações)
  - `buscaNP.py` — BFS, DFS, DFS limitada, IDA*, Bidirecional (grid)
  - `BuscaP.py` — Custo Uniforme, Greedy, A*, IDA* (grid)
  - `utils.py` — Utilidades de grid
  - `Node.py`, `NodeP.py` — Classes de nós
  - `mapa3.txt` — Mapa de exemplo (grid)
