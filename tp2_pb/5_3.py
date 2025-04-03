import time
import random
import concurrent.futures


def merge_sort_sequencial(lista):
   if len(lista) <= 1:
       return lista
   meio = len(lista) // 2
   esquerda = merge_sort_sequencial(lista[:meio])
   direita = merge_sort_sequencial(lista[meio:])
   return merge(esquerda, direita)


def merge_sort_paralelo(lista):
   if len(lista) <= 1:
       return lista
   meio = len(lista) // 2
   with concurrent.futures.ThreadPoolExecutor() as executor:
       esquerda_futuro = executor.submit(merge_sort_paralelo, lista[:meio])
       direita_futuro = executor.submit(merge_sort_paralelo, lista[meio:])
       esquerda = esquerda_futuro.result()
       direita = direita_futuro.result()
   return merge(esquerda, direita)


def merge(esquerda, direita):
   resultado = []
   i = j = 0
   while i < len(esquerda) and j < len(direita):
       if esquerda[i] < direita[j]:
           resultado.append(esquerda[i])
           i += 1
       else:
           resultado.append(direita[j])
           j += 1
   resultado.extend(esquerda[i:])
   resultado.extend(direita[j:])
   return resultado


def testar_ordenacao(lista):
   start_time = time.time()
   lista_sequencial = merge_sort_sequencial(lista)
   tempo_sequencial = time.time() - start_time


   start_time = time.time()
   lista_paralela = merge_sort_paralelo(lista)
   tempo_paralelo = time.time() - start_time


   return tempo_sequencial, tempo_paralelo


tamanhos = [2**i for i in range(1, 11)]
tempos_sequenciais = []
tempos_paralelos = []


for tamanho in tamanhos:
   lista = [random.randint(0, 100000) for _ in range(tamanho)]
   tempo_sequencial, tempo_paralelo = testar_ordenacao(lista)
   tempos_sequenciais.append(tempo_sequencial)
   tempos_paralelos.append(tempo_paralelo)


import matplotlib.pyplot as plt


plt.plot(tamanhos, tempos_sequenciais, label="Sequencial", marker='o')
plt.plot(tamanhos, tempos_paralelos, label="Paralelo", marker='x')
plt.xlabel("Tamanho da lista")
plt.ylabel("Tempo (segundos)")
plt.title("Tempo de Execução para Ordenação (MergeSort)")
plt.legend()
plt.show()


