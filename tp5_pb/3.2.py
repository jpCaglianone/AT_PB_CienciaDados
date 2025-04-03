import socket
import ssl
import sys


def monkey_patch_socket():
    """
    Realiza o monkey patch do socket para interceptar os dados enviados e recebidos.
    """
    # Salva as funções originais
    original_send = socket.socket.send
    original_recv = socket.socket.recv

    # Define as novas funções com interceptação
    def send_with_logging(self, data, *args, **kwargs):
        print(f"Interceptado (envio): {data}")
        return original_send(self, data, *args, **kwargs)

    def recv_with_logging(self, bufsize, *args, **kwargs):
        data = original_recv(self, bufsize, *args, **kwargs)
        print(f"Interceptado (recebido): {data}")
        return data

    # Aplica o monkey patch
    socket.socket.send = send_with_logging
    socket.socket.recv = recv_with_logging


def criar_contexto_ssl():
    """
    Cria um contexto SSL/TLS para o cliente.
    """
    contexto = ssl.create_default_context()
    contexto.check_hostname = False
    contexto.verify_mode = ssl.CERT_NONE  # Para testes - em produção use CERT_REQUIRED
    return contexto


def cliente_tls(host, porta, mensagem):
    """
    Estabelece uma conexão TLS com um servidor e envia uma mensagem.

    Args:
        host: Endereço do servidor
        porta: Porta do servidor
        mensagem: Mensagem a ser enviada
    """
    # Aplica o monkey patch para interceptar os dados
    monkey_patch_socket()

    # Cria um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Cria contexto SSL
        contexto = criar_contexto_ssl()

        # Envolve o socket com TLS
        sock_seguro = contexto.wrap_socket(sock, server_hostname=host)

        # Conecta ao servidor
        print(f"Conectando a {host}:{porta}...")
        sock_seguro.connect((host, porta))
        print(f"Conexão estabelecida com {sock_seguro.getpeername()}")
        print(f"Usando cifra: {sock_seguro.cipher()}")

        # Envia a mensagem
        sock_seguro.send(mensagem.encode())

        # Recebe a resposta
        resposta = sock_seguro.recv(1024)
        print(f"Resposta do servidor: {resposta.decode()}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        # Fecha a conexão
        sock.close()


def main():
    if len(sys.argv) != 3:
        print("Uso: python cliente_tls.py <host> <porta>")
        return

    host = sys.argv[1]
    porta = int(sys.argv[2])
    mensagem = "Mensagem segura com logging de pacotes"

    cliente_tls(host, porta, mensagem)


if __name__ == "__main__":
    main()


