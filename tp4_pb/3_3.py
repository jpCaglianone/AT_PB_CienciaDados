

import numpy as np
import matplotlib.pyplot as plt
import time
import random
import string
from collections import defaultdict, deque


def criar_grafo_lista_adjacencia(arestas, direcionado=False):
    """
    Cria uma representação de grafo usando lista de adjacência.

    Parâmetros:
    arestas: Lista de tuplas (origem, destino) representando as arestas
    direcionado: Se True, cria um grafo direcionado; se False, não-direcionado

    Retorna:
    Um dicionário onde as chaves são os vértices e os valores são as listas de adjacência
    """
    grafo = defaultdict(list)

    for origem, destino in arestas:
        grafo[origem].append(destino)

        # Se não for direcionado, adiciona a aresta inversa
        if not direcionado:
            grafo[destino].append(origem)

    return dict(grafo)


def bfs(grafo, no_inicial):
    """
    Implementa a busca em largura (BFS) a partir de um nó inicial.

    Parâmetros:
    grafo: Dicionário representando o grafo como lista de adjacência
    no_inicial: Nó inicial para começar a busca

    Retorna:
    Uma lista com a ordem de visita dos nós
    """
    if no_inicial not in grafo:
        return []

    visitados = set()
    ordem_visita = []
    fila = deque([no_inicial])
    visitados.add(no_inicial)

    while fila:
        no_atual = fila.popleft()
        ordem_visita.append(no_atual)

        for vizinho in grafo[no_atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

    return ordem_visita


def gerar_nome_vertice(tamanho=1):
    """Gera um nome aleatório para um vértice"""
    chars = string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(tamanho))


def gerar_arestas_aleatorias(num_vertices, num_arestas):
    """
    Gera uma lista de arestas aleatórias.

    Parâmetros:
    num_vertices: Número de vértices no grafo
    num_arestas: Número de arestas a serem geradas

    Retorna:
    Uma lista de tuplas (origem, destino) representando as arestas
    """
    # Gera nomes para os vértices (A, B, C, ... AA, AB, ...)
    nomes_vertices = []
    tamanho_nome = 1
    while len(nomes_vertices) < num_vertices:
        if len(nomes_vertices) + 26**tamanho_nome <= num_vertices:
            nomes_vertices.extend([gerar_nome_vertice(tamanho_nome) for _ in range(26**tamanho_nome)])
        else:
            nomes_vertices.extend([gerar_nome_vertice(tamanho_nome) for _ in range(num_vertices - len(nomes_vertices))])
        tamanho_nome += 1

    # Garantir que o grafo seja conexo: criar uma espinha dorsal
    arestas = []
    for i in range(1, num_vertices):
        arestas.append((nomes_vertices[i-1], nomes_vertices[i]))

    # Adicionar arestas aleatórias restantes
    arestas_restantes = num_arestas - (num_vertices - 1)
    for _ in range(arestas_restantes):
        origem = random.choice(nomes_vertices)
        destino = random.choice(nomes_vertices)
        # Evita loops e arestas duplicadas
        while destino == origem or (origem, destino) in arestas:
            destino = random.choice(nomes_vertices)
        arestas.append((origem, destino))

    return arestas, nomes_vertices[0]  # Retorna as arestas e o primeiro vértice como nó inicial


def medir_tempo_bfs(grafo, no_inicial):
    """Mede o tempo para executar BFS no grafo"""
    inicio = time.time()
    ordem_visita = bfs(grafo, no_inicial)
    fim = time.time()
    return fim - inicio, ordem_visita


def analisar_cobertura_bfs(grafo, ordem_visita):
    """Analisa a cobertura da BFS no grafo"""
    total_vertices = len(grafo)
    vertices_visitados = len(ordem_visita)
    cobertura = vertices_visitados / total_vertices if total_vertices > 0 else 0

    return {
        "total_vertices": total_vertices,
        "vertices_visitados": vertices_visitados,
        "cobertura": cobertura
    }


def executar_experimentos_bfs():
    """Executa experimentos de BFS com diferentes tamanhos de grafos"""
    # Configurações do experimento
    tamanhos_vertices = [10, 50, 100, 500, 1000]
    densidades = [0.01, 0.05, 0.1]  # Densidade do grafo (proporção de arestas em relação ao máximo possível)
    direcionado = False  # Tipo do grafo: direcionado ou não-direcionado

    resultados = []

    for num_vertices in tamanhos_vertices:
        for densidade in densidades:
            # Em um grafo completo não direcionado, o número máximo de arestas é n(n-1)/2
            max_arestas = num_vertices * (num_vertices - 1) // 2 if not direcionado else num_vertices * (num_vertices - 1)
            num_arestas = int(max_arestas * densidade) + num_vertices - 1  # Garantir grafos conexos

            print(f"\nGerando grafo com {num_vertices} vértices e {num_arestas} arestas (densidade {densidade:.3f}):")

            arestas, no_inicial = gerar_arestas_aleatorias(num_vertices, num_arestas)
            grafo = criar_grafo_lista_adjacencia(arestas, direcionado)

            print(f"  - Executando BFS a partir do nó '{no_inicial}'...")
            tempo, ordem_visita = medir_tempo_bfs(grafo, no_inicial)
            cobertura = analisar_cobertura_bfs(grafo, ordem_visita)

            print(f"  - Tempo de execução: {tempo:.6f} segundos")
            print(f"  - Vértices visitados: {cobertura['vertices_visitados']} de {cobertura['total_vertices']} ({cobertura['cobertura']*100:.2f}%)")

            # Exibir os primeiros 5 nós visitados para grafos de todos os tamanhos
            print(f"  - Primeiros 5 nós visitados: {ordem_visita[:5]}")

            # Para grafos pequenos, mostrar a ordem completa
            if num_vertices <= 10:
                print(f"  - Ordem completa de visita: {ordem_visita}")

            resultados.append({
                "num_vertices": num_vertices,
                "num_arestas": num_arestas,
                "densidade": densidade,
                "tempo": tempo,
                "cobertura": cobertura
            })

    return resultados


