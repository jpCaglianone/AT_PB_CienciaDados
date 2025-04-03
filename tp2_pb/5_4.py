

import time
import random
import concurrent.futures


def max_sequencial(lista):
   return max(lista)


def max_paralelo(lista):
   def chunk_max(start, end):
       chunk = lista[start:end]
       if chunk:  # Verifica se a parte não está vazia
           return max(chunk)
       return float('-inf')  # Retorna um valor muito pequeno se o chunk estiver vazio


   num_threads = 4
   tamanho_chunk = len(lista) // num_threads
   with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
       futuros = [executor.submit(chunk_max, i * tamanho_chunk, (i + 1) * tamanho_chunk) for i in range(num_threads)]
       resultados = [futuro.result() for futuro in concurrent.futures.as_completed(futuros)]
   return max(resultados)


def testar_maximo(lista):
   start_time = time.time()
   max_sequencial_resultado = max_sequencial(lista)
   tempo_sequencial = time.time() - start_time


   start_time = time.time()
   max_paralelo_resultado = max_paralelo(lista)
   tempo_paralelo = time.time() - start_time


   return tempo_sequencial, tempo_paralelo


tamanhos = [2**i for i in range(1, 11)]
tempos_sequenciais = []
tempos_paralelos = []


for tamanho in tamanhos:
   lista = [random.randint(0, 100000) for _ in range(tamanho)]
   tempo_sequencial, tempo_paralelo = testar_maximo(lista)
   tempos_sequenciais.append(tempo_sequencial)
   tempos_paralelos.append(tempo_paralelo)


import matplotlib.pyplot as plt


plt.plot(tamanhos, tempos_sequenciais, label="Sequencial", marker='o')
plt.plot(tamanhos, tempos_paralelos, label="Paralelo", marker='x')
plt.xlabel("Tamanho da lista")
plt.ylabel("Tempo (segundos)")
plt.title("Tempo de Execução para Encontrar Máximo (com OpenMP)")
plt.legend()
plt.show()
