

import time
import matplotlib.pyplot as plt
import numpy as np
import random


class Node:
   def __init__(self, value):
       self.value = value
       self.next = None




class LinkedList:
   def __init__(self):
       self.head = None


   def inserir_inicio(self, value):
       new_node = Node(value)
       new_node.next = self.head
       self.head = new_node


   def inserir_fim(self, value):
       new_node = Node(value)
       if not self.head:
           self.head = new_node
           return
       last = self.head
       while last.next:
           last = last.next
       last.next = new_node


   def excluir(self, value):
       if not self.head:
           return
       if self.head.value == value:
           self.head = self.head.next
           return
       current = self.head
       while current.next:
           if current.next.value == value:
               current.next = current.next.next
               return
           current = current.next


   def exibir(self):
       current = self.head
       elements = []
       while current:
           elements.append(current.value)
           current = current.next
       return elements




def medir_tempo(operacao, *args):
   start_time = time.time()
   operacao(*args)
   end_time = time.time()
   return end_time - start_time




def executar_teste():
   lista = LinkedList()


   tempo_inicio = medir_tempo(lista.inserir_inicio, 5)
   for i in range(10000):
       lista.inserir_inicio(i)


   tempo_fim = medir_tempo(lista.inserir_fim, 15000)
   for i in range(10000, 20000):
       lista.inserir_fim(i)


   tempo_excluir = medir_tempo(lista.excluir, 5)
   for _ in range(100):
       lista.excluir(5)


   tempo_exibir = medir_tempo(lista.exibir)


   return {
       'inicio': tempo_inicio,
       'fim': tempo_fim,
       'excluir': tempo_excluir,
       'exibir': tempo_exibir
   }




resultados = []
for i in range(10):
   print(f"Executando teste {i + 1}/10...")
   resultados.append(executar_teste())


tempos = {
   'inicio': [r['inicio'] for r in resultados],
   'fim': [r['fim'] for r in resultados],
   'excluir': [r['excluir'] for r in resultados],
   'exibir': [r['exibir'] for r in resultados]
}


plt.figure(figsize=(15, 10))


plt.subplot(2, 2, 1)
plt.boxplot(list(tempos.values()), labels=['Inserir Início', 'Inserir Fim', 'Excluir', 'Exibir'])
plt.title('Distribuição dos Tempos por Operação')
plt.ylabel('Tempo (segundos)')
plt.grid(True)


plt.subplot(2, 2, 2)
medias = [np.mean(v) for v in tempos.values()]
plt.bar(['Inserir Início', 'Inserir Fim', 'Excluir', 'Exibir'], medias)
plt.title('Tempo Médio por Operação')
plt.ylabel('Tempo Médio (segundos)')
plt.xticks(rotation=45)
plt.grid(True)


plt.subplot(2, 2, 3)
for operacao, valores in tempos.items():
   plt.plot(range(1, 11), valores, marker='o', label=operacao)
plt.title('Evolução dos Tempos por Teste')
plt.xlabel('Número do Teste')
plt.ylabel('Tempo (segundos)')
plt.legend()
plt.grid(True)


plt.subplot(2, 2, 4)
desvios = [np.std(v) for v in tempos.values()]
plt.bar(['Inserir Início', 'Inserir Fim', 'Excluir', 'Exibir'], desvios)
plt.title('Desvio Padrão por Operação')
plt.ylabel('Desvio Padrão (segundos)')
plt.xticks(rotation=45)
plt.grid(True)


plt.tight_layout()
plt.show()


print("\nEstatísticas das Operações:")
for operacao in tempos:
   valores = tempos[operacao]
   print(f"\n{operacao.capitalize()}:")
   print(f"Média: {np.mean(valores):.6f} segundos")
   print(f"Desvio Padrão: {np.std(valores):.6f} segundos")
   print(f"Mínimo: {min(valores):.6f} segundos")
   print(f"Máximo: {max(valores):.6f} segundos")