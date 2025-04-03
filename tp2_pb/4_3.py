

import time
import matplotlib.pyplot as plt
import numpy as np


def hanoi(n, origem, destino, auxiliar, movimentos):
   if n == 1:
       movimentos.append(f"Mova o disco 1 de {origem} para {destino}")
       return


   hanoi(n - 1, origem, auxiliar, destino, movimentos)
   movimentos.append(f"Mova o disco {n} de {origem} para {destino}")
   hanoi(n - 1, auxiliar, destino, origem, movimentos)


def resolver_hanoi_com_tempo(n):
   movimentos = []
   tempo_inicial = time.time()
   hanoi(n, 'A', 'C', 'B', movimentos)
   tempo_final = time.time()
   return movimentos, tempo_final - tempo_inicial


def analisar_hanoi():
   numeros_discos = range(1, 25)
   tempos = []
   contagem_movimentos = []


   for n in numeros_discos:
       movimentos, tempo_execucao = resolver_hanoi_com_tempo(n)
       tempos.append(tempo_execucao)
       contagem_movimentos.append(len(movimentos))
       print(f"\nPara {n} discos:")
       print(f"Tempo de execução: {tempo_execucao:.6f} segundos")
       print(f"Número de movimentos: {len(movimentos)}")


       if n > 10:
           print("Primeiros 5 movimentos:")
           for movimento in movimentos[:5]:
               print(movimento)
           print("...")
           print("Últimos 5 movimentos:")
           for movimento in movimentos[-5:]:
               print(movimento)
       else:
           for movimento in movimentos:
               print(movimento)


   plt.figure(figsize=(12, 6))


   plt.subplot(1, 2, 1)
   plt.plot(numeros_discos, tempos, 'b-', label='Tempo de execução', marker='o')
   plt.xlabel('Número de discos')
   plt.ylabel('Tempo (segundos)')
   plt.title('Tempo de Execução vs. Número de Discos')
   plt.grid(True)
   plt.legend()


   plt.subplot(1, 2, 2)
   plt.plot(numeros_discos, contagem_movimentos, 'g-', label='Número de movimentos', marker='s')
   plt.yscale('log')
   plt.xlabel('Número de discos')
   plt.ylabel('Número de movimentos (log)')
   plt.title('Número de Movimentos vs. Número de Discos')
   plt.grid(True)
   plt.legend()


   complexidade_teorica = [2 ** n - 1 for n in numeros_discos]
   correlacao = np.corrcoef(contagem_movimentos, complexidade_teorica)[0, 1]
   print(f"\nCorrelação com complexidade teórica (2^n - 1): {correlacao:.6f}")


   return plt


plt = analisar_hanoi()
plt.show()


