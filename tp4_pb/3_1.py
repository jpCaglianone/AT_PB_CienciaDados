import numpy as np
import matplotlib.pyplot as plt
import time
import random
import string
from collections import defaultdict


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
        if len(nomes_vertices) + 26 ** tamanho_nome <= num_vertices:
            nomes_vertices.extend([gerar_nome_vertice(tamanho_nome) for _ in range(26 ** tamanho_nome)])
        else:
            nomes_vertices.extend([gerar_nome_vertice(tamanho_nome) for _ in range(num_vertices - len(nomes_vertices))])
        tamanho_nome += 1

    # Gera as arestas aleatórias
    arestas = []
    for _ in range(num_arestas):
        origem = random.choice(nomes_vertices)
        destino = random.choice(nomes_vertices)
        # Evita loops (arestas de um vértice para ele mesmo)
        while destino == origem:
            destino = random.choice(nomes_vertices)
        arestas.append((origem, destino))

    return arestas


def medir_tempo_construcao_grafo(arestas, direcionado=False):
    """Mede o tempo para construir um grafo a partir de uma lista de arestas"""
    inicio = time.time()
    grafo = criar_grafo_lista_adjacencia(arestas, direcionado)
    fim = time.time()
    return fim - inicio, grafo


def analisar_grafo(grafo):
    """Analisa e retorna estatísticas sobre o grafo"""
    num_vertices = len(grafo)
    total_arestas = sum(len(adjacentes) for adjacentes in grafo.values())
    grau_medio = total_arestas / num_vertices if num_vertices > 0 else 0
    grau_maximo = max(len(adjacentes) for adjacentes in grafo.values()) if grafo else 0
    grau_minimo = min(len(adjacentes) for adjacentes in grafo.values()) if grafo else 0

    return {
        "num_vertices": num_vertices,
        "total_arestas": total_arestas,
        "grau_medio": grau_medio,
        "grau_maximo": grau_maximo,
        "grau_minimo": grau_minimo
    }


def executar_experimentos():
    """Executa experimentos com diferentes tamanhos de grafos"""
    # Configurações do experimento
    tamanhos_vertices = [10, 100, 1000, 5000, 10000]
    densidades = [0.1, 0.3, 0.5]  # Densidade do grafo (proporção de arestas em relação ao máximo possível)
    direcionado = False  # Tipo do grafo: direcionado ou não-direcionado

    resultados = []

    for num_vertices in tamanhos_vertices:
        for densidade in densidades:
            # Em um grafo completo não direcionado, o número máximo de arestas é n(n-1)/2
            max_arestas = num_vertices * (num_vertices - 1) // 2 if not direcionado else num_vertices * (
                        num_vertices - 1)
            num_arestas = int(max_arestas * densidade)

            print(f"\nGerando grafo com {num_vertices} vértices e {num_arestas} arestas (densidade {densidade:.1f}):")

            arestas = gerar_arestas_aleatorias(num_vertices, num_arestas)
            tempo, grafo = medir_tempo_construcao_grafo(arestas, direcionado)
            estatisticas = analisar_grafo(grafo)

            print(f"  - Tempo de construção: {tempo:.6f} segundos")
            print(f"  - Número real de vértices: {estatisticas['num_vertices']}")
            print(f"  - Total de conexões: {estatisticas['total_arestas']}")
            print(f"  - Grau médio: {estatisticas['grau_medio']:.2f}")
            print(f"  - Grau máximo: {estatisticas['grau_maximo']}")
            print(f"  - Grau mínimo: {estatisticas['grau_minimo']}")

            resultados.append({
                "num_vertices": num_vertices,
                "num_arestas": num_arestas,
                "densidade": densidade,
                "tempo": tempo,
                "estatisticas": estatisticas
            })

    return resultados


