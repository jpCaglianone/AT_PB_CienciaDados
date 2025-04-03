



import time
import matplotlib.pyplot as plt
import numpy as np


class Node:
   def __init__(self, valor):
       self.valor = valor
       self.proximo = None
       self.anterior = None


class DoublyLinkedList:
   def __init__(self):
       self.cabeca = None
       self.cauda = None
       self.valores = []
       self.tempos = []


   def adicionar(self, valor):
       novo_no = Node(valor)
       if not self.cabeca:
           self.cabeca = self.cauda = novo_no
       else:
           self.cauda.proximo = novo_no
           novo_no.anterior = self.cauda
           self.cauda = novo_no
       self.valores.append(self.exibir())
       self.tempos.append(time.time())


   def exibir(self):
       atual = self.cabeca
       lista = []
       while atual:
           lista.append(atual.valor)
           atual = atual.proximo
       return lista


   def bubble_sort(self):
       if not self.cabeca:
           return


       trocou = True
       while trocou:
           trocou = False
           atual = self.cabeca
           while atual and atual.proximo:
               if atual.valor > atual.proximo.valor:
                   atual.valor, atual.proximo.valor = atual.proximo.valor, atual.valor
                   trocou = True
               atual = atual.proximo
           self.valores.append(self.exibir())
           self.tempos.append(time.time())


   def mesclar(self, outra_lista):
       lista_mesclada = DoublyLinkedList()
       atual1 = self.cabeca
       atual2 = outra_lista.cabeca


       while atual1 and atual2:
           if atual1.valor <= atual2.valor:
               lista_mesclada.adicionar(atual1.valor)
               atual1 = atual1.proximo
           else:
               lista_mesclada.adicionar(atual2.valor)
               atual2 = atual2.proximo


       while atual1:
           lista_mesclada.adicionar(atual1.valor)
           atual1 = atual1.proximo


       while atual2:
           lista_mesclada.adicionar(atual2.valor)
           atual2 = atual2.proximo


       return lista_mesclada


   def plotar_evolucao(self):
       plt.figure(figsize=(12, 6))
       tempos_normalizados = [t - self.tempos[0] for t in self.tempos]
       for i, valores in enumerate(self.valores):
           plt.plot(valores, marker='o', label=f'Estado {i+1}')
       plt.title('Evolução da Lista')
       plt.xlabel('Índice')
       plt.ylabel('Valor')
       plt.grid(True)
       plt.legend()
       plt.show()


def medir_tempo(func, *args, **kwargs):
   inicio = time.time()
   resultado = func(*args, **kwargs)
   fim = time.time()
   return resultado, fim - inicio


print("==== Testes com Lista Duplamente Encadeada ====")


lista1 = DoublyLinkedList()
for valor in [7, 3, 5, 1, 4]:
   lista1.adicionar(valor)


print("Lista 1 antes da ordenação:", lista1.exibir())
_, tempo_bubble = medir_tempo(lista1.bubble_sort)
print("Lista 1 após ordenação (Bubble Sort):", lista1.exibir())
print(f"Tempo gasto para ordenar a lista 1: {tempo_bubble:.6f} segundos")
lista1.plotar_evolucao()


lista2 = DoublyLinkedList()
for valor in [8, 2, 6, 9, 0]:
   lista2.adicionar(valor)


print("\nLista 2 antes da ordenação:", lista2.exibir())
_, tempo_bubble2 = medir_tempo(lista2.bubble_sort)
print("Lista 2 após ordenação (Bubble Sort):", lista2.exibir())
print(f"Tempo gasto para ordenar a lista 2: {tempo_bubble2:.6f} segundos")
lista2.plotar_evolucao()


_, tempo_mesclagem = medir_tempo(lista1.mesclar, lista2)
lista_mesclada = lista1.mesclar(lista2)
print("\nLista mesclada:", lista_mesclada.exibir())
print(f"Tempo gasto para mesclar as listas: {tempo_mesclagem:.6f} segundos")
lista_mesclada.plotar_evolucao()
