import socket
import time
import matplotlib.pyplot as plt
import numpy as np
import random
import string


def gerar_mensagem_aleatoria(tamanho):
    letras = string.ascii_letters + string.digits
    return ''.join(random.choice(letras) for _ in range(tamanho))


def enviar_mensagens(host, porta, quantidade=20, tamanho_max=100):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.settimeout(5.0)

    tempos_resposta = []
    tamanhos_mensagem = []
    respostas_sucesso = []
    tentativas = []

    for i in range(quantidade):
        tamanho = random.randint(10, tamanho_max)
        mensagem = gerar_mensagem_aleatoria(tamanho)
        tamanhos_mensagem.append(tamanho)

        tentativa = 0
        sucesso = False
        tempo_resposta = 0

        while not sucesso and tentativa < 3:
            try:
                tentativa += 1
                inicio = time.time()
                cliente.sendto(mensagem.encode('utf-8'), (host, porta))

                print(f"Enviando mensagem: '{mensagem}'")

                resposta, endereco = cliente.recvfrom(1024)
                resposta_decodificada = resposta.decode('utf-8')

                fim = time.time()
                tempo_resposta = (fim - inicio) * 1000

                print(f"Resposta recebida: '{resposta_decodificada}' de {endereco}")
                print(f"Tempo de resposta: {tempo_resposta:.2f} ms")

                if resposta_decodificada == "ack":
                    sucesso = True
                    print("Resposta 'ack' recebida com sucesso!")
                else:
                    print(f"Resposta inesperada: '{resposta_decodificada}'")

            except socket.timeout:
                print(f"Tempo esgotado na tentativa {tentativa}.")

        tempos_resposta.append(tempo_resposta if sucesso else 0)
        respostas_sucesso.append(1 if sucesso else 0)
        tentativas.append(tentativa)

        print(f"Mensagem {i + 1}/{quantidade} - {'Sucesso' if sucesso else 'Falha'} após {tentativa} tentativa(s)")
        print("-" * 50)

        time.sleep(0.5)

    cliente.close()

    taxa_sucesso = (sum(respostas_sucesso) / quantidade) * 100
    print(f"\nResumo da execução:")
    print(f"Total de mensagens enviadas: {quantidade}")
    print(f"Total de respostas bem-sucedidas: {sum(respostas_sucesso)}")
    print(f"Taxa de sucesso: {taxa_sucesso:.2f}%")

    if sum(respostas_sucesso) > 0:
        tempos_validos = [t for t, s in zip(tempos_resposta, respostas_sucesso) if s == 1]
        print(f"Tempo médio de resposta: {np.mean(tempos_validos):.2f} ms")
        print(f"Tempo mínimo: {min(tempos_validos):.2f} ms")
        print(f"Tempo máximo: {max(tempos_validos):.2f} ms")

    gerar_graficos(tempos_resposta, tamanhos_mensagem, respostas_sucesso, tentativas)


def gerar_graficos(tempos_resposta, tamanhos_mensagem, respostas_sucesso, tentativas):
    indices = list(range(1, len(tempos_resposta) + 1))

    plt.figure(figsize=(12, 6))
    plt.bar(indices, tempos_resposta)
    plt.title('Tempo de Resposta por Mensagem')
    plt.xlabel('Número da Mensagem')
    plt.ylabel('Tempo de Resposta (ms)')
    plt.grid(True)
    plt.savefig('cliente_tempo_resposta.png')
    plt.close()

    tempos_validos = [t for t, s in zip(tempos_resposta, respostas_sucesso) if s == 1]
    tamanhos_validos = [t for t, s in zip(tamanhos_mensagem, respostas_sucesso) if s == 1]

    if tempos_validos:
        plt.figure(figsize=(12, 6))
        plt.scatter(tamanhos_validos, tempos_validos)
        plt.title('Relação entre Tamanho da Mensagem e Tempo de Resposta')
        plt.xlabel('Tamanho da Mensagem (bytes)')
        plt.ylabel('Tempo de Resposta (ms)')
        plt.grid(True)
        plt.savefig('cliente_tamanho_vs_tempo.png')
        plt.close()

    plt.figure(figsize=(12, 6))
    status = ['Sucesso' if s == 1 else 'Falha' for s in respostas_sucesso]
    status_counts = [status.count('Sucesso'), status.count('Falha')]
    plt.pie(status_counts, labels=['Sucesso', 'Falha'], autopct='%1.1f%%', colors=['green', 'red'])
    plt.title('Taxa de Sucesso das Mensagens')
    plt.savefig('cliente_taxa_sucesso.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.bar(indices, tentativas)
    plt.title('Número de Tentativas por Mensagem')
    plt.xlabel('Número da Mensagem')
    plt.ylabel('Tentativas')
    plt.grid(True)
    plt.savefig('cliente_tentativas.png')
    plt.close()

    if tempos_validos:
        plt.figure(figsize=(12, 6))
        plt.hist(tempos_validos, bins=10)
        plt.title('Distribuição dos Tempos de Resposta (Apenas Sucessos)')
        plt.xlabel('Tempo de Resposta (ms)')
        plt.ylabel('Frequência')
        plt.grid(True)
        plt.savefig('cliente_distribuicao_tempos.png')
        plt.close()


def main():
    host = '127.0.0.1'
    porta = 5000
    print(f"Iniciando cliente UDP para comunicação com {host}:{porta}")
    enviar_mensagens(host, porta)


if __name__ == "__main__":
    main()
