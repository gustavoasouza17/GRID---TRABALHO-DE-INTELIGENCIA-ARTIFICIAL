================================================================================
  LABIRINTO IA — INSTRUCOES DE EXECUCAO
  Resolucao de Labirintos com Algoritmos de Busca
================================================================================

Este documento explica apenas tres coisas:

  1. Que bibliotecas e software e preciso instalar
  2. Como executar o programa
  3. Como funciona a interface grafica

O programa tem duas partes que correm em separado:

  FRONT-END    React + TypeScript + Tailwind CSS     (a interface)
  BACK-END     FastAPI + Python                       (os algoritmos)

  ┌──────────────────┐         ┌──────────────────┐
  │  FRONT-END       │  -----> │  BACK-END        │
  │  interface       │  JSON   │  algoritmos      │
  │  porta 5173      │  <----- │  porta 8001      │
  └──────────────────┘         └──────────────────┘

A interface e onde o utilizador desenha o labirinto. O backend e onde os
algoritmos correm e calculam o caminho.


################################################################################
# 1. BIBLIOTECAS E SOFTWARE A INSTALAR
################################################################################

--------------------------------------------------------------------------------
1.1 SOFTWARE NECESSARIO
--------------------------------------------------------------------------------
    BACK-END     Python 3.13 ou superior
    FRONT-END    Node.js 18 ou superior

Verificar se ja estao instalados (abrir o PowerShell ou o terminal):

    python --version
    node --version

Se aparecer a versao, esta instalado. Se der erro "comando nao reconhecido",
e preciso instalar.

Instalar o Python:  https://www.python.org/downloads/
Instalar o Node.js: https://nodejs.org/


--------------------------------------------------------------------------------
1.2 BIBLIOTECAS DO BACK-END (Python)
--------------------------------------------------------------------------------
Instalar (dentro da pasta BACKEND):

    pip install -r requirements.txt

O ficheiro requirements.txt contem:

  fastapi        Cria a API. Define o endereco /resolver e valida
                 automaticamente os dados recebidos.
  uvicorn        Servidor que executa a aplicacao FastAPI. E o programa
                 que fica a escutar a porta 8001.
  numpy          Importado pelo codigo dos algoritmos (utils.py) para gerar
                 labirintos aleatorios.

--------------------------------------------------------------------------------
1.3 BIBLIOTECAS DO FRONT-END (Node.js)
--------------------------------------------------------------------------------
Instalar (dentro da pasta FRONT-END):

    npm install

O ficheiro package.json contem:

  react, react-dom    Biblioteca de interface. Permite construir o painel
                      de controlo e o desenho do labirinto.
  typescript          Verificacao de tipos. Evita erros no codigo.
  vite                Servidor de desenvolvimento e empacotador. E o que
                      serve a interface na porta 5173.
  tailwindcss         Framework de estilos. Define as cores, os tamanhos
                      e o aspecto visual de toda a interface.
  postcss             Processa o CSS gerado pelo Tailwind.
  autoprefixer        Adiciona prefixos de browser ao CSS.
  @types/react        Tipos do React para o TypeScript.


################################################################################
# 2. COMO EXECUTAR O PROGRAMA
################################################################################

Sao necessarios DOIS terminais abertos ao mesmo tempo. Um para cada parte.

--------------------------------------------------------------------------------
2.1 TERMINAL 1 — BACK-END
--------------------------------------------------------------------------------
    Exemplo: cd "C:\Users\Gustavo\Desktop\TRABALHO INTELIGENCIA ARTIFICIAL\BACKEND"
    & "venv\Scripts\uvicorn.exe" main:app --host 127.0.0.1 --port 8001

Alternativa, usando directamente o Python do ambiente virtual:

    & "venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8001

O que deve aparecer no terminal:

    INFO:     Uvicorn running on http://127.0.0.1:8001

IMPORTANTE: deixar este terminal ABERTO enquanto se usa o programa. Se o
fechar, o backend para e a interface mostra um erro de conexao.

