import numpy as np
import multiprocessing as mp
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor




def soma_paralela(pedaco):
   return np.sum(pedaco)




def main():
   numeros = np.arange(1, 10_000_001)
   num_processos = mp.cpu_count()
   pedacos = np.array_split(numeros, num_processos)


   tempo_inicial = time.time()
   with ProcessPoolExecutor() as executor:
       somas_parciais = list(executor.map(soma_paralela, pedacos))
   soma_total = sum(somas_parciais)
   tempo_final = time.time()


   inicio_sequencial = time.time()
   soma_sequencial = np.sum(numeros)
   fim_sequencial = time.time()


   tempo_paralelo = tempo_final - tempo_inicial
   tempo_sequencial = fim_sequencial - inicio_sequencial


   plt.figure(figsize=(10, 6))
   plt.plot(['Paralelo', 'Sequencial'], [tempo_paralelo, tempo_sequencial], marker='o')
   plt.title('Comparação de Tempo de Execução')
   plt.ylabel('Tempo (segundos)')
   plt.grid(True)
   plt.savefig('soma_paralela_tempo.png')
   plt.close()


   with open('analise_soma_paralela.txt', 'w') as f:
       f.write(f'Análise da Soma Paralela\n\n')
       f.write(f'Número de processos utilizados: {num_processos}\n')
       f.write(f'Soma total: {soma_total}\n')
       f.write(f'Tempo de execução paralela: {tempo_paralelo:.4f} segundos\n')
       f.write(f'Tempo de execução sequencial: {tempo_sequencial:.4f} segundos\n')
       f.write(f'Aceleração: {tempo_sequencial / tempo_paralelo:.2f}x\n')




if __name__ == '__main__':
   main()




