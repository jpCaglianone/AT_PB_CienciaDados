

import random
import time
import matplotlib.pyplot as plt
import numpy as np




def ordena_rapida(lista, tipo_pivo="primeiro"):
   if len(lista) <= 1:
       return lista


   if tipo_pivo == "primeiro":
       pivo = lista[0]
   elif tipo_pivo == "ultimo":
       pivo = lista[-1]
   elif tipo_pivo == "mediano":
       pivo = lista[len(lista) // 2]
   else:
       raise ValueError("Tipo de pivo invalido. Escolha 'primeiro', 'ultimo' ou 'mediano'.")


   menores = [x for x in lista if x < pivo]
   iguais = [x for x in lista if x == pivo]
   maiores = [x for x in lista if x > pivo]


   return ordena_rapida(menores, tipo_pivo) + iguais + ordena_rapida(maiores, tipo_pivo)


plt.style.use('default')
plt.rcParams['figure.figsize'] = [15, 10]
plt.rcParams['font.size'] = 10


dados = [random.randint(1, 100000) for _ in range(50000)]
tipos_pivo = ["primeiro", "ultimo", "mediano"]
resultados_desempenho = {"primeiro": [], "ultimo": [], "mediano": []}


for i in range(1, 21):
   print(f"Teste {i}:")
   for pivo in tipos_pivo:
       inicio = time.time()
       dados_ordenados = ordena_rapida(dados.copy(), pivo)
       fim = time.time()
       duracao = fim - inicio
       resultados_desempenho[pivo].append(duracao)
       print(f"  Pivo: {pivo}, Tempo: {duracao:.6f} segundos")


medias = {pivo: np.mean(tempos) for pivo, tempos in resultados_desempenho.items()}
desvios = {pivo: np.std(tempos) for pivo, tempos in resultados_desempenho.items()}


cores = ['#2ecc71', '#e74c3c', '#3498db']


plt.subplot(2, 2, 1)
for i, pivo in enumerate(tipos_pivo):
   plt.plot(range(1, 21), resultados_desempenho[pivo], marker='o',
            label=pivo, color=cores[i], linewidth=2)
plt.title('Evolução do Tempo de Execução por Teste')
plt.xlabel('Número do Teste')
plt.ylabel('Tempo (segundos)')
plt.legend()
plt.grid(True, alpha=0.3)


plt.subplot(2, 2, 2)
bars = plt.bar(medias.keys(), medias.values(), color=cores)
plt.title('Tempo Médio de Execução por Tipo de Pivô')
plt.ylabel('Tempo Médio (segundos)')
for bar in bars:
   height = bar.get_height()
   plt.text(bar.get_x() + bar.get_width() / 2., height,
            f'{height:.6f}s',
            ha='center', va='bottom')


plt.subplot(2, 2, 3)
bp = plt.boxplot([resultados_desempenho[pivo] for pivo in tipos_pivo],
                labels=tipos_pivo, patch_artist=True)
for i, box in enumerate(bp['boxes']):
   box.set(facecolor=cores[i], alpha=0.7)
plt.title('Distribuição dos Tempos de Execução')
plt.ylabel('Tempo (segundos)')


plt.subplot(2, 2, 4)
bars = plt.bar(desvios.keys(), desvios.values(), color=cores)
plt.title('Desvio Padrão dos Tempos de Execução')
plt.ylabel('Desvio Padrão (segundos)')


for bar in bars:
   height = bar.get_height()
   plt.text(bar.get_x() + bar.get_width() / 2., height,
            f'{height:.6f}s',
            ha='center', va='bottom')


plt.tight_layout()
plt.show()


print("\nAnálise Estatística:")
for pivo in tipos_pivo:
   print(f"\nTipo de pivô: {pivo}")
   print(f"Média: {medias[pivo]:.6f} segundos")
   print(f"Desvio Padrão: {desvios[pivo]:.6f} segundos")
   print(f"Tempo Mínimo: {min(resultados_desempenho[pivo]):.6f} segundos")
   print(f"Tempo Máximo: {max(resultados_desempenho[pivo]):.6f} segundos")


pivo_melhor = min(medias, key=medias.get)
pivo_pior = max(medias, key=medias.get)


print(f"\nMelhor pivô: {pivo_melhor}")
print(f"Pior pivô: {pivo_pior}")
print(f"Diferença de desempenho: {(medias[pivo_pior] - medias[pivo_melhor]):.6f} segundos")
