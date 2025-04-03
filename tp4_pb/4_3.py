import socket
import time
import random
import string


def gerar_mensagem_aleatoria(tamanho):
    letras = string.ascii_letters + string.digits
    return ''.join(random.choice(letras) for _ in range(tamanho))


def enviar_mensagens(host, porta, quantidade=50):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.settimeout(2.0)

    sucessos = 0
    falhas = 0

    for i in range(quantidade):
        tamanho = random.randint(10, 100)
        mensagem = gerar_mensagem_aleatoria(tamanho)

        inicio = time.time()
        cliente.sendto(mensagem.encode('utf-8'), (host, porta))

        try:
            resposta, endereco = cliente.recvfrom(1024)
            resposta_decodificada = resposta.decode('utf-8')

            fim = time.time()
            tempo_total = (fim - inicio) * 1000

            print(f"Mensagem {i + 1}: '{mensagem}'")
            print(f"Resposta: '{resposta_decodificada}' de {endereco}")
            print(f"Tempo: {tempo_total:.2f} ms")
            print("-" * 40)

            if resposta_decodificada == "ack":
                sucessos += 1
            else:
                falhas += 1

            time.sleep(random.uniform(0.1, 0.5))

        except socket.timeout:
            print(f"Tempo esgotado para mensagem {i + 1}")
            falhas += 1

    cliente.close()

    print(f"\nResumo:")
    print(f"Total de mensagens: {quantidade}")
    print(f"Respostas bem-sucedidas: {sucessos}")
    print(f"Falhas: {falhas}")
    print(f"Taxa de sucesso: {(sucessos / quantidade) * 100:.2f}%")


def main():
    host = '127.0.0.1'
    porta = 5000
    enviar_mensagens(host, porta)


if __name__ == "__main__":
    main()
