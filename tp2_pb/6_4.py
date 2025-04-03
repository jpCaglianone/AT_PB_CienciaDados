

import time
import matplotlib.pyplot as plt
import numpy as np


def calcular_combinacoes_pinturas(n_cadeiras, n_cores):
   dp = [[0 for _ in range(n_cores)] for _ in range(n_cadeiras)]
   for cor in range(n_cores):
       dp[0][cor] = 1
   for i in range(1, n_cadeiras):
       for cor_atual in range(n_cores):
           for cor_anterior in range(n_cores):
               if cor_atual != cor_anterior:
                   dp[i][cor_atual] += dp[i - 1][cor_anterior]
   return sum(dp[n_cadeiras - 1])


def analisar_performance():
   cores = [3, 4, 5]
   max_cadeiras = 15
   cadeiras_range = range(1, max_cadeiras + 1)
   plt.figure(figsize=(15, 10))
   plt.subplot(2, 1, 1)
   for n_cores in cores:
       tempos = []
       for n_cadeiras in cadeiras_range:
           inicio = time.time()
           resultado = calcular_combinacoes_pinturas(n_cadeiras, n_cores)
           fim = time.time()
           tempos.append((fim - inicio) * 1000)
       plt.plot(cadeiras_range, tempos, marker='o', label=f'{n_cores} cores')
   plt.title('Análise de Performance - Tempo de Execução')
   plt.xlabel('Número de Cadeiras')
   plt.ylabel('Tempo (ms)')
   plt.grid(True, alpha=0.3)
   plt.legend()
   plt.subplot(2, 1, 2)
   for n_cores in cores:
       combinacoes = []
       for n_cadeiras in cadeiras_range:
           resultado = calcular_combinacoes_pinturas(n_cadeiras, n_cores)
           combinacoes.append(resultado)
       plt.plot(cadeiras_range, combinacoes, marker='o', label=f'{n_cores} cores')
   plt.title('Análise de Resultados - Número de Combinações Possíveis')
   plt.xlabel('Número de Cadeiras')
   plt.ylabel('Número de Combinações')
   plt.grid(True, alpha=0.3)
   plt.legend()
   plt.yscale('log')
   plt.tight_layout()
   return plt


def executar_testes():
   casos_teste = [
       (3, 2),
       (4, 3),
       (5, 3),
       (6, 4),
   ]
   print("Análise de casos específicos:")
   print("-" * 50)
   for n_cadeiras, n_cores in casos_teste:
       inicio = time.time()
       resultado = calcular_combinacoes_pinturas(n_cadeiras, n_cores)
       tempo = (time.time() - inicio) * 1000
       print(f"\nCaso: {n_cadeiras} cadeiras com {n_cores} cores")
       print(f"Número de combinações possíveis: {resultado}")
       print(f"Tempo de execução: {tempo:.4f} ms")


if __name__ == "__main__":
   print("Executando testes...")
   executar_testes()
   print("\nGerando análise de performance...")
   plt = analisar_performance()
   plt.show()
