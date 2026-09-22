from collections import deque
from Node import Node

class buscaNP(object):
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        if y+1<ny:
            if mapa[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                f.append(suc)
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                f.append(suc)
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                f.append(suc)
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                f.append(suc)
        return f[::-1]

    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho

    def localiza_encontro(self,valor,lista):
        for no in reversed(lista):
            if no.estado==valor:
                return no

    def exibirCaminho_bid(self,encontro,fila1,fila2):
        encontro1 = self.localiza_encontro(encontro,fila1)
        encontro2 = self.localiza_encontro(encontro,fila2)
        caminho1 = self.exibirCaminho(encontro1)
        caminho2 = self.exibirCaminho(encontro2)
        caminho2 = list(reversed(caminho2[:-1]))
        return caminho1 + caminho2

    def amplitude_grid(self,inicio,fim,nx,ny,mapa):
        if inicio == fim:
            return [inicio]
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        fila = deque()
        raiz = Node(None,t_inicio,0,None,None)
        fila.append(raiz)
        visitado = {}
        visitado[t_inicio] = 0
        while fila:
            atual = fila.popleft()
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
            for novo in filhos:
                t_novo = tuple(novo)
                flag = True
                if t_novo in visitado:
                    if visitado[t_novo]<=atual.v1+1:
                        flag = False
                if flag:
                    filho = Node(atual,novo,atual.v1 + 1,None,None)
                    fila.append(filho)
                    visitado[t_novo] = atual.v1 + 1
                    if t_novo == t_fim:
                        return self.exibirCaminho(filho)
        return None

    def profundidade_grid(self,inicio,fim,nx,ny,mapa):
        if inicio == fim:
            return [inicio]
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        pilha = deque()
        raiz = Node(None,t_inicio,0,None,None)
        pilha.append(raiz)
        visitado = {}
        visitado[t_inicio] = 0
        while pilha:
            atual = pilha.pop()
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
            for novo in filhos:
                t_novo = tuple(novo)
                flag = True
                if t_novo in visitado:
                    if visitado[t_novo]<=atual.v1+1:
                        flag = False
                if flag:
                    filho = Node(atual,novo,atual.v1 + 1,None,None)
                    pilha.append(filho)
                    visitado[t_novo] = atual.v1 + 1
                    if t_novo == t_fim:
                        return self.exibirCaminho(filho)
        return None

    def prof_limitada_grid(self,inicio,fim,nx,ny,mapa,lim):
        if inicio == fim:
            return [inicio]
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        pilha = deque()
        raiz = Node(None,t_inicio,0,None,None)
        pilha.append(raiz)
        visitado = {}
        visitado[t_inicio] = 0
        while pilha:
            atual = pilha.pop()
            if atual.v1<lim:
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
                for novo in filhos:
                    t_novo = tuple(novo)
                    flag = True
                    if t_novo in visitado:
                        if visitado[t_novo]<=atual.v1+1:
                            flag = False
                    if flag:
                        filho = Node(atual,novo,atual.v1 + 1,None,None)
                        pilha.append(filho)
                        visitado[t_novo] = atual.v1 + 1
                        if t_novo == t_fim:
                            return self.exibirCaminho(filho)
        return None

    def aprof_iterativo_grid(self,inicio,fim,nx,ny,mapa,lim_max):
        if inicio == fim:
            return [inicio]
        for lim in range(1,lim_max):
            t_inicio = tuple(inicio)
            t_fim = tuple(fim)
            pilha = deque()
            raiz = Node(None,t_inicio,0,None,None)
            pilha.append(raiz)
            visitado = {}
            visitado[t_inicio] = 0
            while pilha:
                atual = pilha.pop()
                if atual.v1<lim:
                    filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
                    for novo in filhos:
                        t_novo = tuple(novo)
                        flag = True
                        if t_novo in visitado:
                            if visitado[t_novo]<=atual.v1+1:
                                flag = False
                        if flag:
                            filho = Node(atual,novo,atual.v1 + 1,None,None)
                            pilha.append(filho)
                            visitado[t_novo] = atual.v1 + 1
                            if t_novo == t_fim:
                                return self.exibirCaminho(filho)
            visitado.clear()
            pilha.clear()
        return None

    def bidirecional_grid(self,inicio,fim,nx,ny,mapa):
        if inicio == fim:
            return [inicio]
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        fila1 = deque()
        fila2 = deque()
        raiz = Node(None,t_inicio,0,None,None)
        fila1.append(raiz)
        raiz = Node(None,t_fim,0,None,None)
        fila2.append(raiz)
        visitado1 = {}
        visitado1[t_inicio] = 0
        visitado2 = {}
        visitado2[t_fim] = 0
        nivel = 0
        while fila1 and fila2:
            nivel = len(fila1)
            for _ in range(nivel):
                atual = fila1.popleft()
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
                for novo in filhos:
                    t_novo = tuple(novo)
                    flag = True
                    if t_novo in visitado1:
                        if visitado1[t_novo]<=atual.v1+1:
                            flag = False
                    if flag:
                        filho = Node(atual,novo,atual.v1 + 1,None,None)
                        fila1.append(filho)
                        visitado1[t_novo] = atual.v1 + 1
                        if t_novo in visitado2:
                            return self.exibirCaminho_bid(novo,fila1,fila2)
            nivel = len(fila2)
            for _ in range(nivel):
                atual = fila2.popleft()
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
                for novo in filhos:
                    t_novo = tuple(novo)
                    flag = True
                    if t_novo in visitado2:
                        if visitado2[t_novo]<=atual.v1+1:
                            flag = False
                    if flag:
                        filho = Node(atual,novo,atual.v1 + 1,None,None)
                        fila2.append(filho)
                        visitado2[t_novo] = atual.v1 + 1
                        if t_novo in visitado1:
                            return self.exibirCaminho_bid(novo,fila1,fila2)
        return None
