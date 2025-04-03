import ipaddress
import time
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import os




def verificar_ip_em_rede(ip, prefixo):
   try:
       endereco_ip = ipaddress.ip_address(ip)
       rede = ipaddress.ip_network(prefixo, strict=False)
       return endereco_ip in rede
   except ValueError as e:
       print(f"Erro: {e}")
       return False




def gerar_ip_aleatorio():
   return f"{randint(1, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(1, 254)}"




def executar_teste_performance(quantidade_ips, prefixo="192.168.1.0/24"):
   ips = [gerar_ip_aleatorio() for _ in range(quantidade_ips)]


   inicio = time.time()
   for ip in ips:
       verificar_ip_em_rede(ip, prefixo)
   fim = time.time()


   tempo_total = fim - inicio
   return quantidade_ips, tempo_total




def salvar_resultados(resultados, nome_base):
   with open(f"{nome_base}.txt", "w") as f:
       f.write("Resultados dos Testes de Performance\n")
       f.write("-" * 40 + "\n")
       for qtd, tempo in resultados.items():
           f.write(f"Quantidade de IPs: {qtd:5d} | Tempo: {tempo:.2f} segundos\n")


   plt.figure(figsize=(10, 6))
   qtds = list(resultados.keys())
   tempos = list(resultados.values())


   plt.plot(qtds, tempos, 'b-o', linewidth=2, markersize=8)
   plt.fill_between(qtds, tempos, alpha=0.1)


   plt.title('Tempo de Execução vs Quantidade de IPs', fontsize=14, pad=15)
   plt.xlabel('Quantidade de IPs', fontsize=12)
   plt.ylabel('Tempo de Execução (segundos)', fontsize=12)
   plt.grid(True, linestyle='--', alpha=0.7)


   for qtd, tempo in resultados.items():
       plt.annotate(f'{tempo:.2f}s',
                    (qtd, tempo),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center')


   plt.tight_layout()
   plt.savefig(f"{nome_base}.png", dpi=300, bbox_inches='tight')
   plt.close()




def realizar_todos_testes(nome_base="tp3_4-1"):
   quantidades = [500, 1000, 2500, 5000, 10000]


   resultados = {}
   for qtd in quantidades:
       print(f"Executando teste com {qtd} IPs...")
       _, tempo = executar_teste_performance(qtd)
       resultados[qtd] = tempo
       print(f"Tempo de execução: {tempo:.2f} segundos")


   salvar_resultados(resultados, nome_base)
   print(f"\nResultados salvos em {nome_base}.txt e {nome_base}.png")


   return resultados




if __name__ == "__main__":
   print("Iniciando testes de performance...")
   resultados = realizar_todos_testes()



