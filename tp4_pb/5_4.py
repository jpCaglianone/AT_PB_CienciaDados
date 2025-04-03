import numpy as np
import matplotlib.pyplot as plt
import time
import subprocess
import re
from collections import defaultdict


def fazer_requisicao_get(url):
    inicio = time.time()
    resultado = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    fim = time.time()
    tempo_total = fim - inicio
    tamanho_resposta = len(resultado.stdout)
    return tempo_total, tamanho_resposta, resultado.stdout


def fazer_requisicao_post(url, dados):
    inicio = time.time()
    resultado = subprocess.run(['curl', '-s', '-X', 'POST', '-d', dados, url], capture_output=True, text=True)
    fim = time.time()
    tempo_total = fim - inicio
    tamanho_resposta = len(resultado.stdout)
    return tempo_total, tamanho_resposta, resultado.stdout


def extrair_cabecalhos(url, metodo="GET", dados=None):
    if metodo == "GET":
        resultado = subprocess.run(['curl', '-s', '-I', url], capture_output=True, text=True)
    else:
        resultado = subprocess.run(['curl', '-s', '-I', '-X', 'POST', '-d', dados, url], capture_output=True, text=True)

    cabecalhos = resultado.stdout.strip().split('\n')
    return cabecalhos


def analisar_cabecalhos(cabecalhos):
    info_cabecalhos = {}

    for cab in cabecalhos:
        if ': ' in cab:
            chave, valor = cab.split(': ', 1)
            info_cabecalhos[chave] = valor
        elif ' ' in cab and not ':' in cab:
            partes = cab.split(' ', 2)
            if len(partes) >= 2:
                info_cabecalhos['Status'] = partes[1]

    return info_cabecalhos


def analisar_complexidade(valores_x, valores_y):
    if len(valores_x) < 2 or len(valores_y) < 2:
        return None, [0, 0]

    valores_x_filtrados = []
    valores_y_filtrados = []

    for x, y in zip(valores_x, valores_y):
        if (np.isfinite(x) and np.isfinite(y) and isinstance(x, (int, float)) and isinstance(y, (int, float))):
            valores_x_filtrados.append(x)
            valores_y_filtrados.append(y)

    if len(valores_x_filtrados) < 2:
        return None, [0, 0]

    try:
        coef = np.polyfit(valores_x_filtrados, valores_y_filtrados, 1)
        polinomio = np.poly1d(coef)
        return polinomio, coef
    except np.linalg.LinAlgError:
        media_y = np.mean(valores_y_filtrados)
        media_x = np.mean(valores_x_filtrados)
        if np.std(valores_x_filtrados) != 0:
            inclinacao = (np.std(valores_y_filtrados) / np.std(valores_x_filtrados))
            intercepto = media_y - inclinacao * media_x
        else:
            inclinacao = 0
            intercepto = media_y

        coef = [inclinacao, intercepto]
        polinomio = np.poly1d(coef)
        return polinomio, coef


