from collections import deque
from NodeP import NodeP
from math import fabs

class buscaP(object):
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        if y+1<ny:
            if mapa[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                custo = 3
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                custo = 6
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                custo = 3
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                custo = 1
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        return f

    def inserir_ordenado(self,lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)

    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho

    def heuristica_grid(self,p1,p2):
        if (p2[0]-p1[0])<0:
            c1 = 3
        else:
            c1 = 2
        if (p2[1]-p1[1])<0:
            c2 = 7
        else:
            c2 = 5
        h = fabs(p1[0]-p2[0]) + fabs(p1[1]-p2[1])
        return h

    def custo_uniforme_grid(self,inicio,fim,mapa,nx,ny):
        if inicio == fim:
            return [inicio], 0
        lista = deque()
        t_inicio = tuple(inicio)
        raiz = NodeP(None, t_inicio,0, None, None,0)
        lista.append(raiz)
        visitado = {tuple(inicio): raiz}
        while lista:
            atual = lista.popleft()
            valor_atual = atual.v2
            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
            for novo in filhos:
                v2 = valor_atual + novo[1]
                v1 = v2
                t_novo = tuple(novo[0])
                if (t_novo not in visitado) or (v2<visitado[t_novo].v2):
                    filho = NodeP(atual,t_novo,v1,None,None,v2)
                    visitado[t_novo] = filho
                    self.inserir_ordenado(lista, filho)
        return None

    def greedy_grid(self,inicio,fim,mapa,nx,ny):
        if inicio == fim:
            return [inicio], 0
        lista = deque()
        t_inicio = tuple(inicio)
        raiz = NodeP(None, t_inicio,0, None, None, 0)
        lista.append(raiz)
        visitado = {tuple(inicio): raiz}
        while lista:
            atual = lista.popleft()
            valor_atual = atual.v2
            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
            for novo in filhos:
                v2 = valor_atual + novo[1]
                v1 = self.heuristica_grid(novo[0],fim)
                t_novo = tuple(novo[0])
                if (t_novo not in visitado) or (v2<visitado[t_novo].v2):
                    filho = NodeP(atual,t_novo, v1, None, None, v2)
                    visitado[t_novo] = filho
                    self.inserir_ordenado(lista, filho)
        return None

    def a_estrela_grid(self,inicio,fim,mapa,nx,ny):
        if inicio == fim:
            return [inicio], 0
        lista = deque()
        t_inicio = tuple(inicio)
        raiz = NodeP(None, t_inicio,0, None, None, 0)
        lista.append(raiz)
        visitado = {tuple(inicio): raiz}
        while lista:
            atual = lista.popleft()
            valor_atual = atual.v2
            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
            for novo in filhos:
                v2 = valor_atual + novo[1]
                v1 = v2 + self.heuristica_grid(novo[0],fim)
                t_novo = tuple(novo[0])
                if (t_novo not in visitado) or (v2<visitado[t_novo].v2):
                    filho = NodeP(atual,t_novo, v1, None, None, v2)
                    visitado[t_novo] = filho
                    self.inserir_ordenado(lista, filho)
        return None

    def aia_estrela_grid(self,inicio,fim,mapa,nx,ny):
        if inicio == fim:
            return [inicio], 0
        lim = self.heuristica_grid(inicio,fim)
        while True:
            lista = deque()
            t_inicio = tuple(inicio)
            raiz = NodeP(None, t_inicio,0, None, None, 0)
            lista.append(raiz)
            visitado = {tuple(inicio): raiz}
            novo_lim = []
            while lista:
                atual = lista.popleft()
                valor_atual = atual.v2
                if atual.estado == fim:
                    return self.exibirCaminho(atual), atual.v2
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
                for novo in filhos:
                    v2 = valor_atual + novo[1]
                    v1 = v2 + self.heuristica_grid(novo[0],fim)
                    if v1<=lim:
                        t_novo = tuple(novo[0])
                        if (t_novo not in visitado) or (v2<visitado[t_novo].v2):
                            filho = NodeP(atual,t_novo, v1, None, None, v2)
                            visitado[t_novo] = filho
                            self.inserir_ordenado(lista, filho)
                    else:
                        novo_lim.append(v1)
            lim = (int)(sum(novo_lim)/(len(novo_lim)))
            lista.clear()
            visitado.clear()
            novo_lim.clear()
        return None
