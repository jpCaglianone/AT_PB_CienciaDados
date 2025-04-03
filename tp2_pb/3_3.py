

import matplotlib.pyplot as plt
import numpy as np


class Node:
   def __init__(self, valor):
       self.valor = valor
       self.proximo = None




class LinkedList:
   def __init__(self):
       self.cabeca = None
       self.operacoes = []
       self.estados = []


   def adicionar(self, valor):
       novo_no = Node(valor)
       if not self.cabeca:
           self.cabeca = novo_no
       else:
           atual = self.cabeca
           while atual.proximo:
               atual = atual.proximo
           atual.proximo = novo_no
       self.operacoes.append(f'Adicionado {valor}')
       self.estados.append(self.exibir())


   def buscar(self, valor):
       atual = self.cabeca
       posicao = 0
       while atual:
           if atual.valor == valor:
               return posicao
           atual = atual.proximo
           posicao += 1
       return -1


   def inverter(self):
       anterior = None
       atual = self.cabeca
       while atual:
           proximo_no = atual.proximo
           atual.proximo = anterior
           anterior = atual
           atual = proximo_no
       self.cabeca = anterior
       self.operacoes.append('Lista invertida')
       self.estados.append(self.exibir())


   def exibir(self):
       atual = self.cabeca
       lista = []
       while atual:
           lista.append(atual.valor)
           atual = atual.proximo
       return lista


   def plotar_evolucao(self):
       plt.figure(figsize=(12, 6))


       # Gráfico de linha mostrando o tamanho da lista ao longo das operações
       tamanhos = [len(estado) for estado in self.estados]
       plt.plot(range(len(tamanhos)), tamanhos, marker='o', linestyle='-', linewidth=2, markersize=8)


       plt.title('Evolução do Tamanho da Lista Encadeada')
       plt.xlabel('Número da Operação')
       plt.ylabel('Tamanho da Lista')
       plt.grid(True)


       # Adicionar anotações para cada operação
       for i, (op, tam) in enumerate(zip(self.operacoes, tamanhos)):
           plt.annotate(op, (i, tam), textcoords="offset points", xytext=(0, 10), ha='center')


       plt.tight_layout()
       plt.show()




print("==== Testes com a Lista Encadeada ====")


lista = LinkedList()
print("Teste 1 - Lista inicial vazia:", lista.exibir())


lista.adicionar(1)
lista.adicionar(2)
lista.adicionar(3)
print("Teste 2 - Após adicionar elementos [1, 2, 3]:", lista.exibir())


print("Teste 3 - Buscar o valor 2:", lista.buscar(2))


print("Teste 4 - Buscar o valor 5:", lista.buscar(5))


lista.inverter()
print("Teste 5 - Lista invertida [3, 2, 1]:", lista.exibir())


lista.adicionar(4)
print("Teste 6 - Adicionar o valor 4 após inversão:", lista.exibir())


lista.inverter()
print("Teste 7 - Inverter novamente:", lista.exibir())


print("Teste 8.1 - Buscar o valor 4 (início):", lista.buscar(4))
print("Teste 8.2 - Buscar o valor 2 (meio):", lista.buscar(2))
print("Teste 8.3 - Buscar o valor 3 (fim):", lista.buscar(3))


lista2 = LinkedList()
lista2.adicionar(10)
lista2.inverter()
print("Teste 9 - Inverter lista com um único elemento [10]:", lista2.exibir())


lista_vazia = LinkedList()
lista_vazia.inverter()
print("Teste 10 - Inverter uma lista vazia:", lista_vazia.exibir())


lista.plotar_evolucao()


