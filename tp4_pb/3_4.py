
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque
import random


def criar_grafo_aleatorio(n_nos, probabilidade_conexao=0.3):
    grafo = {}
    for i in range(n_nos):
        grafo[i] = []

    for i in range(n_nos):
        for j in range( i +1, n_nos):
            if random.random() < probabilidade_conexao:
                grafo[i].append(j)
                grafo[j].append(i)

    return grafo


def busca_dfs(grafo, inicio, fim):
    visitados = set()
    caminho = []

    def dfs_recursiva(no_atual, caminho_atual):
        visitados.add(no_atual)
        caminho_atual.append(no_atual)

        if no_atual == fim:
            return True

        for vizinho in grafo[no_atual]:
            if vizinho not in visitados:
                if dfs_recursiva(vizinho, caminho_atual):
                    return True

        caminho_atual.pop()
        return False

    dfs_recursiva(inicio, caminho)
    return caminho if caminho and caminho[-1] == fim else None


def busca_bfs(grafo, inicio, fim):
    if inicio == fim:
        return [inicio]

    visitados = set([inicio])
    fila = deque([(inicio, [inicio])])

    while fila:
        no_atual, caminho = fila.popleft()

        for vizinho in grafo[no_atual]:
            if vizinho == fim:
                return caminho + [vizinho]

            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))

    return None


def comparar_algoritmos(grafos, no_inicio, no_fim):
    tempos_dfs = []
    tempos_bfs = []
    tamanhos_grafo = []
    comprimentos_dfs = []
    comprimentos_bfs = []

    resultados = {'DFS': [], 'BFS': []}

    for grafo in grafos:
        tamanhos_grafo.append(len(grafo))

        inicio_tempo = time.time()
        caminho_dfs = busca_dfs(grafo, no_inicio, no_fim)
        fim_tempo = time.time()
        tempos_dfs.append(fim_tempo - inicio_tempo)
        resultados['DFS'].append(caminho_dfs)
        comprimentos_dfs.append(len(caminho_dfs) if caminho_dfs else 0)

        inicio_tempo = time.time()
        caminho_bfs = busca_bfs(grafo, no_inicio, no_fim)
        fim_tempo = time.time()
        tempos_bfs.append(fim_tempo - inicio_tempo)
        resultados['BFS'].append(caminho_bfs)
        comprimentos_bfs.append(len(caminho_bfs) if caminho_bfs else 0)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(tamanhos_grafo, tempos_dfs, 'ro-', label='DFS')
    plt.plot(tamanhos_grafo, tempos_bfs, 'bo-', label='BFS')
    plt.xlabel('Tamanho do Grafo (número de nós)')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.title('Comparação de Tempo de Execução')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    x = np.array(tamanhos_grafo)
    plt.plot(x, x/ 1000, 'g--', label='O(n) - Linear')
    plt.plot(x, x * np.log(x) / 3000, 'm--', label='O(n log n)')
    plt.plot(tamanhos_grafo, tempos_dfs, 'ro-', label='DFS')
    plt.plot(tamanhos_grafo, tempos_bfs, 'bo-', label='BFS')
    plt.xlabel('Tamanho do Grafo (número de nós)')
    plt.ylabel('Complexidade Relativa')
    plt.title('Análise de Complexidade')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('comparacao_tempo_complexidade.png')
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.bar(np.array(tamanhos_grafo) - 2, comprimentos_dfs, width=4, color='r', alpha=0.6, label='DFS')
    plt.bar(np.array(tamanhos_grafo) + 2, comprimentos_bfs, width=4, color='b', alpha=0.6, label='BFS')
    plt.xlabel('Tamanho do Grafo (número de nós)')
    plt.ylabel('Comprimento do Caminho')
    plt.title('Comparação do Comprimento dos Caminhos Encontrados')
    plt.legend()
    plt.grid(True, axis='y')
    plt.savefig('comparacao_comprimento_caminhos.png')
    plt.close()

    return resultados, tempos_dfs, tempos_bfs, comprimentos_dfs, comprimentos_bfs, tamanhos_grafo


def exemplo_execucao():
    print("Iniciando comparação de algoritmos DFS e BFS...")

    tamanhos = [10, 50, 100, 200, 300, 400, 500]
    grafos_teste = []

    for tamanho in tamanhos:
        grafos_teste.append(criar_grafo_aleatorio(tamanho))

    resultados, tempos_dfs, tempos_bfs, comprimentos_dfs, comprimentos_bfs, tamanhos_grafo = comparar_algoritmos(
        grafos_teste, 0, min(7, tamanhos[0] - 1))

    print("\nEstatísticas de execução:")
    for i, tamanho in enumerate(tamanhos):
        print(f"Grafo com {tamanho} nós:")
        print(f"  DFS: tempo={tempos_dfs[i]:.6f}s", end="")
        if resultados['DFS'][i]:
            print(f", caminho de tamanho {len(resultados['DFS'][i])}")
        else:
            print(", não encontrou caminho")

        print(f"  BFS: tempo={tempos_bfs[i]:.6f}s", end="")
        if resultados['BFS'][i]:
            print(f", caminho de tamanho {len(resultados['BFS'][i])}")
        else:
            print(", não encontrou caminho")

    print("\nGráficos salvos em 'comparacao_tempo_complexidade.png' e 'comparacao_comprimento_caminhos.png'")


if __name__ == "__main__":
    exemplo_execucao()
