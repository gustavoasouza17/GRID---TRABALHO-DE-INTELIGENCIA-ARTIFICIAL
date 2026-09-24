from buscaNP import buscaNP
import utils as fa
from os import system

op = 1
while(op!='3'):
    system("cls")
    print("**** TIPO DE EXECUÇÃO ****\n")
    print("1. GRID")
    print("3. SAIR")
    op = input("Sua opção: ")

    flag_menu = True
    if op=='1':
        arquivo = "mapa3.txt"
        mapa,dx,dy = fa.Gera_Problema_Grid_Fixo(arquivo)
        for x in mapa:
            print(x)
        origem  = tuple(map(int, input("Digite a origem (x y): ").split()))
        destino = tuple(map(int, input("Digite o destino (x y): ").split()))
        flag_origem  = (0<=origem[0]<dx)  and (0<=origem[1]<dy)  and (mapa[origem[0]][origem[1]]==0)
        flag_destino = (0<=destino[0]<dx) and (0<=destino[1]<dy) and (mapa[destino[0]][destino[1]]==0)
        flag_dados = flag_origem and flag_destino
    else:
        flag_menu = False

    if flag_menu:
        if flag_dados:
            sol = buscaNP()

            caminho = sol.amplitude_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("AMPLITUDE", caminho, len(caminho))
            else:
                print("AMPLITUDE\nCAMINHO NÃO ENCONTRADO")

            caminho = sol.profundidade_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("PROFUNDIDADE", caminho, len(caminho))
            else:
                print("PROFUNDIDADE\nCAMINHO NÃO ENCONTRADO")

            limite = 3
            caminho = sol.prof_limitada_grid(origem,destino,dx,dy,mapa,limite)
            if caminho!=None:
                fa.imprimeCaminho("PROFUNDIDADE LIMITADA", caminho, len(caminho))
            else:
                print("PROFUNDIDADE LIMITADA\nCAMINHO NÃO ENCONTRADO")

            l_max = dx + dy
            caminho = sol.aprof_iterativo_grid(origem,destino,dx,dy,mapa,l_max)
            if caminho!=None:
                fa.imprimeCaminho("APROFUNDAMENTO ITERATIVO", caminho, len(caminho))
            else:
                print("APROFUNDAMENTO ITERATIVO\nCAMINHO NÃO ENCONTRADO")

            caminho = sol.bidirecional_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("BIDIRECIONAL", caminho, len(caminho))
            else:
                print("BIDIRECIONAL\nCAMINHO NÃO ENCONTRADO")
        else:
            print("Estados inválidos!")

        op = input("Pressione ENTER para continuar!")