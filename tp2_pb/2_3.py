import random
import time
import matplotlib.pyplot as plt
import numpy as np


class Estudante:
   def __init__(self, nome, nota):
       self.nome = nome
       self.nota = nota


   def __repr__(self):
       return f"{self.nome}: {self.nota}"


def ordena_rapida(lista, chave):
   if len(lista) <= 1:
       return lista


   pivo = lista[0]


   menores = [x for x in lista if chave(x) < chave(pivo)]
   iguais = [x for x in lista if chave(x) == chave(pivo)]
   maiores = [x for x in lista if chave(x) > chave(pivo)]


   return ordena_rapida(menores, chave) + iguais + ordena_rapida(maiores, chave)


def quick_select(lista, k):
   if len(lista) == 1:
       return lista[0]


   pivo = lista[0]


   menores = [x for x in lista if x < pivo]
   iguais = [x for x in lista if x == pivo]
   maiores = [x for x in lista if x > pivo]


   if k <= len(menores):
       return quick_select(menores, k)
   elif k <= len(menores) + len(iguais):
       return pivo
   else:
       return quick_select(maiores, k - len(menores) - len(iguais))


n_listas = 10
n_elementos = 10000
valores_k = [1, 2500, 5000, 7500, 10000]


resultados = {k: [] for k in valores_k}
elementos_encontrados = {k: [] for k in valores_k}


for i in range(n_listas):
   lista = [random.randint(1, 1000) for _ in range(n_elementos)]
   print(f"\nLista {i + 1}:")
   for k in valores_k:
       inicio = time.time()
       k_esimo = quick_select(lista.copy(), k)
       fim = time.time()
       duracao = fim - inicio
       resultados[k].append(duracao)
       elementos_encontrados[k].append(k_esimo)
       print(f"  k={k}, k-ésimo menor elemento: {k_esimo}, Tempo: {duracao:.6f} segundos")


plt.figure(figsize=(15, 10))


plt.subplot(2, 2, 1)
medias = [np.mean(resultados[k]) for k in valores_k]
plt.plot(valores_k, medias, 'o-', linewidth=2)
plt.title('Tempo Médio por Valor de k')
plt.xlabel('Valor de k')
plt.ylabel('Tempo Médio (segundos)')
plt.grid(True)


plt.subplot(2, 2, 2)
plt.boxplot([resultados[k] for k in valores_k], labels=[f'k={k}' for k in valores_k])
plt.title('Distribuição dos Tempos por k')
plt.ylabel('Tempo (segundos)')
plt.grid(True)


plt.subplot(2, 2, 3)
for k in valores_k:
   plt.scatter([k] * len(elementos_encontrados[k]), elementos_encontrados[k], alpha=0.5)
plt.title('Elementos Encontrados por k')
plt.xlabel('Valor de k')
plt.ylabel('Valor do Elemento')
plt.grid(True)


plt.subplot(2, 2, 4)
tempos_normalizados = []
for k in valores_k:
   tempos_k = np.array(resultados[k])
   tempos_normalizados.append(tempos_k / np.mean(tempos_k))
plt.boxplot(tempos_normalizados, labels=[f'k={k}' for k in valores_k])
plt.title('Tempos Normalizados por k')
plt.ylabel('Tempo Normalizado')
plt.grid(True)


plt.tight_layout()
plt.show()


print("\nEstatísticas por valor de k:")
for k in valores_k:
   tempos = resultados[k]
   elementos = elementos_encontrados[k]
   print(f"\nk = {k}")
   print(f"Tempo médio: {np.mean(tempos):.6f} segundos")
   print(f"Desvio padrão: {np.std(tempos):.6f} segundos")
   print(f"Tempo mínimo: {min(tempos):.6f} segundos")
   print(f"Tempo máximo: {max(tempos):.6f} segundos")
   print(f"Média dos elementos encontrados: {np.mean(elementos):.2f}")