def plotar_graficos_bfs(resultados):
    """Plota gráficos com os resultados dos experimentos de BFS"""
    plt.figure(figsize=(15, 10))

    # Agrupa resultados por densidade
    densidades = sorted(set(r["densidade"] for r in resultados))

    # Gráfico 1: Tempo de execução vs número de vértices
    plt.subplot(2, 2, 1)
    for densidade in densidades:
        dados = [(r["num_vertices"], r["tempo"]) for r in resultados if r["densidade"] == densidade]
        dados.sort()  # Ordena por número de vértices
        x, y = zip(*dados)
        plt.plot(x, y, 'o-', label=f'Densidade {densidade:.3f}')

    plt.title('Tempo de Execução BFS vs Número de Vértices')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.legend()

    # Gráfico 2: Tempo de execução vs número de arestas
    plt.subplot(2, 2, 2)
    for densidade in densidades:
        dados = [(r["num_arestas"], r["tempo"]) for r in resultados if r["densidade"] == densidade]
        dados.sort()  # Ordena por número de arestas
        x, y = zip(*dados)
        plt.plot(x, y, 'o-', label=f'Densidade {densidade:.3f}')

    plt.title('Tempo de Execução BFS vs Número de Arestas')
    plt.xlabel('Número de Arestas')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.legend()

    # Gráfico 3: Comparativo de complexidade
    plt.subplot(2, 2, 3)
    # Filtra resultados para densidade média
    densidade_media = densidades[len(densidades)//2]
    dados_vertices = [(r["num_vertices"], r["tempo"]) for r in resultados if r["densidade"] == densidade_media]
    dados_vertices.sort()  # Ordena por número de vértices
    x_vertices, y_tempo = zip(*dados_vertices)
    x_vertices = np.array(x_vertices)

    plt.plot(x_vertices, y_tempo, 'bo-', label='Tempo Real')
    plt.plot(x_vertices, x_vertices / 50000, 'r--', label='O(V) - Referência')
    plt.plot(x_vertices, (x_vertices + (x_vertices * densidade_media * x_vertices)) / 50000, 'g--', label='O(V+E) - Referência')

    plt.title(f'Comparativo de Complexidade (Densidade {densidade_media:.3f})')
    plt.xlabel('Número de Vértices (V)')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.legend()

    # Gráfico 4: Cobertura do BFS vs número de vértices
    plt.subplot(2, 2, 4)
    for densidade in densidades:
        dados = [(r["num_vertices"], r["cobertura"]["cobertura"]) for r in resultados if r["densidade"] == densidade]
        dados.sort()  # Ordena por número de vértices
        x, y = zip(*dados)
        plt.plot(x, y, 'o-', label=f'Densidade {densidade:.3f}')

    plt.title('Cobertura BFS vs Número de Vértices')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Cobertura (proporção de vértices visitados)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig('analise_bfs_grafo.png')
    plt.show()


def exemplo_pratico_bfs():
    """Demonstra um exemplo prático de BFS em um grafo pequeno"""
    # Define um conjunto de arestas para um grafo simples
    arestas = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('E', 'G'), ('F', 'G')]

    print("\nExemplo prático - BFS em um grafo pequeno:")
    grafo = criar_grafo_lista_adjacencia(arestas, direcionado=False)

    # Exibe a lista de adjacência
    print("Lista de adjacência:")
    for vertice, adjacentes in sorted(grafo.items()):
        print(f"  {vertice}: {sorted(adjacentes)}")

    # Executa BFS a partir de diferentes nós iniciais
    nos_iniciais = ['A', 'D', 'G']

    for no_inicial in nos_iniciais:
        print(f"\nBFS a partir do nó '{no_inicial}':")
        tempo, ordem_visita = medir_tempo_bfs(grafo, no_inicial)
        print(f"  - Tempo de execução: {tempo:.6f} segundos")
        print(f"  - Ordem de visita: {ordem_visita}")

        # Demonstra como encontrar os níveis de cada nó na BFS
        niveis = {}
        for i, no in enumerate(ordem_visita):
            # Determinando o nível pela primeira ocorrência na ordem de visita
            if no == no_inicial:
                niveis[no] = 0
            else:
                # Para cada nó, encontramos o vizinho de menor índice na ordem de visita
                nivel_minimo = float('inf')
                for vizinho in grafo[no]:
                    if vizinho in niveis:
                        nivel_minimo = min(nivel_minimo, niveis[vizinho] + 1)
                niveis[no] = nivel_minimo

        print("  - Níveis dos nós:")
        for no, nivel in sorted(niveis.items()):
            print(f"    * {no}: Nível {nivel}")


if __name__ == "__main__":
    print("Exercício 3.3 – BFS em grafo")

    # Executa o exemplo prático
    exemplo_pratico_bfs()

    # Executa os experimentos com diferentes tamanhos de grafos
    print("\nIniciando experimentos de BFS com diferentes tamanhos de grafos...")
    resultados = executar_experimentos_bfs()

    # Plota os gráficos de análise
    plotar_graficos_bfs(resultados)


