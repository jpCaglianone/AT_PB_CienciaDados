
import numpy as np
import matplotlib.pyplot as plt
import time
import networkx as nx
from collections import defaultdict
import os


class Grafo:
    def __init__(self):
        self.grafo = defaultdict(list)

    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)

    def dfs(self, no_inicial):
        visitados = set()
        ordem_visita = []

        def dfs_recursivo(no):
            visitados.add(no)
            ordem_visita.append(no)

            for vizinho in self.grafo[no]:
                if vizinho not in visitados:
                    dfs_recursivo(vizinho)

        dfs_recursivo(no_inicial)
        return ordem_visita


def gerar_grafo_aleatorio(num_nos, densidade):
    g = Grafo()
    for i in range(num_nos):
        for j in range(num_nos):
            if i != j and np.random.random() < densidade:
                g.adicionar_aresta(i, j)
    return g


def criar_grafo_arvore(num_nos):
    g = Grafo()
    for i in range(1, num_nos):
        pai = np.random.randint(0, i)
        g.adicionar_aresta(pai, i)
    return g


def criar_grafo_ciclo(num_nos):
    g = Grafo()
    for i in range(num_nos -1):
        g.adicionar_aresta(i, i+ 1)
    g.adicionar_aresta(num_nos - 1, 0)
    return g


def criar_grafo_completo(num_nos):
    g = Grafo()
    for i in range(num_nos):
        for j in range(num_nos):
            if i != j:
                g.adicionar_aresta(i, j)
    return g


def criar_grafo_bipartido(num_nos):
    g = Grafo()
    metade = num_nos // 2

    for i in range(metade):
        for j in range(metade, num_nos):
            g.adicionar_aresta(i, j)
    return g


def visualizar_grafo(grafo, ordem_visita=None, titulo="Visualização do Grafo", nome_arquivo=None):
    G = nx.DiGraph()

    for no in grafo.grafo:
        for vizinho in grafo.grafo[no]:
            G.add_edge(no, vizinho)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)

    if ordem_visita:
        node_colors = ['lightblue' for _ in range(max(G.nodes()) + 1 if G.nodes() else 1)]
        for idx, no in enumerate(ordem_visita):
            if no in G.nodes():
                node_colors[no] = plt.cm.viridis(idx / len(ordem_visita))

        nx.draw(G, pos, with_labels=True, node_color=[node_colors[n] for n in G.nodes()],
                node_size=700, arrows=True, arrowsize=15)

        edge_colors = []
        for u, v in G.edges():
            if u in ordem_visita and v in ordem_visita and ordem_visita.index(u) < ordem_visita.index(v):
                edge_colors.append('red')
            else:
                edge_colors.append('black')

        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1.5)
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue',
                node_size=700, arrows=True, arrowsize=15)

    plt.title(titulo)
    plt.axis('off')
    plt.tight_layout()

    if nome_arquivo:
        plt.savefig(nome_arquivo)
        plt.close()


def analisar_desempenho():
    tamanhos = np.arange(10, 1010, 100)
    densidades = [0.1, 0.3, 0.5, 0.7]
    todos_tempos = {d: [] for d in densidades}

    for d in densidades:
        for n in tamanhos:
            g = gerar_grafo_aleatorio(n, d)
            inicio = time.time()
            g.dfs(0)
            fim = time.time()
            todos_tempos[d].append(fim - inicio)

    plt.figure(figsize=(12, 6))
    for d in densidades:
        plt.plot(tamanhos, todos_tempos[d], marker='o', label=f'Densidade={d}')

    plt.xlabel('Número de Nós')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Tempo de Execução do DFS vs. Tamanho do Grafo')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('dfs_tempo_execucao.png')
    plt.close()

    complexidades = []
    for n in tamanhos:
        complexidades.append(n + (n * (n - 1)) * 0.5)  # O(V + E), onde E médio é n*(n-1)/2 * densidade

    plt.figure(figsize=(12, 6))
    plt.plot(tamanhos, complexidades, marker='x', color='red', linestyle='--', label='Complexidade Teórica O(V+E)')
    for d in densidades:
        plt.plot(tamanhos, [t * 10000 for t in todos_tempos[d]], marker='o', label=f'Densidade={d} (escalado)')

    plt.xlabel('Número de Nós')
    plt.ylabel('Operações / Tempo (escalado)')
    plt.title('Comparação entre Complexidade Teórica e Tempo Real')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('dfs_complexidade_comparacao.png')
    plt.close()


