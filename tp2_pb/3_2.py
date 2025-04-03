

import time
import matplotlib.pyplot as plt
import numpy as np




class DNode:
   def __init__(self, value):
       self.value = value
       self.next = None
       self.prev = None




class DoublyLinkedList:
   def __init__(self):
       self.head = None
       self.tail = None


   def inserir_inicio(self, value):
       new_node = DNode(value)
       if not self.head:
           self.head = new_node
           self.tail = new_node
       else:
           new_node.next = self.head
           self.head.prev = new_node
           self.head = new_node


   def inserir_fim(self, value):
       new_node = DNode(value)
       if not self.tail:
           self.head = new_node
           self.tail = new_node
       else:
           new_node.prev = self.tail
           self.tail.next = new_node
           self.tail = new_node


   def excluir(self, pos):
       if not self.head:
           return
       current = self.head
       count = 0
       while current:
           if count == pos:
               if current.prev:
                   current.prev.next = current.next
               if current.next:
                   current.next.prev = current.prev
               if current == self.head:
                   self.head = current.next
               if current == self.tail:
                   self.tail = current.prev
               return
           current = current.next
           count += 1


   def exibir(self):
       elements = []
       current = self.head
       while current:
           elements.append(current.value)
           current = current.next
       return elements


   def exibir_reversa(self):
       elements = []
       current = self.tail
       while current:
           elements.append(current.value)
           current = current.prev
       return elements




def medir_tempo(operacao, *args):
   start_time = time.time()
   operacao(*args)
   end_time = time.time()
   return end_time - start_time




todos_tempos = {
   'inicio': [],
   'fim': [],
   'excluir': [],
   'exibir': [],
   'reversa': []
}




def main():
   lista = DoublyLinkedList()


   for i in range(10000):
       lista.inserir_inicio(i)


   tempo_inicio = medir_tempo(lista.inserir_inicio, 5)
   todos_tempos['inicio'].append(tempo_inicio)


   for i in range(10000, 20000):
       lista.inserir_fim(i)


   tempo_fim = medir_tempo(lista.inserir_fim, 15000)
   todos_tempos['fim'].append(tempo_fim)


   tempo_excluir = medir_tempo(lista.excluir, 5)
   todos_tempos['excluir'].append(tempo_excluir)


   tempo_exibir = medir_tempo(lista.exibir)
   todos_tempos['exibir'].append(tempo_exibir)


   tempo_exibir_reversa = medir_tempo(lista.exibir_reversa)
   todos_tempos['reversa'].append(tempo_exibir_reversa)


   print("Tempo para inserir no início:", tempo_inicio)
   print("Tempo para inserir no fim:", tempo_fim)
   print("Tempo para excluir na posição 5:", tempo_excluir)
   print("Tempo para exibir a lista:", tempo_exibir)
   print("Tempo para exibir a lista reversa:", tempo_exibir_reversa)




for i in range(10):
   main()


plt.figure(figsize=(12, 6))
operacoes = list(todos_tempos.keys())
medias = [np.mean(todos_tempos[op]) for op in operacoes]


plt.bar(operacoes, medias)
plt.title('Tempo Médio por Operação')
plt.ylabel('Tempo (segundos)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
