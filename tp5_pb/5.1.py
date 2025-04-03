#!/usr/bin/env python3


import dns.resolver
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
from concurrent.futures import ThreadPoolExecutor


def coletar_registros_dns(dominio):
    resultados = {}

    tipos_registros = ['A', 'MX', 'NS']

    for tipo in tipos_registros:
        try:
            resposta = dns.resolver.resolve(dominio, tipo)
            if tipo == 'A':
                resultados[tipo] = [str(dado.address) for dado in resposta]
            elif tipo == 'MX':
                resultados[tipo] = [f"{dado.preference} {dado.exchange}" for dado in resposta]
            elif tipo == 'NS':
                resultados[tipo] = [str(dado.target) for dado in resposta]
        except Exception as e:
            resultados[tipo] = [f"Erro: {str(e)}"]

    return resultados


def exibir_resultados(dominio, resultados):
    print(f"\nResultados para o domínio: {dominio}")
    for tipo, dados in resultados.items():
        print(f"Registros {tipo}:")
        for dado in dados:
            print(f"  {dado}")


def processar_lista_dominios(lista_dominios):
    resultados_dominios = {}

    for dominio in lista_dominios:
        resultados = coletar_registros_dns(dominio)
        resultados_dominios[dominio] = resultados
        exibir_resultados(dominio, resultados)

    return resultados_dominios


def processar_lista_dominios_paralelo(lista_dominios):
    resultados_dominios = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futuros = {executor.submit(coletar_registros_dns, dominio): dominio for dominio in lista_dominios}
        for futuro in futuros:
            dominio = futuros[futuro]
            try:
                resultados = futuro.result()
                resultados_dominios[dominio] = resultados
                exibir_resultados(dominio, resultados)
            except Exception as e:
                print(f"Erro ao processar {dominio}: {e}")

    return resultados_dominios


def gerar_graficos(tempos, tamanhos):
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(tamanhos, tempos, 'bo-', linewidth=2, markersize=8)
    plt.title('Tempo de Execução vs. Quantidade de Domínios')
    plt.xlabel('Quantidade de Domínios')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    coefs = np.polyfit(tamanhos, tempos, 1)
    linha_ajuste = np.polyval(coefs, tamanhos)
    plt.plot(tamanhos, tempos, 'bo', markersize=8, label='Dados Medidos')
    plt.plot(tamanhos, linha_ajuste, 'r-', linewidth=2, label=f'Ajuste Linear: {coefs[0]:.4f}x + {coefs[1]:.4f}')
    plt.title('Análise de Complexidade')
    plt.xlabel('Quantidade de Domínios')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('analise_tempo_dns.png')

    plt.figure(figsize=(10, 6))
    plt.loglog(tamanhos, tempos, 'bo-', linewidth=2, markersize=8)
    plt.title('Análise de Complexidade (Escala Log-Log)')
    plt.xlabel('Quantidade de Domínios (log)')
    plt.ylabel('Tempo (segundos) (log)')
    plt.grid(True)
    plt.savefig('analise_tempo_dns_loglog.png')


def main():
    dominios_teste = [
        "google.com",
        "facebook.com",
        "amazon.com",
        "microsoft.com",
        "apple.com",
        "twitter.com",
        "instagram.com",
        "linkedin.com",
        "netflix.com",
        "github.com",
        "wikipedia.org",
        "yahoo.com",
        "reddit.com",
        "wordpress.com",
        "adobe.com",
        "twitch.tv",
        "ebay.com",
        "cnn.com",
        "bbc.co.uk",
        "nytimes.com"
    ]

    tamanhos_teste = [1, 5, 10, 15, 20]
    tempos_execucao = []

    print("Iniciando testes de desempenho para coleta de registros DNS")

    for tamanho in tamanhos_teste:
        print(f"\n\nTestando com {tamanho} domínios:")
        lista_atual = dominios_teste[:tamanho]

        inicio = time.time()
        processar_lista_dominios(lista_atual)
        fim = time.time()

        tempo_total = fim - inicio
        tempos_execucao.append(tempo_total)

        print(f"Tempo de execução para {tamanho} domínios: {tempo_total:.4f} segundos")

    print("\nGerando gráficos de análise de desempenho...")
    gerar_graficos(tempos_execucao, tamanhos_teste)
    print("Gráficos salvos como 'analise_tempo_dns.png' e 'analise_tempo_dns_loglog.png'")

    if len(sys.argv) > 1:
        dominio_usuario = sys.argv[1]
        print(f"\nConsultando domínio fornecido pelo usuário: {dominio_usuario}")
        resultados = coletar_registros_dns(dominio_usuario)
        exibir_resultados(dominio_usuario, resultados)
    else:
        print("\nDica: Você pode fornecer um domínio específico como argumento, ex: ./dns_recon.py example.com")


if __name__ == "__main__":
    main()
