import time
import random


def k_menores_elementos(lista, k=10):
   menores = [float('inf')] * k
   for num in lista[:k]:
       menores.append(num)
       menores = sorted(menores)[:k]
   for num in lista[k:]:
       if num < menores[-1]:
           menores[-1] = num
           menores = sorted(menores)[:k]
   return menores


def main():
   lista_aleatoria = random.sample(range(1, 100000), 50000)


   start_time = time.time()
   menores_10 = k_menores_elementos(lista_aleatoria, k=1000)
   end_time = time.time()


   tempo_execucao = end_time - start_time


   print("Os 10 menores elementos encontrados:", menores_10)
   print("Tempo de execução: {:.6f} segundos".format(tempo_execucao))


for i in range(10):
   main()
