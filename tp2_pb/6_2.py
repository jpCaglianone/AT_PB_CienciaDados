

from time import perf_counter
import matplotlib.pyplot as plt
import random
import string




def encontrar_subsequencia(str1, str2):
   m, n = len(str1), len(str2)
   matriz = [[0] * (n + 1) for _ in range(m + 1)]


   for i in range(1, m + 1):
       for j in range(1, n + 1):
           if str1[i - 1] == str2[j - 1]:
               matriz[i][j] = matriz[i - 1][j - 1] + 1
           else:
               matriz[i][j] = max(matriz[i - 1][j], matriz[i][j - 1])


   subsequencia = []
   i, j = m, n
   while i > 0 and j > 0:
       if str1[i - 1] == str2[j - 1]:
           subsequencia.append(str1[i - 1])
           i -= 1
           j -= 1
       elif matriz[i - 1][j] > matriz[i][j - 1]:
           i -= 1
       else:
           j -= 1


   return matriz[m][n], ''.join(reversed(subsequencia))




def visualizar_matriz(str1, str2):
   m, n = len(str1), len(str2)
   matriz = [[0] * (n + 1) for _ in range(m + 1)]


   for i in range(1, m + 1):
       for j in range(1, n + 1):
           if str1[i - 1] == str2[j - 1]:
               matriz[i][j] = matriz[i - 1][j - 1] + 1
           else:
               matriz[i][j] = max(matriz[i - 1][j], matriz[i][j - 1])


   print("\nMatriz de programação dinâmica:")
   print("   ", end=" ")
   print("   ".join(str2))
   for i in range(m + 1):
       if i == 0:
           print(" ", end=" ")
       else:
           print(str1[i - 1], end=" ")
       for j in range(n + 1):
           print(f"{matriz[i][j]:2d}", end=" ")
       print()
   return matriz




def gerar_string_aleatoria(tamanho):
   return ''.join(random.choices(string.ascii_lowercase, k=tamanho))




def testar_casos():
   casos_teste = [
       ("abcde", "ace", "Caso básico"),
       ("AGGTAB", "GXTXAYB", "DNA exemplo"),
       ("programa", "algoritmo", "Palavras relacionadas"),
       ("python", "javascript", "Linguagens de programação"),
       ("11111", "11111", "Strings iguais")
   ]


   for str1, str2, descricao in casos_teste:
       print(f"\nTestando: {descricao}")
       print(f"String 1: {str1}")
       print(f"String 2: {str2}")


       inicio = perf_counter()
       matriz = visualizar_matriz(str1, str2)
       comprimento, subsequencia = encontrar_subsequencia(str1, str2)
       tempo = perf_counter() - inicio


       print(f"Comprimento da maior subsequência: {comprimento}")
       print(f"Subsequência encontrada: {subsequencia}")
       print(f"Tempo de execução: {tempo:.6f} segundos")




def analisar_desempenho():
   tamanhos = range(5, 201, 20)
   tempos = []
   comprimentos = []


   for n in tamanhos:
       str1 = gerar_string_aleatoria(n)
       str2 = gerar_string_aleatoria(n)


       inicio = perf_counter()
       comprimento, _ = encontrar_subsequencia(str1, str2)
       tempo = perf_counter() - inicio


       tempos.append(tempo)
       comprimentos.append(comprimento)


       print(f"\nTamanho {n}:")
       print(f"Tempo: {tempo:.6f} segundos")
       print(f"Comprimento da subsequência: {comprimento}")


   plt.figure(figsize=(12, 5))


   plt.subplot(1, 2, 1)
   plt.plot(tamanhos, tempos, 'b-', marker='o')
   plt.title('Tempo de Execução vs Tamanho das Strings')
   plt.xlabel('Tamanho das Strings')
   plt.ylabel('Tempo (segundos)')
   plt.grid(True)


   plt.subplot(1, 2, 2)
   plt.plot(tamanhos, comprimentos, 'r-', marker='o')
   plt.title('Comprimento da Subsequência vs Tamanho das Strings')
   plt.xlabel('Tamanho das Strings')
   plt.ylabel('Comprimento da Subsequência')
   plt.grid(True)


   plt.tight_layout()
   return plt




if __name__ == "__main__":
   print("Executando testes com casos predefinidos...")
   testar_casos()


   print("\nIniciando análise de desempenho...")
   plt = analisar_desempenho()
   plt.show()
