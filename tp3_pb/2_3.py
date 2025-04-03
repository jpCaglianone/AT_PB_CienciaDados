





import numpy as np
import multiprocessing as mp
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor




def eh_primo(n):
   if n < 2:
       return False
   for i in range(2, int(np.sqrt(n)) + 1):
       if n % i == 0:
           return False
   return True




def contar_primos_intervalo(tupla_intervalo):
   inicio, fim = tupla_intervalo
   return sum(1 for n in range(inicio, fim) if eh_primo(n))




def contador_primos_paralelo(inicio, fim, num_processos):
   tamanho_pedaco = (fim - inicio) // num_processos
   intervalos = [(i, i + tamanho_pedaco) for i in range(inicio, fim, tamanho_pedaco)]
   intervalos[-1] = (intervalos[-1][0], fim)


   with ProcessPoolExecutor() as executor:
       resultados = list(executor.map(contar_primos_intervalo, intervalos))
   return sum(resultados)




def main():
   inicio, fim = 1, 100001
   num_processos = mp.cpu_count()


   tempo_inicial = time.time()
   contagem_paralela = contador_primos_paralelo(inicio, fim, num_processos)
   tempo_paralelo = time.time() - tempo_inicial


   resultados_pedacos = []
   tamanho_pedaco = (fim - inicio) // num_processos
   for i in range(inicio, fim, tamanho_pedaco):
       fim_pedaco = min(i + tamanho_pedaco, fim)
       contagem = contar_primos_intervalo((i, fim_pedaco))
       resultados_pedacos.append(contagem)


   plt.figure(figsize=(12, 6))
   plt.plot(range(len(resultados_pedacos)), resultados_pedacos,
            marker='o', linestyle='-', linewidth=2)
   plt.title('Distribuição de Números Primos por Pedaço')
   plt.xlabel('Pedaço')
   plt.ylabel('Quantidade de Primos')
   plt.grid(True)
   plt.savefig('distribuicao_primos.png')
   plt.close()


   with open('analise_primos.txt', 'w') as f:
       f.write('Análise da Contagem de Números Primos\n\n')
       f.write(f'Intervalo analisado: {inicio} a {fim - 1}\n')
       f.write(f'Número de processos: {num_processos}\n')
       f.write(f'Total de números primos encontrados: {contagem_paralela}\n')
       f.write(f'Tempo de execução: {tempo_paralelo:.2f} segundos\n')
       f.write('\nDistribuição por pedaço:\n')
       for i, contagem in enumerate(resultados_pedacos):
           f.write(f'Pedaço {i}: {contagem} primos\n')




if __name__ == '__main__':
   main()






