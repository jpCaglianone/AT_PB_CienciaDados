

import time
import matplotlib.pyplot as plt
import numpy as np




def troco_minimo(moedas, valor):
   dp = [float('inf')] * (valor + 1)
   moedas_usadas = [[] for _ in range(valor + 1)]
   dp[0] = 0


   for i in range(1, valor + 1):
       for moeda in moedas:
           if moeda <= i:
               if dp[i - moeda] + 1 < dp[i]:
                   dp[i] = dp[i - moeda] + 1
                   moedas_usadas[i] = moedas_usadas[i - moeda] + [moeda]


   return dp[valor], moedas_usadas[valor]




def analisar_performance():
   moedas_br = [1, 5, 10, 25, 50, 100]
   valores_teste = list(range(100, 10001, 100))
   tempos = []


   for valor in valores_teste:
       inicio = time.time()
       troco_minimo(moedas_br, valor)
       fim = time.time()
       tempos.append((fim - inicio) * 1000)  # Converter para milissegundos


   plt.figure(figsize=(10, 6))
   plt.plot(valores_teste, tempos, 'b-', label='Tempo de Execução')
   plt.scatter(valores_teste, tempos, color='red', alpha=0.5)


   z = np.polyfit(valores_teste, tempos, 1)
   p = np.poly1d(z)
   plt.plot(valores_teste, p(valores_teste), "r--", alpha=0.8, label='Tendência Linear')


   plt.xlabel('Valor do Troco (centavos)')
   plt.ylabel('Tempo de Execução (ms)')
   plt.title('Análise de Performance do Algoritmo de Troco Mínimo')
   plt.grid(True, alpha=0.3)
   plt.legend()


   coef_angular = z[0]
   print(f"Coeficiente angular da linha de tendência: {coef_angular:.6f} ms/centavo")


   plt.show()




def testar_casos():
   moedas_br = [1, 5, 10, 25, 50, 100]
   casos_teste = [
       (43, "R$ 0,43"),
       (99, "R$ 0,99"),
       (178, "R$ 1,78"),
       (468, "R$ 4,68")
   ]


   print("Testes com moedas brasileiras:", moedas_br)
   print("-" * 50)


   for valor, valor_formatado in casos_teste:
       inicio = time.time()
       qtd, moedas = troco_minimo(moedas_br, valor)
       fim = time.time()


       print(f"Valor: {valor_formatado}")
       print(f"Quantidade mínima de moedas: {qtd}")
       print(f"Moedas usadas: {moedas}")
       print(f"Tempo de execução: {((fim - inicio) * 1000):.4f} ms")
       print("-" * 50)




if __name__ == "__main__":
   print("Executando testes de casos específicos...")
   testar_casos()


   print("\nIniciando análise de performance...")
   analisar_performance()
