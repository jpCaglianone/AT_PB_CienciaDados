import socket
import ssl
import time
import numpy as np
import matplotlib.pyplot as plt
import sys


def criar_contexto_ssl():
    contexto = ssl.create_default_context()
    contexto.check_hostname = False
    contexto.verify_mode = ssl.CERT_NONE
    return contexto


def conectar_servidor(host, porta, mensagem, tamanho_buffer=1024):
    inicio = time.time()

    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        contexto = criar_contexto_ssl()
        socket_ssl = contexto.wrap_socket(socket_cliente, server_hostname=host)

        socket_ssl.connect((host, porta))
        print("Cliente: conexão estabelecida")

        socket_ssl.send(mensagem.encode('utf-8'))

        dados = socket_ssl.recv(tamanho_buffer)
        resposta = dados.decode('utf-8')
        print(f"Cliente: recebido: {resposta}")

        socket_ssl.close()
        fim = time.time()
        return fim - inicio

    except Exception as e:
        print(f"Erro no cliente: {e}")
        return -1
    finally:
        socket_cliente.close()


def medir_tempos(tamanhos_dados):
    tempos = []
    tamanhos_bem_sucedidos = []

    for tamanho in tamanhos_dados:
        mensagem = "A" * tamanho
        tempo_total = conectar_servidor('localhost', 8443, mensagem, tamanho)
        if tempo_total > 0:
            tempos.append(tempo_total)
            tamanhos_bem_sucedidos.append(tamanho)
            print(f"Tamanho da mensagem: {tamanho}, Tempo: {tempo_total:.6f} segundos")

    return tempos, tamanhos_bem_sucedidos


def plotar_grafico_tempo(tamanhos, tempos):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='green')
    plt.title('Tempo de Execução do Cliente TLS')
    plt.xlabel('Tamanho da Mensagem')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.savefig('tempo_execucao_cliente_tls.png')


def plotar_grafico_complexidade(tamanhos, tempos):
    plt.figure(figsize=(10, 6))

    x = np.array(tamanhos)
    y = np.array(tempos)

    plt.plot(x, y, 'o-', label='Tempo medido')

    modelo_linear = x / x[0] * y[0]
    plt.plot(x, modelo_linear, '--', label='O(n)')

    plt.title('Complexidade do Cliente TLS')
    plt.xlabel('Tamanho da Mensagem')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)
    plt.savefig('complexidade_cliente_tls.png')


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'teste':
        conectar_servidor('localhost', 8443, "Olá, servidor TLS!")
    else:
        tamanhos_mensagem = [1024, 2048, 4096, 8192, 16384]
        tempos, tamanhos_bem_sucedidos = medir_tempos(tamanhos_mensagem)

        if len(tempos) > 1:
            plotar_grafico_tempo(tamanhos_bem_sucedidos, tempos)
            plotar_grafico_complexidade(tamanhos_bem_sucedidos, tempos)
        else:
            print("Não foi possível coletar dados suficientes para gerar gráficos.")


if __name__ == "__main__":
    main()