--------------------------------------------------------------------------------
2.2 TERMINAL 2 — FRONT-END
--------------------------------------------------------------------------------
    Exemplo cd "C:\Users\Gustavo\Desktop\TRABALHO INTELIGENCIA ARTIFICIAL\FRONT-END"
    npm run dev

O que deve aparecer no terminal:

    Local:   http://localhost:5173/

--------------------------------------------------------------------------------
2.3 ABRIR NO NAVEGADOR
--------------------------------------------------------------------------------
    http://localhost:5173

A interface do programa aparece nessa pagina.


--------------------------------------------------------------------------------
2.4 CONFIRMAR QUE ESTA A FUNCIONAR
--------------------------------------------------------------------------------
    PASSO 1   Abrir http://localhost:8001 numa aba nova do navegador.
               Deve aparecer uma lista com os 9 metodos de busca.
               Se aparecer "site can't be reached", o backend nao esta
               a correr: voltar ao terminal 1.

    PASSO 2   Abrir http://localhost:5173.
               Deve aparecer a interface com o painel de controlo a
               esquerda e o labirinto a direita.

    PASSO 3   Na interface, escrever origem "0,0", destino "9,9",
               escolher o metodo BFS e clicar em Executar.
               Deve aparecer um caminho azul no labirinto.


--------------------------------------------------------------------------------
2.5 PORTAS
--------------------------------------------------------------------------------
    Frontend      5173    Servidor de desenvolvimento do Vite
    Backend       8001    Servidor FastAPI

    O backend tem de ser arrancado SEMPRE primeiro, porque a interface
    precisa dele para calcular os caminhos.

    Se a porta 8001 ja estiver ocupada, significa que ja existe um servidor
    a correr. Fechar o terminal antigo antes de arrancar outro.

    Se alguma vez mudar a porta do backend, tem de actualizar a interface
    em dois sitios do ficheiro FRONT-END/src/App.tsx (a linha do "fetch" e
    a linha da mensagem de erro), para ambas apontarem para a porta nova.


################################################################################
# 3. FUNCIONAMENTO DA INTERFACE GRAFICA
################################################################################

--------------------------------------------------------------------------------
3.1 COMO ESTA ORGANIZADO O ECRÃ
--------------------------------------------------------------------------------
A janela ocupa o ecrã inteiro (100% da altura) e divide-se em duas areas:

    ┌───────────────────┬────────────────────────────────┐
    │                   │                                │
    │  PAINEL DE        │       O LABIRINTO              │
    │  CONTROLO         │                                │
    │  (30% largura)    │       (70% largura)            │
    │                   │                                │
    │  cinzento-claro   │       grid 10x10 centrado      │
    │                   │                                │
    └───────────────────┴────────────────────────────────┘

O painel de controlo e onde se configura a busca. O labirinto e onde se
desenha o mapa e se ve o resultado.


--------------------------------------------------------------------------------
3.2 O PAINEL DE CONTROLO (lado esquerdo)
--------------------------------------------------------------------------------
    ┌─────────────────────────────┐
    │ Configuração do Labirinto  │  Titulo
    ├─────────────────────────────┤
    │ ORIGEM (X,Y)                │  Campo de texto. De onde a busca
    │ [ 0,0                    ]  │  parte. A celula fica verde.
    │                             │
    │ DESTINO (X,Y)               │  Campo de texto. Para onde a busca
    │ [ 9,9                    ]  │  vai. A celula fica vermelha.
    │                             │
    │ METODO                      │  Lista desplegavel com os 9
    │ [ Busca em Largura (BFS) v] │  algoritmos de busca.
    │                             │
    │ [      EXECUTAR          ]  │  Botao azul. Calcula o caminho.
    │ [    Reiniciar Grid      ]  │  Botao branco. Limpa o labirinto.
    │                             │
    │ CAMINHO                     │  Mostra o resultado da ultima
    │ ┌─────────────────────────┐ │  execucao: as coordenadas
    │ │ (0,0) -> (0,1) -> ...  │ │  percorridas, o custo e o numero
    │ └─────────────────────────┘ │  de nos.
    │                             │
    │ ■ Livre  ■ Parede  ■ Origem │  Legenda com o significado
    │ ■ Destino ■ Caminho         │  de cada cor.
    └─────────────────────────────┘