def comparar_diferentes_tipos_grafos():
    tipos_grafos = {
        "Árvore": criar_grafo_arvore,
        "Ciclo": criar_grafo_ciclo,
        "Completo": criar_grafo_completo,
        "Bipartido": criar_grafo_bipartido,
        "Aleatório (d=0.3)": lambda n: gerar_grafo_aleatorio(n, 0.3)
    }

    tamanhos = [10, 20, 30, 40, 50]
    resultados = {tipo: [] for tipo in tipos_grafos}

    for n in tamanhos:
        for tipo, func_gerar in tipos_grafos.items():
            g = func_gerar(n)
            inicio = time.time()
            g.dfs(0)
            fim = time.time()
            resultados[tipo].append(fim - inicio)

    plt.figure(figsize=(12, 6))
    for tipo, tempos in resultados.items():
        plt.plot(tamanhos, tempos, marker='o', label=tipo)

    plt.xlabel('Número de Nós')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Comparação de Desempenho do DFS em Diferentes Tipos de Grafos')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('dfs_comparacao_tipos_grafos.png')
    plt.close()


def demonstracao():
    np.random.seed(42)

    # Criando o grafo original
    g_original = Grafo()
    arestas = [
        (0, 1), (0, 2), (1, 3), (1, 4),
        (2, 5), (2, 6), (3, 7), (5, 8),
        (6, 9), (9, 10)
    ]
    for u, v in arestas:
        g_original.adicionar_aresta(u, v)

    no_inicial = 0
    ordem_visita = g_original.dfs(no_inicial)

    print(f"Ordem de visita DFS no grafo original (nó inicial = {no_inicial}):")
    print(ordem_visita)

    visualizar_grafo(g_original, ordem_visita, "Grafo Original - DFS", 'grafo_original.png')

    # Criando e visualizando os diferentes tipos de grafos
    g_arvore = criar_grafo_arvore(12)
    ordem_visita = g_arvore.dfs(0)
    print(f"\nOrdem de visita DFS no grafo árvore (nó inicial = 0):")
    print(ordem_visita)
    visualizar_grafo(g_arvore, ordem_visita, "Grafo Árvore - DFS", 'grafo_arvore.png')

    g_ciclo = criar_grafo_ciclo(10)
    ordem_visita = g_ciclo.dfs(0)
    print(f"\nOrdem de visita DFS no grafo ciclo (nó inicial = 0):")
    print(ordem_visita)
    visualizar_grafo(g_ciclo, ordem_visita, "Grafo Ciclo - DFS", 'grafo_ciclo.png')

    g_completo = criar_grafo_completo(8)
    ordem_visita = g_completo.dfs(0)
    print(f"\nOrdem de visita DFS no grafo completo (nó inicial = 0):")
    print(ordem_visita)
    visualizar_grafo(g_completo, ordem_visita, "Grafo Completo - DFS", 'grafo_completo.png')

    g_bipartido = criar_grafo_bipartido(12)
    ordem_visita = g_bipartido.dfs(0)
    print(f"\nOrdem de visita DFS no grafo bipartido (nó inicial = 0):")
    print(ordem_visita)
    visualizar_grafo(g_bipartido, ordem_visita, "Grafo Bipartido - DFS", 'grafo_bipartido.png')

    g_aleatorio = gerar_grafo_aleatorio(15, 0.3)
    ordem_visita = g_aleatorio.dfs(0)
    print(f"\nOrdem de visita DFS no grafo aleatório (nó inicial = 0):")
    print(ordem_visita)
    visualizar_grafo(g_aleatorio, ordem_visita, "Grafo Aleatório - DFS", 'grafo_aleatorio.png')

    # Análise de desempenho
    analisar_desempenho()

    # Comparação entre diferentes tipos de grafos
    comparar_diferentes_tipos_grafos()

    print("\nTodas as imagens foram salvas na pasta do código.")


if __name__ == "__main__":
    demonstracao()


