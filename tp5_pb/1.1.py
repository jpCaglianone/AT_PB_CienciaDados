import sys
import heapq
import time
import numpy as np
import matplotlib.pyplot as plt
import random


def dijkstra(grafo, origem):
    distancias = {vertice: float('infinity') for vertice in grafo}
    distancias[origem] = 0
    fila_prioridade = [(0, origem)]
    visitados = set()

    while fila_prioridade:
        distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)

        if vertice_atual in visitados:
            continue

        visitados.add(vertice_atual)

        for vizinho, peso in grafo[vertice_atual]:
            distancia = distancia_atual + peso

            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                heapq.heappush(fila_prioridade, (distancia, vizinho))

    return distancias


def gerar_grafo_aleatorio(num_vertices, densidade=0.5, peso_max=10):
    grafo = {}
    vertices = [chr(65 + i) if i < 26 else f'V{i}' for i in range(num_vertices)]

    for vertice in vertices:
        grafo[vertice] = []

    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j and random.random() < densidade:
                peso = random.randint(1, peso_max)
                grafo[vertices[i]].append((vertices[j], peso))

    return grafo


def medir_tempo_execucao(tamanhos):
    tempos = []

    for tamanho in tamanhos:
        grafo = gerar_grafo_aleatorio(tamanho)
        origem = list(grafo.keys())[0]

        inicio = time.time()
        dijkstra(grafo, origem)
        fim = time.time()

        tempo_total = fim - inicio
        tempos.append(tempo_total)
        print(f"Tamanho do grafo: {tamanho} vértices, Tempo: {tempo_total:.6f} segundos")

    return tempos


def plotar_grafico_tempo(tamanhos, tempos):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='blue')
    plt.title('Tempo de Execução do Algoritmo de Dijkstra')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.savefig('tempo_execucao_dijkstra.png')


def plotar_grafico_complexidade(tamanhos, tempos):
    plt.figure(figsize=(10, 6))

    x = np.array(tamanhos)
    y = np.array(tempos)

    plt.plot(x, y, 'o-', label='Tempo medido')

    modelo_n_log_n = x * np.log(x) / (x[0] * np.log(x[0])) * y[0]
    plt.plot(x, modelo_n_log_n, '--', label='O(n log n)')

    plt.title('Comparação da Complexidade do Algoritmo de Dijkstra')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)
    plt.savefig('complexidade_dijkstra.png')


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'teste':
        grafo_exemplo = {
            'A': [('B', 1), ('C', 4)],
            'B': [('A', 1), ('C', 2), ('D', 5)],
            'C': [('A', 4), ('B', 2), ('D', 1)],
            'D': [('B', 5), ('C', 1)]
        }
        origem = 'A'

        resultado = dijkstra(grafo_exemplo, origem)

        for vertice, distancia in resultado.items():
            print(f"Distância até {vertice}: {distancia}")
    else:
        tamanhos = [10, 50, 100, 200, 500]
        tempos = medir_tempo_execucao(tamanhos)
        plotar_grafico_tempo(tamanhos, tempos)
        plotar_grafico_complexidade(tamanhos, tempos)


if __name__ == "__main__":
    main()