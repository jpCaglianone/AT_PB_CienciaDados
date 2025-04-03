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


plt.style.use('default')
plt.rcParams['figure.figsize'] = [15, 10]
plt.rcParams['font.size'] = 10


tamanhos = [100, 250, 500, 750, 1000]
tempos = []
distribuicoes = []


for tamanho in tamanhos:
   estudantes = [
       Estudante(f"Estudante{i}", random.randint(0, 100)) for i in range(tamanho)
   ]


   inicio = time.time()
   estudantes_ordenados = ordena_rapida(estudantes, chave=lambda x: x.nota)
   fim = time.time()


   tempos.append(fim - inicio)
   distribuicoes.append([e.nota for e in estudantes_ordenados])


plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
plt.plot(tamanhos, tempos, marker='o', color='#2ecc71', linewidth=2)
plt.title('Tempo de Execução vs. Tamanho da Entrada')
plt.xlabel('Número de Estudantes')
plt.ylabel('Tempo (segundos)')
plt.grid(True, alpha=0.3)


plt.subplot(2, 2, 2)
plt.hist(distribuicoes[-1], bins=20, color='#3498db', alpha=0.7)
plt.title(f'Distribuição das Notas ({tamanhos[-1]} estudantes)')
plt.xlabel('Nota')
plt.ylabel('Frequência')
plt.grid(True, alpha=0.3)


plt.subplot(2, 2, 3)
plt.boxplot(distribuicoes, labels=tamanhos)
plt.title('Distribuição das Notas por Tamanho da Amostra')
plt.xlabel('Tamanho da Amostra')
plt.ylabel('Notas')
plt.grid(True, alpha=0.3)


plt.subplot(2, 2, 4)
medias = [np.mean(dist) for dist in distribuicoes]
desvios = [np.std(dist) for dist in distribuicoes]


x = np.arange(len(tamanhos))
width = 0.35


plt.bar(x - width / 2, medias, width, label='Média', color='#e74c3c', alpha=0.7)
plt.bar(x + width / 2, desvios, width, label='Desvio Padrão', color='#9b59b6', alpha=0.7)
plt.xticks(x, tamanhos)
plt.title('Estatísticas por Tamanho da Amostra')
plt.xlabel('Tamanho da Amostra')
plt.ylabel('Valor')
plt.legend()
plt.grid(True, alpha=0.3)


plt.tight_layout()
plt.show()


print("\nAnálise Estatística:")
for i, tamanho in enumerate(tamanhos):
   print(f"\nTamanho da amostra: {tamanho}")
   print(f"Tempo de execução: {tempos[i]:.6f} segundos")
   print(f"Média das notas: {np.mean(distribuicoes[i]):.2f}")
   print(f"Desvio padrão: {np.std(distribuicoes[i]):.2f}")
   print(f"Nota mínima: {min(distribuicoes[i])}")
   print(f"Nota máxima: {max(distribuicoes[i])}")


print("\nAnálise de Complexidade:")
razoes = [tempos[i + 1] / tempos[i] for i in range(len(tempos) - 1)]
razoes_tamanho = [tamanhos[i + 1] / tamanhos[i] for i in range(len(tamanhos) - 1)]
print("\nRazões de crescimento:")
for i in range(len(razoes)):
   print(f"Aumento de {tamanhos[i]} para {tamanhos[i + 1]} elementos:")
   print(f"Razão de tempo: {razoes[i]:.2f}")
   print(f"Razão de tamanho: {razoes_tamanho[i]:.2f}")