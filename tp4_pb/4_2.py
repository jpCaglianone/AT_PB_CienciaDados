import numpy as np
import matplotlib.pyplot as plt
import time
import random


def ordenacao_bolha(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def ordenacao_selecao(lista):
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if lista[j] < lista[min_idx]:
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
    return lista


def ordenacao_insercao(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and chave < lista[j]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista


def ordenacao_quicksort(lista):
    if len(lista) <= 1:
        return lista
    pivo = lista[len(lista) // 2]
    esquerda = [x for x in lista if x < pivo]
    meio = [x for x in lista if x == pivo]
    direita = [x for x in lista if x > pivo]
    return ordenacao_quicksort(esquerda) + meio + ordenacao_quicksort(direita)


def ordenacao_mergesort(lista):
    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2
    esquerda = lista[:meio]
    direita = lista[meio:]

    esquerda = ordenacao_mergesort(esquerda)
    direita = ordenacao_mergesort(direita)

    return mesclar(esquerda, direita)


def mesclar(esquerda, direita):
    resultado = []
    i = j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i] < direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


def medir_tempo_execucao(algoritmo, tamanhos_listas):
    tempos = []
    for tamanho in tamanhos_listas:
        lista = [random.randint(1, 1000) for _ in range(tamanho)]
        inicio = time.time()
        if algoritmo.__name__ in ['ordenacao_quicksort', 'ordenacao_mergesort']:
            resultado = algoritmo(lista)
        else:
            lista_copia = lista.copy()
            resultado = algoritmo(lista_copia)
        fim = time.time()
        tempos.append(fim - inicio)
    return tempos


def main():
    tamanhos_entrada = [100, 500, 1000, 2000, 3000, 4000, 5000]
    algoritmos = [
        ordenacao_bolha,
        ordenacao_selecao,
        ordenacao_insercao,
        ordenacao_quicksort,
        ordenacao_mergesort
    ]

    todos_tempos = {}
    for algoritmo in algoritmos:
        print(f"Executando {algoritmo.__name__}...")
        tempos = medir_tempo_execucao(algoritmo, tamanhos_entrada)
        todos_tempos[algoritmo.__name__] = tempos

    # Gráfico de comparação de tempo
    plt.figure(figsize=(12, 8))
    for algoritmo, tempos in todos_tempos.items():
        nome_algoritmo = algoritmo.replace('ordenacao_', '')
        plt.plot(tamanhos_entrada, tempos, marker='o', label=nome_algoritmo)

    plt.title('Comparação de Tempo de Execução entre Algoritmos de Ordenação')
    plt.xlabel('Tamanho da Entrada')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.legend()
    plt.grid(True)
    plt.savefig('comparacao_tempos.png')

    # Gráfico com escala logarítmica para visualizar melhor as diferenças
    plt.figure(figsize=(12, 8))
    for algoritmo, tempos in todos_tempos.items():
        nome_algoritmo = algoritmo.replace('ordenacao_', '')
        plt.plot(tamanhos_entrada, tempos, marker='o', label=nome_algoritmo)

    plt.title('Comparação de Tempo de Execução (Escala Logarítmica)')
    plt.xlabel('Tamanho da Entrada')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.savefig('comparacao_tempos_log.png')

    # Comparação teórica de complexidade
    complexidades = {
        'bolha': [n ** 2 for n in tamanhos_entrada],
        'selecao': [n ** 2 for n in tamanhos_entrada],
        'insercao': [n ** 2 for n in tamanhos_entrada],
        'quicksort': [n * np.log(n) for n in tamanhos_entrada],
        'mergesort': [n * np.log(n) for n in tamanhos_entrada]
    }

    # Normalizar as complexidades teóricas para comparação
    fator = 0.00001
    plt.figure(figsize=(12, 8))
    for nome, valores in complexidades.items():
        valores_normalizados = [valor * fator for valor in valores]
        plt.plot(tamanhos_entrada, valores_normalizados, '--', label=f'{nome} (teórico)')

    plt.title('Complexidade Teórica dos Algoritmos')
    plt.xlabel('Tamanho da Entrada')
    plt.ylabel('Tempo Teórico (normalizado)')
    plt.legend()
    plt.grid(True)
    plt.savefig('complexidade_teorica.png')

    print('Análise concluída. Gráficos salvos na pasta atual.')


if __name__ == "__main__":
    main()
