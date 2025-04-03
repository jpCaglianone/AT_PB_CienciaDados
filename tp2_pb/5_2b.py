import time
import matplotlib.pyplot as plt
from a import ArvoreBinariaParalela




def criar_arvore(tamanho):
   arvore = ArvoreBinariaParalela()
   for i in range(tamanho):
       arvore.inserir(i)
   return arvore




def testar_busca(tamanho):
   arvore = criar_arvore(tamanho)


   start_time = time.time()
   arvore.buscar(tamanho // 2)
   tempo_sequencial = time.time() - start_time


   start_time = time.time()
   arvore.buscar_paralelo(tamanho // 2)
   tempo_paralelo = time.time() - start_time


   return tempo_sequencial, tempo_paralelo




tamanhos = [2 ** i for i in range(1, 10)]
tempos_sequenciais = []
tempos_paralelos = []


for tamanho in tamanhos:
   tempo_sequencial, tempo_paralelo = testar_busca(tamanho)
   tempos_sequenciais.append(tempo_sequencial)
   tempos_paralelos.append(tempo_paralelo)
   print(
       f"Tamanho da árvore: {tamanho}, Tempo sequencial: {tempo_sequencial:.6f} s, Tempo paralelo: {tempo_paralelo:.6f} s")


plt.figure(figsize=(10, 6))


plt.subplot(2, 1, 1)
plt.plot(tamanhos, tempos_sequenciais, label='Busca Sequencial', marker='o', color='b')
plt.plot(tamanhos, tempos_paralelos, label='Busca Paralela', marker='x', color='r')
plt.xlabel('Tamanho da Árvore (número de nós)')
plt.ylabel('Tempo de Execução (segundos)')
plt.title('Comparação de Tempo de Execução entre Busca Sequencial e Paralela')
plt.legend()


plt.subplot(2, 1, 2)
plt.plot(tamanhos, [t2 - t1 for t1, t2 in zip(tempos_sequenciais, tempos_paralelos)],
        label='Diferença de Tempo (Paralela - Sequencial)', marker='s', color='g')
plt.xlabel('Tamanho da Árvore (número de nós)')
plt.ylabel('Diferença de Tempo (segundos)')
plt.title('Diferença de Tempo entre Busca Paralela e Sequencial')
plt.legend()


plt.tight_layout()
plt.show()


media_sequencial = sum(tempos_sequenciais) / len(tempos_sequenciais)
media_paralela = sum(tempos_paralelos) / len(tempos_paralelos)


print("\nMédia de tempos:")
print(f"Média de tempo sequencial: {media_sequencial:.6f} s")
print(f"Média de tempo paralelo: {media_paralela:.6f} s")
