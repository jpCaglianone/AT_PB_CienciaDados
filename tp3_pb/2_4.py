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




def contador_primos_sequencial(inicio, fim):
   return sum(1 for n in range(inicio, fim) if eh_primo(n))




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




def testar_desempenho(inicio, fim, num_testes=3):
   num_processos = mp.cpu_count()
   tempos_paralelos = []
   tempos_sequenciais = []


   for _ in range(num_testes):
       tempo_inicial = time.time()
       contagem_paralela = contador_primos_paralelo(inicio, fim, num_processos)
       tempos_paralelos.append(time.time() - tempo_inicial)


       tempo_inicial = time.time()
       contagem_sequencial = contador_primos_sequencial(inicio, fim)
       tempos_sequenciais.append(time.time() - tempo_inicial)


   return (
       np.mean(tempos_paralelos),
       np.std(tempos_paralelos),
       np.mean(tempos_sequenciais),
       np.std(tempos_sequenciais),
       contagem_paralela
   )




def main():
   inicio, fim = 1, 100001
   media_paralela, desvio_paralelo, media_sequencial, desvio_sequencial, total_primos = testar_desempenho(inicio, fim)


   plt.figure(figsize=(12, 6))


   plt.subplot(1, 2, 1)
   plt.plot(['Paralelo', 'Sequencial'], [media_paralela, media_sequencial],
            marker='o', linestyle='-', linewidth=2)
   plt.errorbar(['Paralelo', 'Sequencial'], [media_paralela, media_sequencial],
                yerr=[desvio_paralelo, desvio_sequencial], fmt='none', color='black', capsize=5)
   plt.title('Comparação de Tempo de Execução')
   plt.ylabel('Tempo (segundos)')
   plt.grid(True)


   plt.subplot(1, 2, 2)
   aceleracao = media_sequencial / media_paralela
   eficiencia = aceleracao / mp.cpu_count()
   metricas = [aceleracao, eficiencia]
   plt.plot(['Aceleração', 'Eficiência'], metricas, marker='o', linestyle='-', linewidth=2)
   plt.title('Métricas de Desempenho')
   plt.grid(True)


   plt.tight_layout()
   plt.savefig('comparacao_desempenho.png')
   plt.close()


   tamanhos = [10000, 50000, 100000]
   tempos_paralelos = []
   tempos_sequenciais = []


   for tamanho in tamanhos:
       media_p, _, media_s, _, _ = testar_desempenho(1, tamanho + 1, num_testes=1)
       tempos_paralelos.append(media_p)
       tempos_sequenciais.append(media_s)


   plt.figure(figsize=(8, 6))
   plt.plot(tamanhos, tempos_paralelos, marker='o', label='Paralelo', linewidth=2)
   plt.plot(tamanhos, tempos_sequenciais, marker='s', label='Sequencial', linewidth=2)
   plt.xlabel('Tamanho do Intervalo')
   plt.ylabel('Tempo (segundos)')
   plt.title('Escalabilidade')
   plt.legend()
   plt.grid(True)
   plt.savefig('escalabilidade.png')
   plt.close()


   with open('analise_desempenho.txt', 'w') as f:
       f.write('Análise de Desempenho - Contagem de Números Primos\n\n')
       f.write(f'Intervalo analisado: {inicio} a {fim - 1}\n')
       f.write(f'Número de processos: {mp.cpu_count()}\n')
       f.write(f'Total de números primos encontrados: {total_primos}\n\n')
       f.write('Tempos de Execução:\n')
       f.write(f'Paralelo: {media_paralela:.2f} ± {desvio_paralelo:.2f} segundos\n')
       f.write(f'Sequencial: {media_sequencial:.2f} ± {desvio_sequencial:.2f} segundos\n\n')
       f.write('Métricas de Desempenho:\n')
       f.write(f'Aceleração: {aceleracao:.2f}x\n')
       f.write(f'Eficiência: {eficiencia:.2f}\n\n')
       f.write('Análise de Escalabilidade:\n')
       for tamanho, tempo_p, tempo_s in zip(tamanhos, tempos_paralelos, tempos_sequenciais):
           f.write(f'Tamanho {tamanho}: Paralelo = {tempo_p:.2f}s, Sequencial = {tempo_s:.2f}s\n')




if __name__ == '__main__':
   main()


