
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import random


def mochila_gulosa(itens, capacidade):
    for i, item in enumerate(itens):
        item['indice'] = i
        item['razao'] = item['valor'] / item['peso']

    itens_ordenados = sorted(itens, key=lambda x: x['razao'], reverse=True)

    peso_total = 0
    valor_total = 0
    itens_selecionados = []

    for item in itens_ordenados:
        if peso_total + item['peso'] <= capacidade:
            itens_selecionados.append(item)
            peso_total += item['peso']
            valor_total += item['valor']

    return itens_selecionados, valor_total, peso_total


def gerar_itens_aleatorios(n, peso_max=20, valor_max=100):
    itens = []
    for i in range(n):
        peso = random.randint(1, peso_max)
        valor = random.randint(1, valor_max)
        itens.append({
            'nome': f'item{ i +1}',
            'peso': peso,
            'valor': valor
        })
    return itens


def medir_tempo_execucao(tamanhos, capacidade_relativa=0.5):
    tempos = []
    valores = []

    for tamanho in tamanhos:
        capacidade = int(tamanho * capacidade_relativa * 10)
        itens = gerar_itens_aleatorios(tamanho)

        inicio = time.time()
        itens_selecionados, valor_total, peso_total = mochila_gulosa(itens, capacidade)
        fim = time.time()

        tempo_total = fim - inicio
        tempos.append(tempo_total)
        valores.append(valor_total)

        print(f"Número de itens: {tamanho}, Capacidade: {capacidade}, Tempo: {tempo_total:.6f} segundos")
        print(f"Valor total: {valor_total}, Peso total: {peso_total}")
        print(f"Número de itens selecionados: {len(itens_selecionados)}")
        print("-" * 50)

    return tempos, valores


def plotar_grafico_tempo(tamanhos, tempos):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='blue')
    plt.title('Tempo de Execução da Heurística Gulosa para o Problema da Mochila')
    plt.xlabel('Número de Itens')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.savefig('tempo_execucao_mochila_gulosa.png')


def plotar_grafico_complexidade(tamanhos, tempos):
    plt.figure(figsize=(10, 6))

    x = np.array(tamanhos)
    y = np.array(tempos)

    plt.plot(x, y, 'o-', label='Tempo medido')

    modelo_n_log_n = x * np.log(x) / (x[0] * np.log(x[0])) * y[0]
    plt.plot(x, modelo_n_log_n, '--', label='O(n log n)')

    plt.title('Comparação da Complexidade da Heurística Gulosa para o Problema da Mochila')
    plt.xlabel('Número de Itens')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)
    plt.savefig('complexidade_mochila_gulosa.png')


def plotar_grafico_valor(tamanhos, valores):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, valores, marker='o', linestyle='-', color='green')
    plt.title('Valor Total Obtido pela Heurística Gulosa')
    plt.xlabel('Número de Itens')
    plt.ylabel('Valor Total')
    plt.grid(True)
    plt.savefig('valor_mochila_gulosa.png')


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'teste':
        itens_exemplo = [
            {'nome': 'item1', 'peso': 2, 'valor': 40},
            {'nome': 'item2', 'peso': 3, 'valor': 50},
            {'nome': 'item3', 'peso': 5, 'valor': 100},
            {'nome': 'item4', 'peso': 4, 'valor': 90}
        ]
        capacidade = 8

        itens_selecionados, valor_total, peso_total = mochila_gulosa(itens_exemplo, capacidade)

        print("Itens selecionados pela heurística gulosa:")
        for item in itens_selecionados:
            print(f"{item['nome']}: peso {item['peso']}, valor {item['valor']}, razão {item['razao']:.2f}")

        print(f"Valor total: {valor_total}")
        print(f"Peso total: {peso_total}")
        print(f"Capacidade utilizada: {peso_total}/{capacidade}")
    else:
        tamanhos = [100, 500, 1000, 5000, 10000]
        tempos, valores = medir_tempo_execucao(tamanhos)

        plotar_grafico_tempo(tamanhos, tempos)
        plotar_grafico_complexidade(tamanhos, tempos)
        plotar_grafico_valor(tamanhos, valores)


if __name__ == "__main__":
    main()
