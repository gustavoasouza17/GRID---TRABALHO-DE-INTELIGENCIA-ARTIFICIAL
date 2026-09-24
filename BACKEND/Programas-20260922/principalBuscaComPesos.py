import utils as fa
import sys
from os import system
from BuscaP import buscaP

while(True):
    system("cls")
    print("**** TIPO DE EXECUÇÃO ****\n")
    print("1. GRID")
    print("2. SAIR")
    op = input("Sua opção:")

    if(op=='1'):
        arquivo = "mapa3.txt"
        mapa,dx,dy = fa.Gera_Problema_Grid_Fixo(arquivo)
        for x in mapa:
            print(x)
        origem  = tuple(map(int, input("Digite a origem (x y): ").split()))
        destino = tuple(map(int, input("Digite o destino (x y): ").split()))
        print(origem)
        print(destino)
        flag_origem  = (0<=origem[0]<dx)  and (0<=origem[1]<dy)  and (mapa[origem[0]][origem[1]]==0)
        flag_destino = (0<=destino[0]<dx) and (0<=destino[1]<dy) and (mapa[destino[0]][destino[1]]==0)
        flag = flag_origem and flag_destino
    else:
        sys.exit()

    if flag:
        system("cls")
        sol = buscaP()

        caminho, custo = sol.custo_uniforme_grid(origem,destino,mapa,dx,dy)
        if caminho!=None:
            print("*** CUSTO UNIFORME ****")
            print("Caminho...: ",caminho)
            print("Custo.....:",custo)
        else:
            print("Caminho não encontrado")

        caminho, custo = sol.greedy_grid(origem,destino,mapa,dx,dy)
        if caminho!=None:
            print("\n*** GREEDY ****")
            print("Caminho...: ",caminho)
            print("Custo.....:",custo)
        else:
            print("Caminho não encontrado")

        caminho, custo = sol.a_estrela_grid(origem,destino,mapa,dx,dy)
        if caminho!=None:
            print("\n*** A ESTRELA ****")
            print("Caminho...: ",caminho)
            print("Custo.....:",custo)
        else:
            print("Caminho não encontrado")

        caminho, custo = sol.aia_estrela_grid(origem,destino,mapa,dx,dy)
        if caminho!=None:
            print("\n*** AIA ESTRELA ****")
            print("Caminho...: ",caminho)
            print("Custo.....:",custo)
        else:
            print("Caminho não encontrado")

        input("\nPressione ENTER para continuar.")