import ipaddress
import time
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import os


class TrieNode:
   def __init__(self):
       self.children = {}
       self.prefix = None


class IPTrie:
   def __init__(self):
       self.root = TrieNode()


   def insert(self, prefix):
       try:
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
       except ValueError as e:
           print(f"Erro ao inserir prefixo {prefix}: {e}")


   def longest_prefix_match(self, ip):
       try:
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
       except ValueError as e:
           print(f"Erro ao buscar longest prefix match para IP {ip}: {e}")
           return None


def gerar_ip_aleatorio():
   return f"{randint(1, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(1, 254)}"


def gerar_prefixo_aleatorio():
   ip = gerar_ip_aleatorio()
   mascara = randint(8, 30)
   return f"{ip}/{mascara}"


def executar_teste_performance(qtd_prefixos, qtd_buscas):
   prefixos = [gerar_prefixo_aleatorio() for _ in range(qtd_prefixos)]
   trie = IPTrie()
   inicio = time.time()
   for prefix in prefixos:
       trie.insert(prefix)
   fim = time.time()
   tempo_insercao = fim - inicio
   ips = [gerar_ip_aleatorio() for _ in range(qtd_buscas)]
   inicio = time.time()
   for ip in ips:
       trie.longest_prefix_match(ip)
   fim = time.time()
   tempo_busca = fim - inicio
   return tempo_insercao, tempo_busca


def realizar_todos_testes(nome_base="tp3_4-2"):
   qtd_prefixos_lista = [100, 500, 1000, 5000, 10000]
   qtd_buscas = 1000
   resultados_insercao = {}
   resultados_busca = {}
   for qtd_prefixos in qtd_prefixos_lista:
       print(f"Executando teste com {qtd_prefixos} prefixos e {qtd_buscas} buscas...")
       tempo_ins, tempo_busca = executar_teste_performance(qtd_prefixos, qtd_buscas)
       resultados_insercao[qtd_prefixos] = tempo_ins
       resultados_busca[qtd_prefixos] = tempo_busca
       print(f"Tempo de inserção: {tempo_ins:.2f} segundos")
       print(f"Tempo de busca: {tempo_busca:.2f} segundos")
   salvar_resultados(resultados_insercao, resultados_busca, nome_base)
   print(f"\nResultados salvos em {nome_base}.txt, {nome_base}_insercao.png e {nome_base}_busca.png")
   return resultados_insercao, resultados_busca


def salvar_resultados(resultados_insercao, resultados_busca, nome_base):
   with open(f"{nome_base}.txt", "w") as f:
       f.write("Resultados dos Testes de Performance da Trie para IPs\n")
       f.write("=" * 60 + "\n\n")
       f.write("TEMPOS DE INSERÇÃO\n")
       f.write("-" * 40 + "\n")
       for qtd, tempo in resultados_insercao.items():
           f.write(f"Quantidade de prefixos: {qtd:5d} | Tempo: {tempo:.4f} segundos\n")
       f.write("\nTEMPOS DE BUSCA\n")
       f.write("-" * 40 + "\n")
       for qtd, tempo in resultados_busca.items():
           f.write(f"Quantidade de prefixos na Trie: {qtd:5d} | Tempo para 1000 buscas: {tempo:.4f} segundos\n")
   plt.figure(figsize=(10, 6))
   qtds = list(resultados_insercao.keys())
   tempos = list(resultados_insercao.values())
   plt.plot(qtds, tempos, 'r-o', linewidth=2, markersize=8)
   plt.fill_between(qtds, tempos, alpha=0.1, color='red')
   plt.title('Tempo de Inserção vs Quantidade de Prefixos', fontsize=14, pad=15)
   plt.xlabel('Quantidade de Prefixos', fontsize=12)
   plt.ylabel('Tempo de Execução (segundos)', fontsize=12)
   plt.grid(True, linestyle='--', alpha=0.7)
   for qtd, tempo in resultados_insercao.items():
       plt.annotate(f'{tempo:.4f}s', (qtd, tempo), textcoords="offset points", xytext=(0, 10), ha='center')
   plt.tight_layout()
   plt.savefig(f"{nome_base}_insercao.png", dpi=300, bbox_inches='tight')
   plt.close()
   plt.figure(figsize=(10, 6))
   qtds = list(resultados_busca.keys())
   tempos = list(resultados_busca.values())
   plt.plot(qtds, tempos, 'b-o', linewidth=2, markersize=8)
   plt.fill_between(qtds, tempos, alpha=0.1, color='blue')
   plt.title('Tempo de Busca (1000 IPs) vs Tamanho da Trie', fontsize=14, pad=15)
   plt.xlabel('Quantidade de Prefixos na Trie', fontsize=12)
   plt.ylabel('Tempo para 1000 Buscas (segundos)', fontsize=12)
   plt.grid(True, linestyle='--', alpha=0.7)
   for qtd, tempo in resultados_busca.items():
       plt.annotate(f'{tempo:.4f}s', (qtd, tempo), textcoords="offset points", xytext=(0, 10), ha='center')
   plt.tight_layout()
   plt.savefig(f"{nome_base}_busca.png", dpi=300, bbox_inches='tight')
   plt.close()


