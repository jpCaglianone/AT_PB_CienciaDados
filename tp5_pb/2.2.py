
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import random
import math


def distancia_euclidiana(cidade1, cidade2):
    return math.sqrt((cidade1['x'] - cidade2['x'] )**2 + (cidade1['y'] - cidade2['y'] )**2)


def calcular_matriz_distancias(cidades):
    n = len(cidades)
    matriz = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            matriz[i][j] = distancia_euclidiana(cidades[i], cidades[j])

    return matriz


def vizinho_mais_proximo(cidades, cidade_inicial=0):
    n = len(cidades)
    matriz_distancias = calcular_matriz_distancias(cidades)

    visitadas = [False] * n
    rota = [cidade_inicial]
    visitadas[cidade_inicial] = True

    cidade_atual = cidade_inicial
    distancia_total = 0

    for _ in range(n - 1):
        menor_distancia = float('inf')
        proxima_cidade = -1

        for cidade in range(n):
            if not visitadas[cidade] and matriz_distancias[cidade_atual][cidade] < menor_distancia:
                menor_distancia = matriz_distancias[cidade_atual][cidade]
                proxima_cidade = cidade

        rota.append(proxima_cidade)
        visitadas[proxima_cidade] = True
        distancia_total += menor_distancia
        cidade_atual = proxima_cidade

    distancia_total += matriz_distancias[rota[-1]][rota[0]]

    return rota, distancia_total


def gerar_cidades_aleatorias(n, limite=100):
    cidades = []
    for i in range(n):
        cidades.append({
            'nome': chr(65 + i) if i < 26 else f'Cidade{i}',
            'x': random.uniform(0, limite),
            'y': random.uniform(0, limite)
        })
    return cidades


def medir_tempo_execucao(tamanhos):
    tempos = []
    distancias = []

    for tamanho in tamanhos:
        cidades = gerar_cidades_aleatorias(tamanho)

        inicio = time.time()
        rota, distancia_total = vizinho_mais_proximo(cidades)
        fim = time.time()

        tempo_total = fim - inicio
        tempos.append(tempo_total)
        distancias.append(distancia_total)

        print(f"Número de cidades: {tamanho}, Tempo: {tempo_total:.6f} segundos")
        print(f"Distância total da rota: {distancia_total:.2f}")
        print(f"Primeiras 5 cidades da rota: {[cidades[i]['nome'] for i in rota[:5] if i < len(cidades)]}")
        print("-" * 50)

    return tempos, distancias


def plotar_grafico_tempo(tamanhos, tempos):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='blue')
    plt.title('Tempo de Execução da Heurística do Vizinho Mais Próximo para o TSP')
    plt.xlabel('Número de Cidades')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.savefig('tempo_execucao_tsp_vizinho_proximo.png')


def plotar_grafico_complexidade(tamanhos, tempos):
    plt.figure(figsize=(10, 6))

    x = np.array(tamanhos)
    y = np.array(tempos)

    plt.plot(x, y, 'o-', label='Tempo medido')

    modelo_n2 = x** 2 / (x[0] ** 2) * y[0]
    plt.plot(x, modelo_n2, '--', label='O(n²)')

    plt.title('Comparação da Complexidade da Heurística do Vizinho Mais Próximo')
    plt.xlabel('Número de Cidades')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)
    plt.savefig('complexidade_tsp_vizinho_proximo.png')


def plotar_grafico_distancia(tamanhos, distancias):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, distancias, marker='o', linestyle='-', color='green')
    plt.title('Distância Total da Rota vs. Número de Cidades')
    plt.xlabel('Número de Cidades')
    plt.ylabel('Distância Total')
    plt.grid(True)
    plt.savefig('distancia_tsp_vizinho_proximo.png')


def plotar_rota(cidades, rota):
    plt.figure(figsize=(10, 8))

    x = [cidades[i]['x'] for i in rota]
    y = [cidades[i]['y'] for i in rota]

    x.append(x[0])
    y.append(y[0])

    plt.plot(x, y, 'o-')

    for i, cidade in enumerate(rota):
        plt.annotate(cidades[cidade]['nome'], (cidades[cidade]['x'], cidades[cidade]['y']))

    plt.title('Rota do Caixeiro Viajante - Heurística do Vizinho Mais Próximo')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.savefig('rota_tsp_vizinho_proximo.png')


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'teste':
        cidades_exemplo = [
            {'nome': 'A', 'x': 0, 'y': 0},
            {'nome': 'B', 'x': 1, 'y': 5},
            {'nome': 'C', 'x': 5, 'y': 2},
            {'nome': 'D', 'x': 6, 'y': 6},
            {'nome': 'E', 'x': 8, 'y': 3}
        ]

        rota, distancia_total = vizinho_mais_proximo(cidades_exemplo)

        print("Rota encontrada pela heurística do vizinho mais próximo:")
        rota_nomes = " -> ".join(cidades_exemplo[i]['nome'] for i in rota)
        print(rota_nomes + f" -> {cidades_exemplo[rota[0]]['nome']}")
        print(f"Distância total: {distancia_total:.2f}")

        plotar_rota(cidades_exemplo, rota)
    else:
        tamanhos = [10, 50, 100, 500, 1000]
        tempos, distancias = medir_tempo_execucao(tamanhos)

        plotar_grafico_tempo(tamanhos, tempos)
        plotar_grafico_complexidade(tamanhos, tempos)
        plotar_grafico_distancia(tamanhos, distancias)

        cidades_visualizacao = gerar_cidades_aleatorias(20)
        rota_visualizacao, _ = vizinho_mais_proximo(cidades_visualizacao)
        plotar_rota(cidades_visualizacao, rota_visualizacao)


if __name__ == "__main__":
    main()
