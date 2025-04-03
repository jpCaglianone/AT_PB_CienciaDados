
import sys
import heapq
import time
import numpy as np
import matplotlib.pyplot as plt
import random


def prim(grafo, vertice_inicial):
    arestas_mst = []
    vertices_visitados = {vertice_inicial}
    arestas_candidatas = [(peso, vertice_inicial, vizinho)
                          for vizinho, peso in grafo[vertice_inicial]]
    heapq.heapify(arestas_candidatas)

    peso_total = 0

    while arestas_candidatas and len(vertices_visitados) < len(grafo):
        peso, u, v = heapq.heappop(arestas_candidatas)

        if v not in vertices_visitados:
            vertices_visitados.add(v)
            arestas_mst.append((u, v, peso))
            peso_total += peso

            for vizinho, peso in grafo[v]:
                if vizinho not in vertices_visitados:
                    heapq.heappush(arestas_candidatas, (peso, v, vizinho))

    return arestas_mst, peso_total


def gerar_grafo_nao_direcionado(num_vertices, densidade=0.5, peso_max=10):
    grafo = {}
    vertices = [chr(65 + i) if i < 26 else f'V{i}' for i in range(num_vertices)]

    for vertice in vertices:
        grafo[vertice] = []

    for i in range(num_vertices):
        for j in range( i +1, num_vertices):
            if random.random() < densidade:
                peso = random.randint(1, peso_max)
                grafo[vertices[i]].append((vertices[j], peso))
                grafo[vertices[j]].append((vertices[i], peso))

    return grafo


def verificar_conectividade(grafo):
    if not grafo:
        return False

    vertices_visitados = set()
    inicio = next(iter(grafo))

    def dfs(vertice):
        vertices_visitados.add(vertice)
        for vizinho, _ in grafo[vertice]:
            if vizinho not in vertices_visitados:
                dfs(vizinho)

    dfs(inicio)

    return len(vertices_visitados) == len(grafo)


def gerar_grafo_conectado(num_vertices, densidade=0.5, peso_max=10):
    while True:
        grafo = gerar_grafo_nao_direcionado(num_vertices, densidade, peso_max)
        if verificar_conectividade(grafo):
            return grafo
        densidade += 0.1
        if densidade > 1.0:
            densidade = 0.5


def medir_tempo_execucao(tamanhos):
    tempos = []

    for tamanho in tamanhos:
        grafo = gerar_grafo_conectado(tamanho)
        vertice_inicial = list(grafo.keys())[0]

        inicio = time.time()
        prim(grafo, vertice_inicial)
        fim = time.time()

        tempo_total = fim - inicio
        tempos.append(tempo_total)
        print(f"Tamanho do grafo: {tamanho} vértices, Tempo: {tempo_total:.6f} segundos")

    return tempos


def plotar_grafico_tempo(tamanhos, tempos):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='blue')
    plt.title('Tempo de Execução do Algoritmo de Prim')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.savefig('tempo_execucao_prim.png')


def plotar_grafico_complexidade(tamanhos, tempos):
    plt.figure(figsize=(10, 6))

    x = np.array(tamanhos)
    y = np.array(tempos)

    plt.plot(x, y, 'o-', label='Tempo medido')

    modelo_e_log_v = x** 2 * np.log(x) / (x[0] ** 2 * np.log(x[0])) * y[0]
    plt.plot(x, modelo_e_log_v, '--', label='O(E log V)')

    plt.title('Comparação da Complexidade do Algoritmo de Prim')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)
    plt.savefig('complexidade_prim.png')


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'teste':
        grafo_exemplo = {
            'A': [('B', 2), ('C', 3)],
            'B': [('A', 2), ('C', 1), ('D', 4)],
            'C': [('A', 3), ('B', 1), ('D', 5)],
            'D': [('B', 4), ('C', 5)]
        }

        vertice_inicial = 'A'
        arestas_mst, peso_total = prim(grafo_exemplo, vertice_inicial)

        print(f"Árvore Geradora Mínima (iniciando de {vertice_inicial}):")
        for u, v, peso in arestas_mst:
            print(f"{u} - {v} com peso {peso}")
        print(f"Peso total da MST: {peso_total}")
    else:
        tamanhos = [10, 50, 100, 200, 500]
        tempos = medir_tempo_execucao(tamanhos)
        plotar_grafico_tempo(tamanhos, tempos)
        plotar_grafico_complexidade(tamanhos, tempos)


if __name__ == "__main__":
    main()
