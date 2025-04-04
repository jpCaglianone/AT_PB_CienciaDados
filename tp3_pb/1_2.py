import matplotlib.pyplot as plt
import numpy as np
import time
import threading


class No:
   def __init__(self, valor):
       self.valor = valor
       self.esquerda = None
       self.direita = None


class ArvoreBinaria:
   def __init__(self):
       self.raiz = None


   def inserir(self, valor):
       if not self.raiz:
           self.raiz = No(valor)
           return


       atual = self.raiz
       while True:
           if valor < atual.valor:
               if atual.esquerda is None:
                   atual.esquerda = No(valor)
                   break
               atual = atual.esquerda
           else:
               if atual.direita is None:
                   atual.direita = No(valor)
                   break
               atual = atual.direita


   def em_ordem(self, no, resultado=None):
       if resultado is None:
           resultado = []
       if no:
           self.em_ordem(no.esquerda, resultado)
           resultado.append(no.valor)
           self.em_ordem(no.direita, resultado)
       return resultado


   def buscar(self, no, valor):
       if no is None:
           return None
       if valor == no.valor:
           return no
       elif valor < no.valor:
           return self.buscar(no.esquerda, valor)
       else:
           return self.buscar(no.direita, valor)


   def parallel_search(self, valor):
       resultados = []
       lock = threading.Lock()


       def buscar_subarvore(no):
           nonlocal resultados
           if no is None:
               with lock:
                   resultados.append(False)
               return
           if no.valor == valor:
               with lock:
                   resultados.append(True)
               return
           buscar_subarvore(no.esquerda)
           buscar_subarvore(no.direita)


       thread_esquerda = threading.Thread(target=buscar_subarvore, args=(self.raiz.esquerda,))
       thread_direita = threading.Thread(target=buscar_subarvore, args=(self.raiz.direita,))


       thread_esquerda.start()
       thread_direita.start()


       thread_esquerda.join()
       thread_direita.join()


       return any(resultados)


def criar_arvore_balanceada(tamanho):
   valores = sorted(np.random.choice(range(1, tamanho * 2), tamanho, replace=False))
   arvore = ArvoreBinaria()
   def inserir_no_meio(arr):
       if not arr:
           return
       meio = len(arr) // 2
       arvore.inserir(arr[meio])
       inserir_no_meio(arr[:meio])
       inserir_no_meio(arr[meio + 1:])
   inserir_no_meio(valores)
   return arvore, valores


def realizar_teste_busca(tamanho_arvore, num_buscas):
   arvore, valores = criar_arvore_balanceada(tamanho_arvore)
   valores_busca = np.random.choice(valores, num_buscas)


   tempos_sequencial = []
   tempos_paralelo = []


   for valor in valores_busca:
       start = time.time()
       arvore.buscar(arvore.raiz, valor)
       tempos_sequencial.append(time.time() - start)


       start = time.time()
       arvore.parallel_search(valor)
       tempos_paralelo.append(time.time() - start)


   return np.mean(tempos_sequencial), np.mean(tempos_paralelo)


def realizar_todos_os_testes():
   tamanhos_arvore = [100, 500, 1000, 5000, 10000]
   num_buscas = 100


   tempos_sequencial = []
   tempos_paralelo = []


   for tamanho in tamanhos_arvore:
       tempo_seq, tempo_par = realizar_teste_busca(tamanho, num_buscas)
       tempos_sequencial.append(tempo_seq)
       tempos_paralelo.append(tempo_par)


   return tamanhos_arvore, tempos_sequencial, tempos_paralelo


tamanhos_arvore, tempos_sequencial, tempos_paralelo = realizar_todos_os_testes()


plt.figure(figsize=(10,6))
plt.plot(tamanhos_arvore, tempos_sequencial, label="Busca Sequencial", color='blue')
plt.plot(tamanhos_arvore, tempos_paralelo, label="Busca Paralela", color='red')
plt.xlabel('Tamanho da Árvore')
plt.ylabel('Tempo Médio (s)')
plt.title('Desempenho de Busca na Árvore Binária de Busca')
plt.legend()
plt.grid(True)
plt.savefig("tp3_1.2.png")


with open("tp3_1.2.txt", "w") as f:
   f.write("Tamanho da Árvore\tBusca Sequencial (s)\tBusca Paralela (s)\n")
   for i in range(len(tamanhos_arvore)):
       f.write(f"{tamanhos_arvore[i]}\t{tempos_sequencial[i]:.6f}\t{tempos_paralelo[i]:.6f}\n")