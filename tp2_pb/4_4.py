

from time import time, perf_counter
from collections import Counter
import matplotlib.pyplot as plt
import string
import random




def gerar_string_aleatoria(tamanho, num_caracteres_unicos):
   caracteres = string.ascii_lowercase[:num_caracteres_unicos]
   return ''.join(random.choice(caracteres) for _ in range(tamanho))




def gerar_permutacoes(string):
   contador = Counter(string)
   resultado = []
   temp = [''] * len(string)


   def permutar_recursivo(posicao, contador):
       if posicao == len(string):
           resultado.append(''.join(temp))
           return


       for char in contador:
           if contador[char] > 0:
               temp[posicao] = char
               contador[char] -= 1
               permutar_recursivo(posicao + 1, contador)
               contador[char] += 1


   permutar_recursivo(0, contador)
   return resultado




def analisar_desempenho():
   tamanhos = range(5, 13)
   tempos_aleatorio = []
   tempos_repetido = []
   quantidades_aleatorio = []
   quantidades_repetido = []


   resultados = []


   for n in tamanhos:
       string_aleatoria = gerar_string_aleatoria(n, min(n, 26))
       string_repetida = 'a' * n


       print(f"\nTestando tamanho {n}")
       print(f"String aleatória: {string_aleatoria}")


       inicio = perf_counter()
       permutacoes_aleatorio = gerar_permutacoes(string_aleatoria)
       tempo_aleatorio = max(perf_counter() - inicio, 1e-10)


       inicio = perf_counter()
       permutacoes_repetido = gerar_permutacoes(string_repetida)
       tempo_repetido = max(perf_counter() - inicio, 1e-10)


       tempos_aleatorio.append(tempo_aleatorio)
       tempos_repetido.append(tempo_repetido)
       quantidades_aleatorio.append(len(permutacoes_aleatorio))
       quantidades_repetido.append(len(permutacoes_repetido))


       resultado = {
           'tamanho': n,
           'string_aleatoria': string_aleatoria,
           'tempo_aleatorio': tempo_aleatorio,
           'qtd_permutacoes_aleatorio': len(permutacoes_aleatorio),
           'tempo_repetido': tempo_repetido,
           'qtd_permutacoes_repetido': len(permutacoes_repetido)
       }
       resultados.append(resultado)


       print(f"\nResultados para tamanho {n}:")
       print(f"String aleatória:")
       print(f"  Tempo: {tempo_aleatorio:.10f} segundos")
       print(f"  Permutações: {len(permutacoes_aleatorio)}")
       print(f"String repetida:")
       print(f"  Tempo: {tempo_repetido:.10f} segundos")
       print(f"  Permutações: {len(permutacoes_repetido)}")


   plt.figure(figsize=(15, 10))


   plt.subplot(2, 2, 1)
   plt.plot(tamanhos, tempos_aleatorio, 'b-', marker='o', label='String Aleatória')
   plt.plot(tamanhos, tempos_repetido, 'r-', marker='s', label='String Repetida')
   plt.title('Tempo de Execução vs Tamanho da Entrada')
   plt.xlabel('Tamanho da String')
   plt.ylabel('Tempo (segundos)')
   plt.yscale('log')
   plt.grid(True)
   plt.legend()


   plt.subplot(2, 2, 2)
   plt.plot(tamanhos, quantidades_aleatorio, 'b-', marker='o', label='String Aleatória')
   plt.plot(tamanhos, quantidades_repetido, 'r-', marker='s', label='String Repetida')
   plt.title('Número de Permutações vs Tamanho da Entrada')
   plt.xlabel('Tamanho da String')
   plt.ylabel('Quantidade de Permutações')
   plt.yscale('log')
   plt.grid(True)
   plt.legend()


   plt.subplot(2, 2, 3)
   eficiencia_aleatorio = [q / t for q, t in zip(quantidades_aleatorio, tempos_aleatorio)]
   eficiencia_repetido = [q / t for q, t in zip(quantidades_repetido, tempos_repetido)]
   plt.plot(tamanhos, eficiencia_aleatorio, 'b-', marker='o', label='String Aleatória')
   plt.plot(tamanhos, eficiencia_repetido, 'r-', marker='s', label='String Repetida')
   plt.title('Eficiência (Permutações por Segundo)')
   plt.xlabel('Tamanho da String')
   plt.ylabel('Permutações/Segundo')
   plt.yscale('log')
   plt.grid(True)
   plt.legend()


   plt.tight_layout()
   return plt, resultados




def testar_casos_extremos():
   casos_teste = [
       'aaaaabbbbb',
       'abcdefghij',
       'aabbccddee',
       'zyxwvutsrq'
   ]


   for texto in casos_teste:
       print(f"\nCaso teste: '{texto}'")
       inicio = perf_counter()
       permutacoes = gerar_permutacoes(texto)
       tempo_total = max(perf_counter() - inicio, 1e-10)


       print(f"Tamanho da entrada: {len(texto)}")
       print(f"Caracteres únicos: {len(set(texto))}")
       print(f"Total de permutações: {len(permutacoes)}")
       print(f"Tempo de execução: {tempo_total:.10f} segundos")
       print(f"Permutações por segundo: {len(permutacoes) / tempo_total:.2f}")




if __name__ == "__main__":
   print("Iniciando testes de casos extremos...")
   testar_casos_extremos()


   print("\nIniciando análise de desempenho...")
   plt, resultados = analisar_desempenho()


   print("\nResumo final:")
   for r in resultados:
       print(f"\nTamanho {r['tamanho']}:")
       print(f"String aleatória: {r['string_aleatoria']}")
       print(f"  Tempo: {r['tempo_aleatorio']:.10f}s")
       print(f"  Permutações: {r['qtd_permutacoes_aleatorio']}")
       print(f"String repetida:")
       print(f"  Tempo: {r['tempo_repetido']:.10f}s")
       print(f"  Permutações: {r['qtd_permutacoes_repetido']}")


   plt.show()




