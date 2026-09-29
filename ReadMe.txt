# Labirinto IA — Resolução de Labirintos com Algoritmos de Busca

Projeto de Inteligência Artificial com interface gráfica web (React + Tailwind) e API
(FastAPI) que executa 9 algoritmos de busca em grid sobre uma matriz 10x10.

Os algoritmos em `BACKEND/Programas-20260922/` são o código original fornecido,
preservado sem alterações de lógica (apenas removidas as partes de grafo, mantendo grid).

================================================================================
1. ESTRUTURA DE FICHEIROS
================================================================================

TRABALHO INTELIGENCIA ARTIFICIAL/
|
|-- ReadMe.txt                         Este ficheiro (instruções completas)
|
|-- BACKEND/
|   |-- main.py                        SERVIDOR — cria a API e o endpoint /resolver
|   |-- requirements.txt               Lista de bibliotecas Python a instalar
|   |-- test_api.py                    Script de teste dos 9 algoritmos
|   |-- README.md                      Documentação resumida do backend
|   |-- venv/                          Ambiente virtual Python (já criado)
|   |
|   `-- Programas-20260922/            CÓDIGO ORIGINAL DO PROFESSOR
|       |-- buscaNP.py                 Algoritmos SEM pesos (grid)
|       |-- BuscaP.py                  Algoritmos COM pesos (grid)
|       |-- Node.py                    Classe Node (árvore de busca sem pesos)
|       |-- NodeP.py                   Classe NodeP (herda de Node, com v2/custo)
|       |-- utils.py                   Leitura de mapas e impressão de caminhos
|       |-- mapa3.txt                  Mapa de exemplo (formato CSV)
|       |-- principalBuscaSemPesos.py  Script de consola (algoritmos sem pesos)
|       `-- principalBuscaComPesos.py  Script de consola (algoritmos com pesos)
|
`-- FRONT-END/
    |-- src/
    |   |-- App.tsx                    INTERFACE — painel de controlo + grid 10x10
    |   |-- main.tsx                   Ponto de entrada React
    |   `-- index.css                  Importa o Tailwind
    |-- index.html                     Estrutura HTML base
    |-- package.json                   Dependências e scripts npm
    |-- vite.config.ts                 Configuração do Vite
    |-- tailwind.config.js             Configuração do Tailwind
    |-- postcss.config.js              Configuração do PostCSS
    |-- tsconfig.json                  Configuração TypeScript
    `-- tsconfig.node.json             Configuração TypeScript (build)


================================================================================
2. O QUE É CADA FICHEIRO DO BACK-END (explicação detalhada)
================================================================================

--------------------------------------------------------------------------------
2.1 BACKEND/main.py  —  O SERVIDOR (ficheiro que criei, NÃO é do professor)
--------------------------------------------------------------------------------
Este é o ficheiro que transforma o código do professor numa API web.

  Linha 4:  sys.path.insert(...)
      Acrescenta a pasta Programas-20260922 ao caminho de pesquisa do Python,
      para que "import buscaNP" funcione mesmo com o ficheiro noutra pasta.

  Linha 11-12:  from buscaNP import buscaNP / from BuscaP import buscaP
      Carrega o código original do professor.

  Linha 16-21:  CORSMiddleware
      Permite que o frontend (http://localhost:5173) possa fazer pedidos ao
      backend (http://localhost:8000). Sem isto, o navegador bloqueia.

  Linha 24-28:  class ResolverRequest(BaseModel)
      Define o formato do JSON que o frontend envia. Valida automaticamente.

  Linha 31-41:  frontend_grid_to_backend()
      TRADUÇÃO DE FORMATO. O frontend usa 1 = parede, mas o código do professor
      usa 9 = parede (porque 0 = livre e o resto é obstáculo). Esta função converte
      1 -> 9 e 0 -> 0. É a única "ponte" entre os dois formatos.

  Linha 44-70:  backend_grid_to_frontend()
      TRADUÇÃO INVERSA. Recebe o mapa do professor (0=livre, 9=parede) e o caminho
      encontrado, e devolve o formato do frontend: 0=livre, 1=parede,
      2=origem, 3=destino, 4=caminho percorrido.

  Linha 78-135:  executar_busca()
      SELECTOR DE MÉTODOS. Traduz a sigla enviada pelo frontend para a chamada
      correta do código do professor. Ex: "BFS" chama amplitude_grid(),
      "AIA_ESTRELA" chama aia_estrela_grid(). A lógica dos algoritmos NÃO é tocada.

  Linha 138-155:  @app.post("/resolver")
      O ENDPOINT. Recebe origem, destino, método e grid; chama executar_busca();
      devolve o caminho em texto e o grid já pintado.

  Linha 158-159:  @app.get("/")
      Endpoint de diagnóstico. Abrir http://localhost:8000 no navegador deve
      mostrar o estado da API. Útil para confirmar que o servidor está vivo.

--------------------------------------------------------------------------------
2.2 Programas-20260922/buscaNP.py  —  CÓDIGO DO PROFESSOR (sem pesos)
--------------------------------------------------------------------------------
Contém 5 algoritmos que tratam todas as transições como tendo o mesmo peso:

  sucessores_grid()        Devolve os 4 vizinhos válidos (cima, baixo, esq, dir)
                           de uma célula, ignorando paredes.
  exibirCaminho()          Percorre a árvore de busca de trás para frente para
                           extrair a sequência de nós do caminho encontrado.
  amplitude_grid()         BFS — usa FILA. Garante o caminho mais curto em número
                           de nós. É o método "BFS" da interface.
  profundidade_grid()      DFS — usa PILHA. Vai o mais fundo possível antes de
                           recuar. É o método "DFS" da interface.
  prof_limitada_grid()     DFS com limite de profundidade. A interface usa
                           limite = 3 (valor fixo, igual ao script do professor).
  aprof_iterativo_grid()   Executa a prof_limitada com limites crescentes
                           (1, 2, 3, ...). O limite máximo é dx+dy.
  bidirecional_grid()      Duas filas: uma parte da origem, outra do destino.
                           Quando as duas se cruzam, junta os dois caminhos.

--------------------------------------------------------------------------------
2.3 Programas-20260922/BuscaP.py  —  CÓDIGO DO PROFESSOR (com pesos)
--------------------------------------------------------------------------------
Contém 4 algoritmos que pesam cada movimento:

  sucessores_grid()        Devolve os vizinhos com o custo de ir para cada um:
                           Direita = 3, Esquerda = 6, Cima = 3, Baixo = 1.
                           (Célula (0,0) é a linha 0, coluna 0 = canto superior.)
  inserir_ordenado()       Insere um nó na lista por ordem crescente de prioridade.
  heuristica_grid()        Distância Manhattan: |x1-x2| + |y1-y2|.
  custo_uniforme_grid()    Expande sempre o nó mais barato (como Dijkstra).
                           É o método "CUSTO_UNIFORME" da interface.
  greedy_grid()            Escolhe o vizinho mais próximo do destino pela
                           heurística, ignorando o custo já acumulado.
                           É o método "GREEDY" da interface.
  a_estrela_grid()         f(n) = custo acumulado + heurística. Equilibra
                           exploited/explored. É o método "ASTAR" da interface.
  aia_estrela_grid()       A* com corte iterativo. Começa com um limite de
                           heurística e só aceita nós cujo f fique abaixo dele.
                           Quando esgota, aumenta o limite pela média dos f
                           rejeitados e recomeça. É "AIA_ESTRELA" da interface.

--------------------------------------------------------------------------------
2.4 Programas-20260922/Node.py e NodeP.py  —  CÓDIGO DO PROFESSOR
--------------------------------------------------------------------------------
  Node.py    Define um nó da árvore de busca: pai, estado (tupla x,y), v1
             (profundidade), anterior e proximo.
  NodeP.py   Herda de Node e acrescenta v2 (custo acumulado). É usada por
             BuscaP.py, que precisa de comparar custos.

--------------------------------------------------------------------------------
2.5 Programas-20260922/utils.py  —  CÓDIGO DO PROFESSOR
--------------------------------------------------------------------------------
  Gera_Problema_Grid_Fixo(arquivo)   Lê mapa3.txt (linhas CSV) e devolve a
                                     matriz, o número de linhas e de colunas.
  Gera_Problema_Grid_Ale(nx,ny,qtd) Gera grid aleatório com qtd obstáculos.
  imprimeCaminho(texto,...)          Imprime o caminho na consola.

  Nota: as funções com sufixo _P são idênticas às principais, mantidas como
  estavam no código original.

--------------------------------------------------------------------------------
2.6 Programas-20260922/principalBusca*.py  —  CÓDIGO DO PROFESSOR
--------------------------------------------------------------------------------
Scripts de consola (linha de comandos) que o professor usava para testar.
Foram adaptados para trabalhar apenas com GRID (a opção GRAFO foi removida,
porque o nosso projeto usa exclusivamente grid).

  principalBuscaSemPesos.py  Menu: executa amplitude, profundidade, limitada,
                             aprofundamento iterativo e bidirecional de uma vez.
  principalBuscaComPesos.py  Executa custo uniforme, greedy, A* e AIA* de uma vez.

  NOTA IMPORTANTE: estes dois ficheiros NÃO são usados pela aplicação web.
  São para teste directo no terminal. A aplicação web chama os algoritmos
  directamente através do main.py.


================================================================================
3. O QUE ESTAVA A CAUSAR O ERRO DE CONEXÃO
================================================================================

O frontend mostrava "Erro ao conectar ao servidor" porque o backend NÃO ESTAVA
A CORRER. Não era bug no código — o servidor tem de ser iniciado manualmente
antes de usar a interface. O erro acontece sempre nestas situações:

  1. O terminal do backend foi fechado.
  2. O uvicorn foi iniciado e a sessão/terminal que o launched terminou.
  3. O backend está a correr numa porta diferente (a interface espera a 8000).

Confirmação rápida: abrir http://localhost:8000 no navegador. Se aparecer
  {"status":"Labirinto IA API","endpoints":["/resolver (POST)"]}
o backend está vivo. Se aparecer "This site can't be reached", está parado.


================================================================================
4. BIBLIOTECAS E SOFTWARE A INSTALAR
================================================================================

--------------------------------------------------------------------------------
4.1 BACKEND (Python 3.13+)
--------------------------------------------------------------------------------
Verificar se tem Python instalado:
    python --version

Instalar as bibliotecas (dentro da pasta BACKEND):
    pip install -r requirements.txt

O requirements.txt contém:
    fastapi==0.141.1    Framework web que cria a API e valida os dados
                        recebidos. Define a rota /resolver.
    uvicorn==0.53.0     Servidor ASGI que executa a aplicação FastAPI.
                        É o que fica "a ouvir" na porta 8000.
    numpy==2.5.3       Usado em utils.py para gerar grids aleatórios.
                        (O grid da interface não precisa, mas o código do
                        professor importa numpy no topo do ficheiro.)

Nota sobre o ambiente virtual (venv): a pasta BACKEND/venv já existe e já tem
estas bibliotecas instaladas. Para usar, basta chamar os executáveis lá dentro.

--------------------------------------------------------------------------------
4.2 FRONT-END (Node.js 18 ou superior)
--------------------------------------------------------------------------------
Verificar se tem Node.js instalado:
    node --version

Instalar as dependências (dentro da pasta FRONT-END):
    npm install

O package.json contém:
    react@18.3.1            Biblioteca de interface (componentes, estados).
    react-dom@18.3.1       Renderiza o React no navegador.
    typescript@5.7.2       Verifica os tipos do código, evita erros.
    vite@6.0.3             Servidor de desenvolvimento rápido + empacotador.
    @vitejs/plugin-react   Integra React com Vite.
    tailwindcss@3.4.17     Framework CSS (usado para todo o visual).
    postcss@8.4.49         Processa o CSS do Tailwind.
    autoprefixer@10.4.20   Adiciona prefixos de vendor ao CSS.
    @types/react           Tipos do React para o TypeScript.


================================================================================
5. COMO EXECUTAR O PROGRAMA
================================================================================

São necessários DOIS terminais abertos ao mesmo tempo.

--------------------------------------------------------------------------------
TERMINAL 1 — BACKEND (tem de ser iniciado primeiro)
--------------------------------------------------------------------------------
Abrir a pasta BACKEND na pasta do projecto e executar:

    cd "C:\Users\Gustavo\Desktop\TRABALHO INTELIGENCIA ARTIFICIAL\BACKEND"
    & "venv\Scripts\uvicorn.exe" main:app --host 127.0.0.1 --port 8000

Deve aparecer no terminal:
    INFO:     Uvicorn running on http://127.0.0.1:8000

Deixar este TERMINAL ABERTO enquanto usar a interface. Se o fechar, o backend
para e a interface volta a mostrar o erro de conexão.

Alternativa usando o Python do venv:
    & "venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000

Verificar que está a funcionar: abrir http://localhost:8000 no navegador.

--------------------------------------------------------------------------------
TERMINAL 2 — FRONTEND
--------------------------------------------------------------------------------
    cd "C:\Users\Gustavo\Desktop\TRABALHO INTELIGENCIA ARTIFICIAL\FRONT-END"
    npm run dev

Deve aparecer:
    Local:   http://localhost:5173/

Abrir esse endereço no navegador.


================================================================================
6. FUNCIONAMENTO DA INTERFACE GRÁFICA
================================================================================

A janela ocupa 100% do ecrã (100vh) e divide-se em duas secções.

--------------------------------------------------------------------------------
6.1 PAINEL DE CONTROLO — barra lateral esquerda (30% da largura)
--------------------------------------------------------------------------------
Fundo cinzento-claro. De cima para baixo:

  "Configuração do Labirinto"   Título.

  ORIGEM (X,Y)                  Campo de texto. Escrever a coordenada da célula
                                inicial, formato "0,0" (sem espaços). A célula
                                fica verde no grid depois de executar.

  DESTINO (X,Y)                 Campo de texto. Mesmo formato. A célula fica
                                vermelha.

  MÉTODO                        Lista com 9 algoritmos:
                                  Busca em Largura (BFS)
                                  Busca em Profundidade (DFS)
                                  Profundidade Limitada
                                  Aprofundamento Iterativo
                                  Busca Bidirecional
                                  Custo Uniforme
                                  Greedy
                                  A* (A-Star)
                                  AIA-Estrela

  EXECUTAR                      Botão azul. Envia o pedido ao backend.

  REINICIAR GRID                Botão branco. Limpa o grid e o caminho.

  CAMINHO                       Área de texto onde aparece o resultado, por
                                exemplo:
                                (0,0) -> (0,1) -> (0,2) ... | Custo: 34 | Nós: 17

  LEGENDA                        Mostra o significado de cada cor.

--------------------------------------------------------------------------------
6.2 LABIRINTO — área principal direita (70% da largura)
--------------------------------------------------------------------------------
Grid de 10 linhas x 10 colunas, centrado na tela. Cada célula é um quadrado
com contorno cinzento.

  Cores de cada célula:
    Branco  = célula livre (passável)
    Preto   = parede / obstáculo
    Verde   = origem
    Vermelho= destino
    Azul    = caminho percorrido pelo algoritmo

  COMO DESENHAR O LABIRINTO: clicar numa célula alterna entre livre (branco)
  e parede (preto). Clicar outra vez volta a ficar livre. As paredes são as
  únicas coisas que bloqueiam a passagem.

  A_origem e o destino são definidos pelos campos de texto, não clicando.
  Por isso, evite clicar na célula que digitou como origem/destino, senão
  transforma-a em parede e o caminho deixa de existir.

--------------------------------------------------------------------------------
6.3 O QUE ACONTECE QUANDO CLICA EM "EXECUTAR" (fluxo completo)
--------------------------------------------------------------------------------
  1. O frontend junta origem, destino, método e o estado atual do grid num
     objeto JSON e envia um POST para:
         http://localhost:8000/resolver

  2. O backend (main.py) recebe o pedido e traduz o grid: converte cada 1
     (parede no frontend) em 9 (parede no código do professor).

  3. Chama a função do algoritmo escolhido, que é o código ORIGINAL do
     professor, sem alterações.

  4. O algoritmo percorre o grid a partir da origem, seguindo osvizinhos
     livres, até encontrar o destino (ou desistir).

  5. O backend recebe a lista de nós do caminho e reconstrói o grid no
     formato do frontend, pintando de azul as células do caminho.

  6. O frontend recebe a resposta e actualiza o ecrã:
     - o grid passa a mostrar o caminho pintado a azul;
     - a área "Caminho" mostra a sequência de coordenadas, o custo e o
       número de nós.


================================================================================
7. OS 9 MÉTODOS DISPONÍVEIS
================================================================================

Métodos SEM pesos (ficheiro buscaNP.py — herdam de Node):
  BFS   "Busca em Largura (BFS)"      amplitude_grid()
        Usa fila. Devolve o caminho com MENOS NÓS. É o mais previsível.

  DFS   "Busca em Profundidade (DFS)" profundidade_grid()
        Usa pilha. Mergulha fundo antes de recuar. Pode dar caminhos longos
        ou estranhos, porque não tem critério de escolha.

  PROF_LIMITADA  "Profundidade Limitada"   prof_limitada_grid()
        DFS que só desce até um limite fixo de 3 níveis. Como está codificado
        com limite 3 (igual ao script do professor), raramente encontra
        caminhos em labirintos maiores. É o comportamento esperado, não um erro.

  APROF_ITERATIVO  "Aprofundamento Iterativo"   aprof_iterativo_grid()
        Repete a Profundidade Limitada com limites crescentes (1, 2, 3...)
        até encontrar o caminho. Equivale à busca em profundidade completa.

  BIDIRECIONAL  "Busca Bidirecional"   bidirecional_grid()
        Lança duas buscas em simultâneo, uma da origem e outra do destino.
        Junta os dois percursos quando se cruzam. Normalmente mais rápido.

Métodos COM pesos (ficheiro BuscaP.py — herdam de NodeP):
  CUSTO_UNIFORME  "Custo Uniforme"   custo_uniforme_grid()
        Como o Dijkstra: expande sempre a célula mais barata. Garante o
        caminho mais barato, mas pode demorar mais a explorar.

  GREEDY  "Greedy"   greedy_grid()
        Escolhe a célula mais próxima do destino (distância Manhattan),
        ignorando o custo já acumulado. Rápido, mas podechoquear becos sem
        saída.

  ASTAR  "A* (A-Star)"   a_estrela_grid()
        Soma o custo já pago com a distância estimada ao destino. É o
        equilíbrio entre Custo Uniforme e Greedy; normalmente o melhor
        equilíbrio entre qualidade e velocidade.

  AIA_ESTRELA  "AIA-Estrela"   aia_estrela_grid()
        Versão do A* que primeiro aceita só os nós com f baixo (corte),
        vamos relaxando esse corte quando a busca esgota. Menos memória
        que o A*, com resultados praticamente iguais.


================================================================================
8. FORMATO DA COMUNICAÇÃO (resumo técnico)
================================================================================

PEDIDO (frontend -> backend), POST http://localhost:8000/resolver
{
    "origem":  "0,0",
    "destino": "9,9",
    "metodo":  "BFS",
    "grid":    [[0,0,0,...], [ ... ], ...]     10 linhas x 10 colunas
}

RESPOSTA (backend -> frontend)
{
    "caminho": "(0,0) -> (0,1) -> ... | Custo: X | Nós: Y",
    "grid":    [[0,0,0,...], [ ... ], ...]     10 linhas x 10 colunas
}

Códigos de célula usados na comunicação:
    0  = livre
    1  = parede            (o backend converte para 9 internamente)
    2  = origem            (verde)
    3  = destino           (vermelho)
    4  = caminho           (azul)


================================================================================
9. RESOLUÇÃO DE PROBLEMAS
================================================================================

SINTOMA: "Erro ao conectar ao servidor"
CAUSA:   O backend não está a correr.
SOLUÇÃO: Abrir o Terminal 1 e iniciar o uvicorn (ver secção 5). Confirmar com
         http://localhost:8000 no navegador.

SINTOMA: "Caminho não encontrado"
CAUSA:   Não existe percurso entre origem e destino. Ou uma das células
         destino/origem foi transformada em parede ao clicar.
SOLUÇÃO: Confirmar que origem e destino não são paredes. Se o destino é
         inacessível por completo, o algoritmo desiste — o frontend mostra o
         aviso mas devolve o grid intacto.

SINTOMA: O método Profundidade Limitada quase nunca encontra caminho
CAUSA:   O limite está fixo em 3 (como no código original do professor). Só
         encontra destinos a 3 níveis ou menos.
SOLUÇÃO: Comportamento esperado. Usar Aprofundamento Iterativo ou A* para
         percursos mais longos.

SINTOMA: Porta 8000 já em uso
CAUSA:   Já existe outro uvicorn a correr.
SOLUÇÃO: Fechar o terminal antigo, ou usar outra porta e ajustar o endereço
         em App.tsx.

SINTOMA: npm install falha / comando não reconhecido
CAUSA:   Node.js não está instalado.
SOLUÇÃO: Instalar Node.js 18+ de https://nodejs.org e reiniciar o terminal.

SINTOMA: pip não reconhecido
CAUSA:   Python não está no PATH.
SOLUÇÃO: Usar sempre o executável do venv:
         & "BACKEND\venv\Scripts\pip.exe" install -r requirements.txt
