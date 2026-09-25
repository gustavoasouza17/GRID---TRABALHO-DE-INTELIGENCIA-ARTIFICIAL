import json
import urllib.request

grid = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,1,1,0,0,0],
    [0,0,0,1,0,1,0,0,0,0],
    [0,1,0,0,0,1,0,0,0,0],
    [0,1,0,0,0,1,0,0,0,0],
    [0,0,0,1,0,1,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0],
    [1,0,1,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
]

metodos = ["BFS", "DFS", "PROF_LIMITADA", "APROF_ITERATIVO", "BIDIRECIONAL",
           "CUSTO_UNIFORME", "GREEDY", "ASTAR", "AIA_ESTRELA"]

for method in metodos:
    body = {"origem": "0,0", "destino": "7,9", "metodo": method, "grid": grid}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:8000/resolver",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"{method}: {result['caminho'][:80]}...")
    except Exception as e:
        print(f"{method}: Erro - {e}")