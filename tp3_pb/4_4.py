import ipaddress
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import os


class TrieNode:
    def __init__(self):
        self.children = {}
        self.prefix = None


class IPTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, prefix):
        net = ipaddress.IPv4Network(prefix, strict=False)
        node = self.root

        ip_int = int(net.network_address)
        prefix_len = net.prefixlen

        for i in range(32):
            if i < prefix_len:
                bit = (ip_int >> (31 - i)) & 1

                if bit not in node.children:
                    node.children[bit] = TrieNode()

                node = node.children[bit]

                if i == prefix_len - 1:
                    node.prefix = prefix

    def longest_prefix_match(self, ip):
        ip_addr = ipaddress.IPv4Address(ip)
        node = self.root
        best_match = None

        ip_int = int(ip_addr)

        for i in range(32):
            bit = (ip_int >> (31 - i)) & 1

            if bit not in node.children:
                break

            node = node.children[bit]

            if node.prefix is not None:
                best_match = node.prefix

        return best_match


def busca_linear(prefixos, ip):
    ip_addr = ipaddress.IPv4Address(ip)
    melhor_match = None
    maior_prefixo = -1

    for prefixo in prefixos:
        rede = ipaddress.IPv4Network(prefixo, strict=False)
        if ip_addr in rede and rede.prefixlen > maior_prefixo:
            melhor_match = prefixo
            maior_prefixo = rede.prefixlen

    return melhor_match


def gerar_ip_aleatorio():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def gerar_prefixo_aleatorio():
    ip = gerar_ip_aleatorio()
    mascara = random.randint(8, 30)
    return f"{ip}/{mascara}"


def gerar_lista_prefixos(quantidade):
    return [gerar_prefixo_aleatorio() for _ in range(quantidade)]


def comparar_metodos(tamanhos_lista):
    resultados = {
        'tamanhos': tamanhos_lista,
        'tempo_linear': [],
        'tempo_trie': [],
        'tempo_construcao_trie': []
    }

    num_buscas = 50

    for tamanho in tamanhos_lista:
        print(f"Testando com {tamanho} prefixos...")

        prefixos = gerar_lista_prefixos(tamanho)
        ips_teste = [gerar_ip_aleatorio() for _ in range(num_buscas)]

        inicio = time.time()
        trie = IPTrie()
        for prefixo in prefixos:
            trie.insert(prefixo)
        fim = time.time()
        tempo_construcao = fim - inicio
        resultados['tempo_construcao_trie'].append(tempo_construcao)

        inicio = time.time()
        for ip in ips_teste:
            busca_linear(prefixos, ip)
        fim = time.time()
        tempo_linear = fim - inicio
        resultados['tempo_linear'].append(tempo_linear)

        inicio = time.time()
        for ip in ips_teste:
            trie.longest_prefix_match(ip)
        fim = time.time()
        tempo_trie = fim - inicio
        resultados['tempo_trie'].append(tempo_trie)

        print(f"  Tempo busca linear: {tempo_linear:.4f}s")
        print(f"  Tempo busca Trie: {tempo_trie:.4f}s")
        print(f"  Tempo construção Trie: {tempo_construcao:.4f}s")

    return resultados


def gerar_graficos(resultados, nome_base="tp3_4-3"):
    tamanhos = resultados['tamanhos']

    with open(f"{nome_base}.txt", "w") as f:
        f.write("Comparação de Métodos para Longest Prefix Match\n")
        f.write("=" * 50 + "\n\n")

        f.write("TEMPOS DE EXECUÇÃO\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Qtd Prefixos':12} | {'Busca Linear':15} | {'Busca Trie':15} | {'Construção Trie':15}\n")

        for i, tamanho in enumerate(tamanhos):
            f.write(
                f"{tamanho:12d} | {resultados['tempo_linear'][i]:15.4f} | {resultados['tempo_trie'][i]:15.4f} | {resultados['tempo_construcao_trie'][i]:15.4f}\n")

        f.write("\nANÁLISE COMPARATIVA\n")
        f.write("-" * 50 + "\n")
        for i, tamanho in enumerate(tamanhos):
            razao = resultados['tempo_linear'][i] / resultados['tempo_trie'][i]
            f.write(f"Para {tamanho} prefixos, a busca Trie é {razao:.1f}x mais rápida que a busca linear.\n")

        f.write("\nCONCLUSÃO\n")
        f.write("-" * 50 + "\n")
        f.write("A busca Trie é significativamente mais eficiente para grandes conjuntos de dados.\n")
        f.write("O custo inicial de construção da Trie é compensado pela rapidez nas buscas.\n")

    plt.figure(figsize=(12, 6))
    plt.plot(tamanhos, resultados['tempo_linear'], 'r-o', linewidth=2, markersize=8, label='Busca Linear')
    plt.plot(tamanhos, resultados['tempo_trie'], 'b-o', linewidth=2, markersize=8, label='Busca Trie')

    plt.title('Comparação: Busca Linear vs. Trie para Longest Prefix Match', fontsize=14, pad=15)
    plt.xlabel('Número de Prefixos', fontsize=12)
    plt.ylabel('Tempo de Execução (segundos)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig(f"{nome_base}_busca.png", dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(tamanhos, resultados['tempo_construcao_trie'], 'g-o', linewidth=2, markersize=8)

    plt.title('Tempo de Construção da Trie', fontsize=14, pad=15)
    plt.xlabel('Número de Prefixos', fontsize=12)
    plt.ylabel('Tempo de Execução (segundos)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(f"{nome_base}_construcao.png", dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(12, 6))
    eficiencia = [resultados['tempo_linear'][i] / resultados['tempo_trie'][i] for i in range(len(tamanhos))]
    plt.bar(range(len(tamanhos)), eficiencia, color='purple', alpha=0.7)

    plt.title('Eficiência: Quanto a Trie é mais rápida que a Busca Linear', fontsize=14, pad=15)
    plt.xlabel('Tamanho da Lista de Prefixos', fontsize=12)
    plt.ylabel('Fator de Velocidade (x vezes mais rápido)', fontsize=12)
    plt.xticks(range(len(tamanhos)), tamanhos)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')

    for i, valor in enumerate(eficiencia):
        plt.text(i, valor + 0.5, f'{valor:.1f}x', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{nome_base}_eficiencia.png", dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    tamanhos_teste = [100, 500, 1000, 2500, 5000]

    print("Iniciando comparação entre métodos de busca por prefixo...")
    resultados = comparar_metodos(tamanhos_teste)

    print("\nGerando gráficos e relatório...")
    gerar_graficos(resultados)

    print("\nAnálise concluída! Arquivos salvos: tp3_4-3.txt e imagens PNG.")



