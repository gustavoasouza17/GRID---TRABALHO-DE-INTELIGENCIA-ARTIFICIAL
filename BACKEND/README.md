# Backend — Labirinto IA

API FastAPI que expõe os algoritmos de busca em grid à interface web.

Documentação completa em `../ReadMe.txt`.

## Porta

O servidor usa a porta **8001**.

## Requisitos

- Python 3.13+
- numpy, fastapi, uvicorn (instalar via `pip install -r requirements.txt`)

## Como executar

```bash
cd BACKEND
& "venv\Scripts\uvicorn.exe" main:app --host 127.0.0.1 --port 8001
```

Ou usando o Python do venv:
```bash
& "venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8001
```

Confirmar que está a correr: abrir `http://localhost:8001` no navegador.

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
- `metodo`: sigla do algoritmo (ver tabela abaixo)
- `grid`: array 10x10 — 0=livre, 1=parede

**Resposta:**
```json
{
  "caminho": "(0,0) -> (0,1) -> ... | Custo: X | Nos: Y",
  "grid": [[0,0,...], ...]
}
```

**Métodos aceites:**

| Sigla | Algoritmo | Classe | Ficheiro |
|---|---|---|---|
| `BFS` | Busca em Largura | `buscaNP` | `buscaNP.py` |
| `DFS` | Busca em Profundidade | `buscaNP` | `buscaNP.py` |
| `PROF_LIMITADA` | Profundidade Limitada | `buscaNP` | `buscaNP.py` |
| `APROF_ITERATIVO` | Aprofundamento Iterativo | `buscaNP` | `buscaNP.py` |
| `BIDIRECIONAL` | Busca Bidirecional | `buscaNP` | `buscaNP.py` |
| `CUSTO_UNIFORME` | Custo Uniforme | `buscaP` | `BuscaP.py` |
| `GREEDY` | Greedy | `buscaP` | `BuscaP.py` |
| `ASTAR` | A* (A-Star) | `buscaP` | `BuscaP.py` |
| `AIA_ESTRELA` | AIA-Estrela | `buscaP` | `BuscaP.py` |

### GET /

Diagnóstico. Confirma que a API está viva e lista os métodos disponíveis.

## Estrutura

Ficheiros de código original (não modificados):
- `buscaNP.py` — algoritmos sem pesos
- `BuscaP.py` — algoritmos com pesos
- `Node.py`, `NodeP.py` — classes de nós
- `utils.py` — utilitários
- `principalBuscaSemPesos.py`, `principalBuscaComPesos.py` — scripts de consola

Ficheiro do projecto:
- `main.py` — API FastAPI que liga o código original à interface
- `test_api.py` — script de teste dos 9 métodos
