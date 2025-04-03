

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
       self.tempos_ordenacao = []
       self.tamanhos = []
       self.valores = []


   def adicionar(self, valor):
       novo_no = Node(valor)
       if not self.cabeca:
           self.cabeca = self.cauda = novo_no
       else:
           self.cauda.proximo = novo_no
           novo_no.anterior = self.cauda
           self.cauda = novo_no
       self.valores.append(valor)
       self.tamanhos.append(len(self.valores))


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
       inicio = time.time()
       trocou = True
       while trocou:
           trocou = False
           atual = self.cabeca
           while atual and atual.proximo:
               if atual.valor > atual.proximo.valor:
                   atual.valor, atual.proximo.valor = atual.proximo.valor, atual.valor
                   trocou = True
               atual = atual.proximo
       fim = time.time()
       self.tempos_ordenacao.append(fim - inicio)


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


   def plotar_desempenho(self):
       plt.figure(figsize=(15, 5))


       plt.subplot(1, 2, 1)
       plt.plot(self.tamanhos, 'b-', linewidth=2)
       plt.title('Crescimento da Lista')
       plt.xlabel('Operações')
       plt.ylabel('Tamanho')
       plt.grid(True)


       if self.tempos_ordenacao:
           plt.subplot(1, 2, 2)
           plt.bar(range(len(self.tempos_ordenacao)), self.tempos_ordenacao)
           plt.title('Tempo de Ordenação')
           plt.xlabel('Tentativas')
           plt.ylabel('Tempo (s)')


       plt.tight_layout()
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


lista2 = DoublyLinkedList()
for valor in [8, 2, 6, 9, 0]:
   lista2.adicionar(valor)


print("\nLista 2 antes da ordenação:", lista2.exibir())
_, tempo_bubble2 = medir_tempo(lista2.bubble_sort)
print("Lista 2 após ordenação (Bubble Sort):", lista2.exibir())
print(f"Tempo gasto para ordenar a lista 2: {tempo_bubble2:.6f} segundos")


_, tempo_mesclagem = medir_tempo(lista1.mesclar, lista2)
lista_mesclada = lista1.mesclar(lista2)
print("\nLista mesclada:", lista_mesclada.exibir())
print(f"Tempo gasto para mesclar as listas: {tempo_mesclagem:.6f} segundos")


print("\n==== Testes Adicionais ====")


lista_vazia = DoublyLinkedList()
print("Teste 4.1 - Lista vazia antes da ordenação:", lista_vazia.exibir())
_, tempo_vazia = medir_tempo(lista_vazia.bubble_sort)
print("Teste 4.2 - Lista vazia após ordenação:", lista_vazia.exibir())
print(f"Tempo gasto para ordenar lista vazia: {tempo_vazia:.6f} segundos")


_, tempo_mesclagem_vazia = medir_tempo(lista1.mesclar, lista_vazia)
lista_mesclada_vazia = lista1.mesclar(lista_vazia)
print("Teste 5 - Mesclagem de lista ordenada com lista vazia:", lista_mesclada_vazia.exibir())
print(f"Tempo gasto para mesclar lista ordenada com lista vazia: {tempo_mesclagem_vazia:.6f} segundos")


lista_unica = DoublyLinkedList()
lista_unica.adicionar(42)
print("\nTeste 6.1 - Lista com único elemento antes da ordenação:", lista_unica.exibir())
_, tempo_unica = medir_tempo(lista_unica.bubble_sort)
print("Teste 6.2 - Lista com único elemento após ordenação:", lista_unica.exibir())
print(f"Tempo gasto para ordenar lista com um único elemento: {tempo_unica:.6f} segundos")


lista_unica2 = DoublyLinkedList()
lista_unica2.adicionar(10)
_, tempo_mesclagem_unica = medir_tempo(lista_unica.mesclar, lista_unica2)
lista_mesclada_unica = lista_unica.mesclar(lista_unica2)
print("Teste 7 - Mesclagem de duas listas com único elemento cada:", lista_mesclada_unica.exibir())
print(f"Tempo gasto para mesclar listas com único elemento: {tempo_mesclagem_unica:.6f} segundos")


lista_ordenada = DoublyLinkedList()
for valor in [1, 2, 3, 4, 5]:
   lista_ordenada.adicionar(valor)
print("\nTeste 8.1 - Lista já ordenada antes da ordenação:", lista_ordenada.exibir())
_, tempo_ordenada = medir_tempo(lista_ordenada.bubble_sort)
print("Teste 8.2 - Lista já ordenada após ordenação:", lista_ordenada.exibir())
print(f"Tempo gasto para ordenar lista já ordenada: {tempo_ordenada:.6f} segundos")


lista_reversa = DoublyLinkedList()
for valor in [9, 8, 7, 6, 5]:
   lista_reversa.adicionar(valor)
print("\nTeste 9.1 - Lista em ordem reversa antes da ordenação:", lista_reversa.exibir())
_, tempo_reversa = medir_tempo(lista_reversa.bubble_sort)
print("Teste 9.2 - Lista em ordem reversa após ordenação:", lista_reversa.exibir())
print(f"Tempo gasto para ordenar lista em ordem reversa: {tempo_reversa:.6f} segundos")


lista_grande1 = DoublyLinkedList()
lista_grande2 = DoublyLinkedList()
for valor in range(0, 100, 2):
   lista_grande1.adicionar(valor)
for valor in range(1, 101, 2):
   lista_grande2.adicionar(valor)
_, tempo_mesclagem_grande = medir_tempo(lista_grande1.mesclar, lista_grande2)
lista_grande_mesclada = lista_grande1.mesclar(lista_grande2)
print("\nTeste 10 - Mesclagem de duas listas grandes ordenadas:", lista_grande_mesclada.exibir())
print(f"Tempo gasto para mesclar duas listas grandes ordenadas: {tempo_mesclagem_grande:.6f} segundos")


lista1.plotar_desempenho()
lista2.plotar_desempenho()
lista_grande1.plotar_desempenho()
lista_grande2.plotar_desempenho()


