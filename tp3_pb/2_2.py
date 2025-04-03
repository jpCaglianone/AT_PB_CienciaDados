

import numpy as np
import multiprocessing as mp
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor




def multiplicar_linha(args):
   linha, matriz_b = args
   return np.dot(linha, matriz_b)




def multiplicacao_matriz_paralela(matriz_a, matriz_b):
   with ProcessPoolExecutor() as executor:
       args = [(linha, matriz_b) for linha in matriz_a]
       resultado = list(executor.map(multiplicar_linha, args))
   return np.array(resultado)




def main():
   matriz_a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
   matriz_b = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])


   inicio_tempo = time.time()
   resultado_paralelo = multiplicacao_matriz_paralela(matriz_a, matriz_b)
   tempo_paralelo = time.time() - inicio_tempo


   inicio_tempo = time.time()
   resultado_sequencial = np.dot(matriz_a, matriz_b)
   tempo_sequencial = time.time() - inicio_tempo


   plt.figure(figsize=(12, 5))
   plt.subplot(1, 2, 1)
   plt.imshow(resultado_paralelo, cmap='viridis')
   plt.title('Resultado Paralelo')
   plt.colorbar()


   plt.subplot(1, 2, 2)
   plt.plot(['Paralelo', 'Sequencial'], [tempo_paralelo, tempo_sequencial],
            marker='o', linestyle='-', linewidth=2)
   plt.title('Tempo de Execução')
   plt.ylabel('Tempo (segundos)')
   plt.grid(True)
   plt.tight_layout()
   plt.savefig('matriz_multiplicacao.png')
   plt.close()


   with open('analise_multiplicacao_matriz.txt', 'w') as f:
       f.write('Análise da Multiplicação de Matrizes\n\n')
       f.write(f'Matriz A:\n{matriz_a}\n\n')
       f.write(f'Matriz B:\n{matriz_b}\n\n')
       f.write(f'Resultado:\n{resultado_paralelo}\n\n')
       f.write(f'Tempo de execução paralela: {tempo_paralelo:.6f} segundos\n')
       f.write(f'Tempo de execução sequencial: {tempo_sequencial:.6f} segundos\n')
       f.write(f'Aceleração: {tempo_sequencial / tempo_paralelo:.2f}x\n')




if __name__ == '__main__':
   main()
