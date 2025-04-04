import random
import matplotlib.pyplot as plt
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


   def pre_ordem(self, no, resultado=None):
       if resultado is None:
           resultado = []
       if no:
           resultado.append(no.valor)
           self.pre_ordem(no.esquerda, resultado)
           self.pre_ordem(no.direita, resultado)
       return resultado


   def pos_ordem(self, no, resultado=None):
       if resultado is None:
           resultado = []
       if no:
           self.pos_ordem(no.esquerda, resultado)
           self.pos_ordem(no.direita, resultado)
           resultado.append(no.valor)
       return resultado


   # Novo método para busca sequencial
   def sequential_search(self, no, valor):
       if no is None:
           return False
       if no.valor == valor:
           return True
       elif valor < no.valor:
           return self.sequential_search(no.esquerda, valor)
       else:
           return self.sequential_search(no.direita, valor)


   # Novo método para busca paralela (usando threading)
   def parallel_search(self, valor):
       threads = []
       resultados = []


       def buscar_subarvore(no):
           if no is None:
               resultados.append(False)
               return
           if no.valor == valor:
               resultados.append(True)
               return
           buscar_subarvore(no.esquerda)
           buscar_subarvore(no.direita)


       # Criando threads para busca nas subárvores
       thread_esquerda = threading.Thread(target=buscar_subarvore, args=(self.raiz.esquerda,))
       thread_direita = threading.Thread(target=buscar_subarvore, args=(self.raiz.direita,))


       threads.append(thread_esquerda)
       threads.append(thread_direita)


       # Iniciando as threads
       thread_esquerda.start()
       thread_direita.start()

       for thread in threads:
           thread.join()

       return any(resultados)




def criar_arvore_balanceada(tamanho):
   valores = sorted(random.sample(range(1, tamanho * 2), tamanho))
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


def salvar_resultados(tamanhos_arvore, tempos_sequenciais, tempos_paralelos):
   with open("tp3_1.1.txt", "w") as f:
       f.write("Análise de Desempenho de Busca em Árvore Binária\n")
       f.write("=" * 50 + "\n\n")
       f.write("Parâmetros do Teste:\n")
       f.write("- 100 buscas por tamanho de árvore\n")
       f.write("- Árvores binárias balanceadas\n\n")
       f.write("Resultados:\n")
       f.write("-" * 30 + "\n")


       for i, tamanho in enumerate(tamanhos_arvore):
           f.write(f"\nTamanho da Árvore: {tamanho}\n")
           f.write(f"Tempo de Busca Sequencial: {tempos_sequenciais[i]:.4f} segundos\n")
           f.write(f"Tempo de Busca Paralela: {tempos_paralelos[i]:.4f} segundos\n")
           speedup = tempos_sequenciais[i] / tempos_paralelos[i]
           f.write(f"Speedup: {speedup:.2f}x\n")


   plt.figure(figsize=(12, 6))


   plt.subplot(1, 2, 1)
   plt.plot(tamanhos_arvore, tempos_sequenciais, 'b-o', label='Sequencial')
   plt.plot(tamanhos_arvore, tempos_paralelos, 'r-o', label='Paralela')
   plt.title('Tempo de Busca vs Tamanho da Árvore')
   plt.xlabel('Número de Nós')
   plt.ylabel('Tempo (segundos)')
   plt.legend()
   plt.grid(True)


   plt.subplot(1, 2, 2)
   speedups = [s / p for s, p in zip(tempos_sequenciais, tempos_paralelos)]
   plt.plot(tamanhos_arvore, speedups, 'g-o')
   plt.title('Speedup da Busca Paralela')
   plt.xlabel('Número de Nós')
   plt.ylabel('Speedup (Sequencial/Paralela)')
   plt.grid(True)


   plt.tight_layout()
   plt.savefig('tp3_1.1.png', dpi=300, bbox_inches='tight')
   plt.close()




def realizar_teste_desempenho(tamanho_arvore, num_buscas):
   arvore, valores = criar_arvore_balanceada(tamanho_arvore)
   valores_busca = random.choices(valores, k=num_buscas)


   inicio = time.time()
   for valor in valores_busca:
       arvore.sequential_search(arvore.raiz, valor)
   tempo_sequencial = time.time() - inicio


   inicio = time.time()
   for valor in valores_busca:
       arvore.parallel_search(valor)
   tempo_paralelo = time.time() - inicio


   return tempo_sequencial, tempo_paralelo




def realizar_todos_os_testes():
   tamanhos_arvore = [100, 500, 1000, 5000, 10000]
   num_buscas = 100
   resultados_sequenciais = []
   resultados_paralelos = []


   for tamanho in tamanhos_arvore:
       print(f"Testando com tamanho de árvore {tamanho}...")
       tempo_seq, tempo_par = realizar_teste_desempenho(tamanho, num_buscas)
       resultados_sequenciais.append(tempo_seq)
       resultados_paralelos.append(tempo_par)
       print(f"Tempo Sequencial: {tempo_seq:.4f}s")
       print(f"Tempo Paralelo: {tempo_par:.4f}s")


   salvar_resultados(tamanhos_arvore, resultados_sequenciais, resultados_paralelos)


if __name__ == "__main__":
   arvore = ArvoreBinaria()
   for valor in [50, 30, 70, 20, 40, 60, 80]:
       arvore.inserir(valor)


   print("Em ordem:", arvore.em_ordem(arvore.raiz))
   print("Pré-ordem:", arvore.pre_ordem(arvore.raiz))
   print("Pós-ordem:", arvore.pos_ordem(arvore.raiz))


   print("\nIniciando testes de desempenho...")
   realizar_todos_os_testes()