def plotar_graficos(resultados):
    """Plota gráficos com os resultados dos experimentos"""
    plt.figure(figsize=(15, 10))

    # Agrupa resultados por densidade
    densidades = sorted(set(r["densidade"] for r in resultados))

    # Gráfico 1: Tempo de construção vs número de vértices
    plt.subplot(2, 2, 1)
    for densidade in densidades:
        dados = [(r["num_vertices"], r["tempo"]) for r in resultados if r["densidade"] == densidade]
        dados.sort()  # Ordena por número de vértices
        x, y = zip(*dados)
        plt.plot(x, y, 'o-', label=f'Densidade {densidade:.1f}')

    plt.title('Tempo de Construção vs Número de Vértices')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.legend()

    # Gráfico 2: Tempo de construção vs número de arestas
    plt.subplot(2, 2, 2)
    for densidade in densidades:
        dados = [(r["num_arestas"], r["tempo"]) for r in resultados if r["densidade"] == densidade]
        dados.sort()  # Ordena por número de arestas
        x, y = zip(*dados)
        plt.plot(x, y, 'o-', label=f'Densidade {densidade:.1f}')

    plt.title('Tempo de Construção vs Número de Arestas')
    plt.xlabel('Número de Arestas')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.legend()

    # Gráfico 3: Comparativo de complexidade
    plt.subplot(2, 2, 3)
    # Filtra resultados para densidade média
    densidade_media = densidades[len(densidades) // 2]
    dados_vertices = [(r["num_vertices"], r["tempo"]) for r in resultados if r["densidade"] == densidade_media]
    dados_vertices.sort()  # Ordena por número de vértices
    x_vertices, y_tempo = zip(*dados_vertices)
    x_vertices = np.array(x_vertices)

    plt.plot(x_vertices, y_tempo, 'bo-', label='Tempo Real')
    plt.plot(x_vertices, x_vertices / 100000, 'r--', label='O(n) - Referência')
    plt.plot(x_vertices, (x_vertices * np.log(x_vertices)) / 100000, 'g--', label='O(n log n) - Referência')

    plt.title(f'Comparativo de Complexidade (Densidade {densidade_media:.1f})')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.legend()

    # Gráfico 4: Grau médio vs número de vértices
    plt.subplot(2, 2, 4)
    for densidade in densidades:
        dados = [(r["num_vertices"], r["estatisticas"]["grau_medio"]) for r in resultados if
                 r["densidade"] == densidade]
        dados.sort()  # Ordena por número de vértices
        x, y = zip(*dados)
        plt.plot(x, y, 'o-', label=f'Densidade {densidade:.1f}')

    plt.title('Grau Médio vs Número de Vértices')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Grau Médio')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig('analise_grafo_lista_adjacencia.png')
    plt.show()


def exemplo_pratico():
    """Demonstra um exemplo prático de criação e uso de um grafo"""
    # Define um conjunto de arestas para um grafo simples
    arestas = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E'), ('E', 'A')]

    print("\nExemplo prático - Grafo não direcionado:")
    grafo = criar_grafo_lista_adjacencia(arestas, direcionado=False)

    # Exibe a lista de adjacência
    print("Lista de adjacência:")
    for vertice, adjacentes in grafo.items():
        print(f"  {vertice}: {adjacentes}")

    # Exibe estatísticas do grafo
    estatisticas = analisar_grafo(grafo)
    print("\nEstatísticas do grafo:")
    print(f"  - Número de vértices: {estatisticas['num_vertices']}")
    print(f"  - Total de conexões: {estatisticas['total_arestas']}")
    print(f"  - Grau médio: {estatisticas['grau_medio']:.2f}")
    print(f"  - Grau máximo: {estatisticas['grau_maximo']}")
    print(f"  - Grau mínimo: {estatisticas['grau_minimo']}")

    # Demonstra como encontrar todos os vizinhos de um vértice
    vertice = 'A'
    print(f"\nVizinhos do vértice {vertice}: {grafo[vertice]}")

    # Demonstra como verificar se existe uma aresta entre dois vértices
    origem, destino = 'A', 'C'
    existe_aresta = destino in grafo[origem]
    print(f"Existe aresta de {origem} para {destino}? {'Sim' if existe_aresta else 'Não'}")


if __name__ == "__main__":
    print("Exercício 3.1 – Representação de grafo (lista de adjacência)")

    # Executa o exemplo prático
    exemplo_pratico()

    # Executa os experimentos com diferentes tamanhos de grafos
    print("\nIniciando experimentos com diferentes tamanhos de grafos...")
    resultados = executar_experimentos()

    # Plota os gráficos de análise
    plotar_graficos(resultados)
