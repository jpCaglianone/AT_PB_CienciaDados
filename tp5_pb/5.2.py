#!/usr/bin/env python3
import subprocess
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def executar_nmap(host, faixa_portas=None):
    inicio = time.time()

    if faixa_portas:
        comando = ["nmap", "-sV", "-p", faixa_portas, host]
    else:
        comando = ["nmap", "-sV", host]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        saida = resultado.stdout
    except subprocess.CalledProcessError as e:
        saida = f"Erro ao executar o Nmap: {e}"
    except FileNotFoundError:
        saida = "Erro: Nmap não está instalado ou não foi encontrado no sistema."

    fim = time.time()
    tempo_execucao = fim - inicio

    return saida, tempo_execucao


def salvar_resultados(host, saida, tempo, faixa_portas=None):
    nome_arquivo = f"resultado_nmap_{host.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(nome_arquivo, "w") as arquivo:
        arquivo.write(f"Host: {host}\n")
        if faixa_portas:
            arquivo.write(f"Faixa de portas: {faixa_portas}\n")
        arquivo.write(f"Tempo de execução: {tempo:.2f} segundos\n\n")
        arquivo.write(saida)

    return nome_arquivo


def gerar_graficos(tempos, quantidades):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(quantidades, tempos, 'o-', color='blue')
    plt.title('Tempo de Execução por Quantidade de Portas')
    plt.xlabel('Quantidade de Portas')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    # Complexidade O(n) para varredura de portas
    n = np.array(quantidades)
    complexidade = n * np.log(n)  # Complexidade aproximada para varredura de portas

    plt.plot(quantidades, tempos, 'o-', label='Tempo Real', color='blue')
    plt.plot(quantidades, complexidade / np.max(complexidade) * np.max(tempos), '--',
             label='Complexidade Teórica O(n log n)', color='red')
    plt.title('Complexidade do Algoritmo')
    plt.xlabel('Quantidade de Portas')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"analise_nmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")


def main():
    if len(sys.argv) < 2:
        print("Uso: python group5_exercicio2.py <host> [faixas_de_portas separadas por espaço]")
        sys.exit(1)

    host = sys.argv[1]

    # Executar com diferentes quantidades de portas para análise de desempenho
    faixas_teste = ["1-100", "1-500", "1-1000", "1-2000", "1-5000"]
    tempos = []
    quantidades = [100, 500, 1000, 2000, 5000]

    # Se foram fornecidas faixas de portas específicas na linha de comando, use-as
    if len(sys.argv) > 2:
        faixas_teste = sys.argv[2:]
        quantidades = [int(faixa.split('-')[1]) - int(faixa.split('-')[0]) + 1
                       if '-' in faixa else 1 for faixa in faixas_teste]

    print(f"Iniciando varredura para o host {host} com diferentes faixas de portas:")

    for i, faixa in enumerate(faixas_teste):
        print(f"\nExecutando Nmap para faixa de portas: {faixa}")
        saida, tempo = executar_nmap(host, faixa)
        tempos.append(tempo)

        nome_arquivo = salvar_resultados(host, saida, tempo, faixa)
        print(f"Resultados salvos em: {nome_arquivo}")
        print(f"Tempo de execução: {tempo:.2f} segundos")

    # Gerar gráficos
    gerar_graficos(tempos, quantidades)
    print(f"\nGráficos de análise de desempenho gerados.")


if __name__ == "__main__":
    main()


