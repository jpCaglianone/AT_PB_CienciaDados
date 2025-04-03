

from time import perf_counter
import matplotlib.pyplot as plt
import random




def mochila_pd(capacidade, pesos, valores):
   n = len(pesos)
   tabela = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]
   items_selecionados = [[False for _ in range(capacidade + 1)] for _ in range(n + 1)]


   for i in range(1, n + 1):
       for w in range(capacidade + 1):
           if pesos[i - 1] <= w:
               if valores[i - 1] + tabela[i - 1][w - pesos[i - 1]] > tabela[i - 1][w]:
                   tabela[i][w] = valores[i - 1] + tabela[i - 1][w - pesos[i - 1]]
                   items_selecionados[i][w] = True
               else:
                   tabela[i][w] = tabela[i - 1][w]
           else:
               tabela[i][w] = tabela[i - 1][w]


   resultado = []
   w = capacidade
   for i in range(n, 0, -1):
       if items_selecionados[i][w]:
           resultado.append(i - 1)
           w -= pesos[i - 1]


   return tabela[n][capacidade], resultado




def gerar_caso_teste(n_items, max_peso, max_valor):
   pesos = [random.randint(1, max_peso) for _ in range(n_items)]
   valores = [random.randint(1, max_valor) for _ in range(n_items)]
   capacidade = random.randint(max(pesos), sum(pesos) // 2)
   return pesos, valores, capacidade




def testar_mochila():
   casos_teste = [
       {
           'pesos': [2, 3, 4, 5],
           'valores': [3, 4, 5, 6],
           'capacidade': 8,
           'descricao': 'Caso básico'
       },
       {
           'pesos': [10, 20, 30],
           'valores': [60, 100, 120],
           'capacidade': 50,
           'descricao': 'Valores altos'
       },
       {
           'pesos': [1, 1, 1, 1, 1],
           'valores': [1, 2, 3, 4, 5],
           'capacidade': 3,
           'descricao': 'Pesos iguais'
       }
   ]


   for caso in casos_teste:
       print(f"\nTestando: {caso['descricao']}")
       print(f"Capacidade da mochila: {caso['capacidade']}")
       print(f"Pesos disponíveis: {caso['pesos']}")
       print(f"Valores dos itens: {caso['valores']}")


       inicio = perf_counter()
       valor_maximo, items = mochila_pd(caso['capacidade'], caso['pesos'], caso['valores'])
       tempo = perf_counter() - inicio


       print(f"Valor máximo alcançado: {valor_maximo}")
       print(f"Itens selecionados (índices): {items}")
       print(f"Tempo de execução: {tempo:.6f} segundos")




def analisar_desempenho():
   tamanhos = range(5, 501, 50)
   tempos = []
   valores_maximos = []


   for n in tamanhos:
       pesos, valores, capacidade = gerar_caso_teste(n, 100, 1000)


       inicio = perf_counter()
       valor_maximo, _ = mochila_pd(capacidade, pesos, valores)
       tempo = perf_counter() - inicio


       tempos.append(tempo)
       valores_maximos.append(valor_maximo)


       print(f"\nTamanho {n}:")
       print(f"Tempo: {tempo:.6f} segundos")
       print(f"Valor máximo: {valor_maximo}")


   plt.figure(figsize=(12, 5))


   plt.subplot(1, 2, 1)
   plt.plot(tamanhos, tempos, 'b-', marker='o')
   plt.title('Tempo de Execução vs Tamanho da Entrada')
   plt.xlabel('Número de Itens')
   plt.ylabel('Tempo (segundos)')
   plt.grid(True)


   plt.subplot(1, 2, 2)
   plt.plot(tamanhos, valores_maximos, 'r-', marker='o')
   plt.title('Valor Máximo vs Tamanho da Entrada')
   plt.xlabel('Número de Itens')
   plt.ylabel('Valor Máximo Alcançado')
   plt.grid(True)


   plt.tight_layout()
   return plt




if __name__ == "__main__":
   print("Executando testes com casos predefinidos...")
   testar_mochila()


   print("\nIniciando análise de desempenho...")
   plt = analisar_desempenho()
   plt.show()