def main():
    url_base = "http://127.0.0.1:8000"
    dados_post = "nome=Joao"

    print("\nComparando requisições GET e POST via cURL")
    print("\n1. Realizando requisição GET simples...")
    tempo_get, tamanho_get, resposta_get = fazer_requisicao_get(url_base)
    cabecalhos_get = extrair_cabecalhos(url_base)
    info_cabecalhos_get = analisar_cabecalhos(cabecalhos_get)

    print("\n2. Realizando requisição POST...")
    tempo_post, tamanho_post, resposta_post = fazer_requisicao_post(url_base, dados_post)
    cabecalhos_post = extrair_cabecalhos(url_base, "POST", dados_post)
    info_cabecalhos_post = analisar_cabecalhos(cabecalhos_post)

    print("\nRESUMO DE COMPARAÇÃO GET vs. POST:")
    print(f"Tempo GET: {tempo_get:.4f}s | Tempo POST: {tempo_post:.4f}s")
    print(f"Tamanho resposta GET: {tamanho_get} bytes | Tamanho resposta POST: {tamanho_post} bytes")

    print("\nCABEÇALHOS GET:")
    for chave, valor in info_cabecalhos_get.items():
        print(f"  {chave}: {valor}")

    print("\nCABEÇALHOS POST:")
    for chave, valor in info_cabecalhos_post.items():
        print(f"  {chave}: {valor}")

    print("\nREALIZANDO MÚLTIPLAS REQUISIÇÕES PARA ANÁLISE...")

    repeticoes = 10
    tempos_get = []
    tempos_post = []

    for i in range(repeticoes):
        t_get, _, _ = fazer_requisicao_get(url_base)
        tempos_get.append(t_get)

        t_post, _, _ = fazer_requisicao_post(url_base, dados_post)
        tempos_post.append(t_post)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.bar([0, 1], [np.mean(tempos_get), np.mean(tempos_post)], yerr=[np.std(tempos_get), np.std(tempos_post)])
    plt.xticks([0, 1], ['GET', 'POST'])
    plt.title('Tempo Médio de Resposta')
    plt.ylabel('Tempo (segundos)')

    plt.subplot(2, 2, 2)
    plt.boxplot([tempos_get, tempos_post], labels=['GET', 'POST'])
    plt.title('Distribuição de Tempos de Resposta')
    plt.ylabel('Tempo (segundos)')

    plt.subplot(2, 2, 3)
    plt.plot(range(1, repeticoes + 1), tempos_get, 'b-o', label='GET')
    plt.plot(range(1, repeticoes + 1), tempos_post, 'r-o', label='POST')
    plt.xlabel('Número da Requisição')
    plt.ylabel('Tempo (segundos)')
    plt.title('Comparativo de Tempos por Requisição')
    plt.legend()

    if not resposta_get or not resposta_post:
        plt.subplot(2, 2, 4)
        plt.text(0.5, 0.5, 'Sem dados suficientes para análise de conteúdo',
                 horizontalalignment='center', verticalalignment='center')
    else:
        bytes_get = [ord(c) for c in resposta_get[:100] if ord(c) < 256]
        bytes_post = [ord(c) for c in resposta_post[:100] if ord(c) < 256]

        plt.subplot(2, 2, 4)
        if len(bytes_get) > 0 and len(bytes_post) > 0:
            plt.hist([bytes_get, bytes_post], bins=20, label=['GET', 'POST'], alpha=0.7)
            plt.title('Distribuição de Valores ASCII das Respostas')
            plt.xlabel('Valor ASCII')
            plt.ylabel('Frequência')
            plt.legend()
        else:
            plt.text(0.5, 0.5, 'Dados de resposta não adequados para histograma',
                     horizontalalignment='center', verticalalignment='center')

    plt.tight_layout()
    plt.savefig('comparacao_get_post.png')

    print("\nGráficos de análise salvos em 'comparacao_get_post.png'")

    palavras_get = len(resposta_get.split())
    palavras_post = len(resposta_post.split())
    linhas_get = resposta_get.count('\n')
    linhas_post = resposta_post.count('\n')

    print("\nANÁLISE DE CONTEÚDO:")
    print(f"GET: {palavras_get} palavras, {linhas_get} linhas")
    print(f"POST: {palavras_post} palavras, {linhas_post} linhas")

    print("\nDIFERENÇAS ENTRE GET E POST:")
    print("1. No HTTP, GET é usado para solicitar dados e POST para enviar dados ao servidor")
    print(
        "2. Os dados GET são anexados à URL (como query strings), enquanto os dados POST são enviados no corpo da requisição")
    print(
        "3. GET tem limitações de tamanho devido às restrições de comprimento de URL, enquanto POST pode enviar volumes maiores de dados")
    print("4. GET é visível na URL e fica no histórico do navegador, enquanto POST é invisível na URL")
    print(
        "5. GET é idempotente (pode ser repetido sem efeitos colaterais), enquanto POST normalmente altera o estado do servidor")
    print(f"6. Nos nossos testes, GET levou em média {np.mean(tempos_get):.4f}s e POST {np.mean(tempos_post):.4f}s")

    if np.mean(tempos_post) > np.mean(tempos_get):
        diferenca_percentual = ((np.mean(tempos_post) - np.mean(tempos_get)) / np.mean(tempos_get)) * 100
        print(f"   POST foi {diferenca_percentual:.2f}% mais lento que GET")
    else:
        diferenca_percentual = ((np.mean(tempos_get) - np.mean(tempos_post)) / np.mean(tempos_post)) * 100
        print(f"   GET foi {diferenca_percentual:.2f}% mais lento que POST")


if __name__ == "__main__":
    main()