--------------------------------------------------------------------------------
3.3 O LABIRINTO (lado direito)
--------------------------------------------------------------------------------
Um GRID de 10 linhas por 10 colunas, centrada na area. Cada celula e um
quadrado com contorno cinzento.

    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
    │   │   │   │   │   │   │   │   │   │   │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
    │   │   │   │   │   │   │   │   │   │   │
    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
    │   │   │   │   │   │   │   │   │   │   │   10 linhas
    └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
      10 colunas

Cada celula pode ter uma de cinco cores:

    ┌─────────┐
    │         │  BRANCO     Celula livre. A busca pode passar.
    └─────────┘
    ┌─────────┐
    │█████████│  PRETO      Parede. Bloqueia a passagem.
    └─────────┘
    ┌─────────┐
    │ Início  │  VERDE      Celula de origem.
    └─────────┘
    ┌─────────┐
    │   Fim   │  VERMELHO   Celula de destino.
    └─────────┘
    ┌─────────┐
    │ Caminho │  AZUL       Celula por onde passou o caminho.
    └─────────┘

Ao desenhar uma parede, a celula fica preta. A origem e o destino ficam
vermelhos depois da execucao. Quando a busca corre, as celulas do caminho
ficam azuis.


--------------------------------------------------------------------------------
3.4 AS COORDENADAS
--------------------------------------------------------------------------------
Cada celula tem uma coordenada (X, Y), onde:

    X = linha    (de cima para baixo,  de 0 a 9)
    Y = coluna   (da esquerda para a direita, de 0 a 9)

    Y=0  Y=1  Y=2  Y=3  ...
  ┌────┬────┬────┬────┐
  │    │    │    │    │  X=0
  ├────┼────┼────┼────┤
  │    │    │    │    │  X=1
  ├────┼────┼────┼────┤
  │    │    │    │    │  X=2
  └────┴────┴────┴────┘

Assim, a coordenada (2,3) e a celula que esta na 3a linha (contando de cima
a partir de zero) e na 4a coluna (contando da esquerda a partir de zero).

Como a grelha e 10x10, o X e o Y vao sempre de 0 a 9. Coordenadas como "10,0"
ou "0,-1" sao invalidas.

Nas caixas de texto escreve-se "2,3" ou "2, 3" (sem aspas).


--------------------------------------------------------------------------------
3.5 COMO DESENHAR O LABIRINTO
--------------------------------------------------------------------------------
    Clicar numa celula alterna entre LIVRE e PAREDE:

        clicar 1a vez   ->  vira PARDE (preto)
        clicar 2a vez   ->  vira LIVRE (branco)

Todas as celulas comecam livres, por isso se nao clicar em nada, os algoritmos
encontram caminhos diretos em linha reta.

Para criar um labirinto de verdade, e preciso desenhar paredes que formem
becos sem saida e obriguem os algoritmos a escolher entre rotas alternativas.

--------------------------------------------------------------------------------
3.6 OS METODOS DE BUSCA DISPONIVEIS
--------------------------------------------------------------------------------
A lista "METODO" tem 9 algoritmos:

  Busca em Largura (BFS)      Procura por niveis. Devolve sempre o caminho
                              mais curto em numero de passos.

  Busca em Profundidade (DFS) Mergulha o mais fundo possivel antes de recuar.
                              Pode devolver caminhos mais longos.

  Profundidade Limitada       Como o DFS, mas so desce 3 niveis. So encontra
                              destinos a 3 passos ou menos da origem.

  Aprofundamento Iterativo     Repete a Profundidade Limitada com limites
                              crescentes (1, 2, 3...) ate encontrar o
                              caminho.

  Busca Bidirecional          Faz duas buscas ao mesmo tempo, uma a partir
                              da origem e outra do destino, e junta os
                              percursos quando se cruzam. E mais rapida.

  Custo Uniforme              Como o BFS, mas cada direccao tem um custo
                              diferente. Devolve o caminho mais barato.

  Greedy                      Escolhe sempre a celula mais proxima do destino.

  A* (A-Star)                Combina o custo ja percorrido com a distancia
                              estimada ate ao destino. E o melhor equilibrio
                              entre rapidez e qualidade.

  AIA-Estrela                 Como o A*, mas com memoria reduzida.

