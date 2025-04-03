
import socket
import ssl
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


def criar_contexto_ssl():
    contexto = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    contexto.load_cert_chain(certfile="certificado.pem", keyfile="chave.pem")
    return contexto


def iniciar_servidor(porta, tamanho_buffer=1024):
    inicio = time.time()

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor_socket.bind(('localhost', porta))
    servidor_socket.listen(5)

    contexto = criar_contexto_ssl()

    print(f"Servidor TLS iniciado na porta {porta}")

    try:
        conexao, endereco = servidor_socket.accept()
        conexao_ssl = contexto.wrap_socket(conexao, server_side=True)

        print(f"Conexão estabelecida com {endereco}")

        dados = conexao_ssl.recv(tamanho_buffer)
        mensagem = dados.decode('utf-8')
        print(f"Recebido: {mensagem}")

        conexao_ssl.send(dados)

        conexao_ssl.close()
        fim = time.time()
        return fim - inicio

    except Exception as e:
        print(f"Erro no servidor: {e}")
        return -1
    finally:
        servidor_socket.close()


def gerar_certificado():
    if not (os.path.exists("certificado.pem") and os.path.exists("chave.pem")):
        print("Gerando certificado autoassinado...")
        os.system \
            ("openssl req -x509 -newkey rsa:4096 -nodes -out certificado.pem -keyout chave.pem -days 365 -subj '/CN=localhost'")
        print("Certificado gerado com sucesso.")


def medir_tempos(tamanhos_dados):
    tempos = []

    for tamanho in tamanhos_dados:
        tempo_total = iniciar_servidor(8443, tamanho)
        if tempo_total > 0:
            tempos.append(tempo_total)
            print(f"Tamanho do buffer: {tamanho}, Tempo: {tempo_total:.6f} segundos")

    return tempos


def plotar_grafico_tempo(tamanhos, tempos):
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='blue')
    plt.title('Tempo de Execução do Servidor TLS')
    plt.xlabel('Tamanho do Buffer')
    plt.ylabel('Tempo (segundos)')
    plt.grid(True)
    plt.savefig('tempo_execucao_servidor_tls.png')


def plotar_grafico_complexidade(tamanhos, tempos):
    plt.figure(figsize=(10, 6))

    x = np.array(tamanhos)
    y = np.array(tempos)

    plt.plot(x, y, 'o-', label='Tempo medido')

    modelo_linear = x / x[0] * y[0]
    plt.plot(x, modelo_linear, '--', label='O(n)')

    plt.title('Complexidade do Servidor TLS')
    plt.xlabel('Tamanho do Buffer')
    plt.ylabel('Tempo (segundos)')
    plt.legend()
    plt.grid(True)
    plt.savefig('complexidade_servidor_tls.png')


def main():
    gerar_certificado()

    if len(sys.argv) > 1 and sys.argv[1] == 'teste':
        iniciar_servidor(8443)
    else:
        tamanhos_buffer = [1024, 2048, 4096, 8192, 16384]
        print("Modo de benchmark. Execute o cliente com diferentes tamanhos de mensagem.")
        print("Pressione Ctrl+C para encerrar após concluir os testes.")

        tempos = []
        tamanhos_registrados = []

        try:
            while True:
                tamanho_buffer = 1024  # Tamanho padrão para recepção
                tempo = iniciar_servidor(8443, tamanho_buffer)

                if tempo > 0:
                    # Obter o tamanho da última mensagem recebida
                    tamanho_atual = tamanho_buffer  # Simplificado para este exemplo
                    tempos.append(tempo)
                    tamanhos_registrados.append(tamanho_atual)

                    if len(tempos) >= 5:  # Após coletar pelo menos 5 amostras
                        plotar_grafico_tempo(tamanhos_registrados, tempos)
                        plotar_grafico_complexidade(tamanhos_registrados, tempos)

        except KeyboardInterrupt:
            print("\nTestes concluídos.")
            if len(tempos) > 1:
                plotar_grafico_tempo(tamanhos_registrados, tempos)
                plotar_grafico_complexidade(tamanhos_registrados, tempos)
            else:
                print("Dados insuficientes para gerar gráficos.")


if __name__ == "__main__":
    main()
