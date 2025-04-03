import numpy as np
import matplotlib.pyplot as plt
import time
import subprocess
import re


def fazer_requisicao(url):
    inicio = time.time()
    resultado = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    fim = time.time()
    tempo_total = fim - inicio
    tamanho_resposta = len(resultado.stdout)
    return tempo_total, tamanho_resposta, resultado.stdout


def analisar_complexidade(tempos, tamanhos):
    # Verificação de dados válidos
    if len(tempos) < 2 or len(tamanhos) < 2:
        return None, [0, 0]

    # Verificar por valores não numéricos ou infinitos
    tempos_filtrados = []
    tamanhos_filtrados = []

    for t, s in zip(tempos, tamanhos):
        if (np.isfinite(t) and np.isfinite(s) and
                isinstance(t, (int, float)) and isinstance(s, (int, float))):
            tempos_filtrados.append(t)
            tamanhos_filtrados.append(s)

    # Se não tivermos dados suficientes após a filtragem
    if len(tempos_filtrados) < 2:
        return None, [0, 0]

    try:
        coef = np.polyfit(tamanhos_filtrados, tempos_filtrados, 1)
        polinomio = np.poly1d(coef)
        return polinomio, coef
    except np.linalg.LinAlgError:
        # Fallback para um método mais simples se polyfit falhar
        media_tempos = np.mean(tempos_filtrados)
        media_tamanhos = np.mean(tamanhos_filtrados)
        if np.std(tamanhos_filtrados) != 0:
            inclinacao = (np.std(tempos_filtrados) / np.std(tamanhos_filtrados))
            intercepto = media_tempos - inclinacao * media_tamanhos
        else:
            inclinacao = 0
            intercepto = media_tempos

        coef = [inclinacao, intercepto]
        polinomio = np.poly1d(coef)
        return polinomio, coef


def extrair_cabecalhos(url):
    resultado = subprocess.run(['curl', '-s', '-I', url], capture_output=True, text=True)
    cabecalhos = resultado.stdout.strip().split('\n')
    return cabecalhos


def main():
    url_base = "http://127.0.0.1:8000"
    urls_teste = [
        url_base,
        f"{url_base}/index.html",
        f"{url_base}/?param=teste",
        f"{url_base}/?param=teste&outro=valor"
    ]

    tempos = []
    tamanhos = []
    respostas = []

    print("Iniciando análise de requisições HTTP...")

    for url in urls_teste:
        try:
            print(f"\nTestando URL: {url}")
            tempo, tamanho, resposta = fazer_requisicao(url)
            tempos.append(tempo)
            tamanhos.append(tamanho)
            respostas.append(resposta)
            print(f"Tempo de resposta: {tempo:.4f} segundos")
            print(f"Tamanho da resposta: {tamanho} bytes")
            print(f"Primeiros 100 caracteres da resposta: {resposta[:100]}...")

            cabecalhos = extrair_cabecalhos(url)
            print("Cabeçalhos da resposta:")
            for cabecalho in cabecalhos[:5]:  # Primeiros 5 cabeçalhos
                print(f"  {cabecalho}")
        except Exception as e:
            print(f"Erro ao testar URL {url}: {e}")

    # Verificar se temos dados suficientes para plotar
    if len(tempos) == 0 or len(tamanhos) == 0:
        print("Não foram coletados dados suficientes para análise.")
        return

    plt.figure(figsize=(10, 6))

    # Análise de tempos de resposta
    plt.subplot(2, 2, 1)
    plt.bar(range(len(urls_teste)), tempos)
    plt.xticks(range(len(urls_teste)), [f"URL {i + 1}" for i in range(len(urls_teste))])
    plt.title("Tempo de Resposta por URL")
    plt.ylabel("Tempo (segundos)")

    # Análise de tamanho vs tempo
    plt.subplot(2, 2, 2)
    plt.scatter(tamanhos, tempos)

    # Linha de tendência
    modelo, coeficientes = analisar_complexidade(tempos, tamanhos)
    if modelo is not None:
        try:
            x_min = min(tamanhos)
            x_max = max(tamanhos)
            x_linha = np.linspace(x_min, x_max, 100)
            y_linha = modelo(x_linha)
            plt.plot(x_linha, y_linha, 'r-')
            plt.title(f"Relação Tamanho vs Tempo (y = {coeficientes[0]:.6f}x + {coeficientes[1]:.6f})")
        except Exception as e:
            plt.title("Relação Tamanho vs Tempo")
            print(f"Erro ao plotar linha de tendência: {e}")
    else:
        plt.title("Relação Tamanho vs Tempo (dados insuficientes)")

    plt.xlabel("Tamanho (bytes)")
    plt.ylabel("Tempo (segundos)")

    # Múltiplas requisições para um endpoint
    plt.subplot(2, 2, 3)
    tempos_multiplos = []
    for i in range(10):
        try:
            inicio = time.time()
            subprocess.run(['curl', '-s', url_base], capture_output=True)
            fim = time.time()
            tempos_multiplos.append(fim - inicio)
        except Exception as e:
            print(f"Erro na requisição {i + 1}: {e}")

    if tempos_multiplos:
        plt.plot(range(1, len(tempos_multiplos) + 1), tempos_multiplos, 'o-')
        plt.title("Performance em Requisições Consecutivas")
        plt.xlabel("Número da Requisição")
        plt.ylabel("Tempo (segundos)")
    else:
        plt.text(0.5, 0.5, "Dados insuficientes", ha='center', va='center')
        plt.title("Performance em Requisições Consecutivas")

    # Histograma de tempos
    plt.subplot(2, 2, 4)
    if tempos_multiplos:
        plt.hist(tempos_multiplos, bins=min(5, len(tempos_multiplos)))
        plt.title("Distribuição de Tempos de Resposta")
        plt.xlabel("Tempo (segundos)")
        plt.ylabel("Frequência")
    else:
        plt.text(0.5, 0.5, "Dados insuficientes", ha='center', va='center')
        plt.title("Distribuição de Tempos de Resposta")

    plt.tight_layout()
    try:
        plt.savefig("analise_http.png")
        print("\nGráficos salvos em 'analise_http.png'")
    except Exception as e:
        print(f"Erro ao salvar gráfico: {e}")

    plt.close()

    print("\nAnálise completa.")
    if modelo is not None:
        print(f"Complexidade temporal estimada: O(n) com coeficiente {coeficientes[0]:.6f}")
    else:
        print("Não foi possível estimar a complexidade temporal devido a dados insuficientes.")

    # Análise do conteúdo da resposta
    for i, resposta in enumerate(respostas):
        print(f"\nAnálise da resposta {i + 1}:")
        linhas = resposta.count('\n')
        palavras = len(resposta.split())
        links = len(re.findall(r'href=[\'"]?([^\'" >]+)', resposta))
        print(f"  Número de linhas: {linhas}")
        print(f"  Número de palavras: {palavras}")
        print(f"  Número de links: {links}")


if __name__ == "__main__":
    main()