Os quatro primeiros (BFS, DFS, Profundidade Limitada, Aprofundamento
Iterativo, Bidirecional) tratam todos os movimentos como tendo o mesmo custo.
Os ultimos quatro (Custo Uniforme, Greedy, A*, AIA-Estrela) dao um custo
diferente a cada direccao.


--------------------------------------------------------------------------------
3.7 O QUE ACONTECE QUANDO SE CLICA EM "EXECUTAR" — PASSO A PASSO
--------------------------------------------------------------------------------

    PASSO 1 — A interface junta os dados e envia um pedido ao backend.

        POST http://localhost:8001/resolver
        {
            "origem":  "0,0",
            "destino": "9,9",
            "metodo":  "BFS",
            "grid":    [[0,0,0,0,0,0,0,0,0,0],
                        [ ...                            ],
                        ... 10 linhas com 10 colunas cada    ]
        }


    PASSO 2 — O backend traduz o formato do labirinto.

        A interface usa 1 para parede. O codigo dos algoritmos usa 9.
        O backend converte cada 1 num 9 antes de chamar o algoritmo.


    PASSO 3 — O backend verifica as coordenadas.

        Confirma que a origem e o destino estao dentro da grelha e que nao
        sao paredes. Se forem invalidas, devolve um aviso em vez de tentar
        a busca.


    PASSO 4 — O backend chama o algoritmo escolhido.

        Traduz a sigla escolhida no menu (por exemplo "BFS") para a funcao
        correspondente do codigo dos algoritmos. A partir daqui, a logica da
        busca e inteiramente do codigo original.


    PASSO 5 — O algoritmo procura o caminho.

        Parte da origem e vai expandindo celula a celula, seguindo os
        vizinhos livres, ate encontrar o destino. Se nao houver caminho,
        desiste.


    PASSO 6 — O backend prepara a resposta.

        Converte o labirinto de volta para o formato da interface, marcando
        as celulas do caminho.


    PASSO 7 — A interface atualiza o ecra.

        Recebe a resposta e desenha o caminho a azul no labirinto, e escreve
        a sequencia de coordenadas na area "Caminho" do painel de controlo.

    A resposta do backend e:

        {
            "caminho": "(0,0) -> (0,1) -> ... | Custo: X | Nos: Y",
            "grid":    [[0,0,0,...], [ ... ], ...]
        }

    Onde "Caminho" mostra as coordenadas percorridas, "Custo" e o total de
    custo, e "Nos" e o numero de celulas do caminho.


--------------------------------------------------------------------------------
3.8 O BOTAO "REINICIAR GRID"
--------------------------------------------------------------------------------
Limpa o labirinto e o caminho, voltando todas as celulas a livres.

Usar quando se quer recomecar com um labirinto novo, sem ter de reiniciar o
programa.


--------------------------------------------------------------------------------
3.9 SITUACOES QUE PODEM OCORRER
--------------------------------------------------------------------------------

    "Caminho nao encontrado"
        Nao existe caminho entre a origem e o destino. Ou o destino esta
        fechado por paredes, ou a propria origem/destino foi transformada
        em parede. E o funcionamento normal quando o caminho nao existe.

    "Erro ao conectar ao servidor..."
        O backend nao esta a correr. Abrir o terminal 1 e executar o comando
        da seccao 2.1.

    "Coordenada (x,y) e uma parede. Escolha uma celula livre."
        Clicou por cima da celula que escreveu como origem ou destino.
        Clicar nela para a libertar, ou escolher outra coordenada.

    "Coordenada (x,y) fora do grid 10x10"
        As coordenadas tem de estar entre 0 e 9 nos dois eixos.
        Usar valores como "0,0" e "9,9".

    A Profundidade Limitada quase nunca encontra caminho
        E o comportamento esperado: o limite e fixo em 3, por isso so
        encontra destinos a 3 passos ou menos. Para percursos mais longos,
        usar o Aprofundamento Iterativo ou o A*.