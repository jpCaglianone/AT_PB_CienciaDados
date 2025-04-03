import socket
import time
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import os


def iniciar_servidor(porta=5000, tempo_execucao=60):
    """Inicia um servidor TCP na porta especificada por um determinado tempo"""

    # Cria o socket TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar o endereço/porta
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Liga o socket à porta
    servidor.bind(('0.0.0.0', porta))

    # Define o máximo de conexões em espera
    servidor.listen(5)

    print(f"Servidor TCP iniciado, escutando na porta {porta}")
    print(f"Use 'telnet 127.0.0.1 {porta}' para se conectar")

    # Define o timeout para o servidor
    servidor.settimeout(1.0)

    # Variáveis para medição de desempenho
    tempos_resposta = []
    qtd_conexoes = 0
    tempo_inicio = time.time()
    tempo_fim = tempo_inicio + tempo_execucao

    try:
        while time.time() < tempo_fim:
            try:
                # Aceita conexões
                cliente, endereco = servidor.accept()
                print(f"Conexão estabelecida com {endereco}")

                # Mede tempo de resposta
                tempo_inicio_conexao = time.time()

                # Envia mensagem de boas-vindas
                mensagem = "Bem-vindo ao servidor TCP! Digite algo e pressione Enter para receber eco.\n"
                cliente.send(mensagem.encode('utf-8'))

                # Configura o cliente para não bloquear
                cliente.settimeout(0.5)

                # Processa cliente em thread separada
                with ThreadPoolExecutor(max_workers=10) as executor:
                    executor.submit(lidar_com_cliente, cliente, endereco, tempos_resposta)

                qtd_conexoes += 1

            except socket.timeout:
                # Timeout normal do servidor.accept()
                pass

    except KeyboardInterrupt:
        print("Servidor interrompido pelo usuário")

    finally:
        servidor.close()

        # Analisa e gera gráficos se houver dados
        if tempos_resposta:
            analisar_desempenho(tempos_resposta, qtd_conexoes)

        print(f"Servidor encerrado após {int(time.time() - tempo_inicio)} segundos")
        print(f"Total de conexões atendidas: {qtd_conexoes}")


def lidar_com_cliente(cliente, endereco, tempos_resposta):
    """Lida com um cliente conectado"""

    tempo_inicio_conexao = time.time()

    try:
        while True:
            # Recebe dados do cliente
            dados = cliente.recv(1024)
            if not dados:
                break

            # Envia eco dos dados recebidos
            cliente.send(f"Eco: {dados.decode('utf-8')}".encode('utf-8'))

    except (socket.timeout, ConnectionResetError):
        # Cliente inativo ou conexão encerrada
        pass

    finally:
        # Fecha conexão e registra tempo
        cliente.close()
        tempo_fim_conexao = time.time()
        tempo_total = (tempo_fim_conexao - tempo_inicio_conexao) * 1000  # em ms
        tempos_resposta.append(tempo_total)
        print(f"Conexão com {endereco} encerrada - Tempo de resposta: {tempo_total:.2f}ms")


def simular_cargas(porta=5000, num_clientes=10):
    """Simula múltiplos clientes se conectando ao servidor"""

    tempos_carga = []

    for i in range(1, num_clientes + 1):
        tempo_inicio = time.time()

        conexoes_ativas = []
        for j in range(i):
            try:
                cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cliente.connect(('127.0.0.1', porta))
                cliente.send(f"Cliente {j} testando carga".encode('utf-8'))
                resposta = cliente.recv(1024)
                cliente.close()
                conexoes_ativas.append(1)
            except:
                pass

        tempo_total = time.time() - tempo_inicio
        tempos_carga.append((i, tempo_total))

    return tempos_carga


def analisar_desempenho(tempos_resposta, qtd_conexoes):
    """Analisa o desempenho do servidor e gera gráficos"""

    # Cria diretório para gráficos se não existir
    if not os.path.exists('graficos'):
        os.makedirs('graficos')

    # Converte para array numpy
    tempos = np.array(tempos_resposta)

    # Estatísticas básicas
    media = np.mean(tempos)
    mediana = np.median(tempos)
    maximo = np.max(tempos)
    minimo = np.min(tempos)

    print("\n=== Análise de Desempenho ===")
    print(f"Tempo médio de resposta: {media:.2f}ms")
    print(f"Tempo mediano de resposta: {mediana:.2f}ms")
    print(f"Tempo máximo de resposta: {maximo:.2f}ms")
    print(f"Tempo mínimo de resposta: {minimo:.2f}ms")

    # Gráfico de histograma de tempos de resposta
    plt.figure(figsize=(10, 6))
    plt.hist(tempos, bins=20, alpha=0.7, color='blue')
    plt.title('Distribuição dos Tempos de Resposta')
    plt.xlabel('Tempo de Resposta (ms)')
    plt.ylabel('Frequência')
    plt.grid(True, alpha=0.3)
    plt.savefig('graficos/distribuicao_tempos.png')
    plt.close()

    # Simula diferentes cargas para análise de escalabilidade
    try:
        tempos_carga = simular_cargas()

        if tempos_carga:
            # Descompacta dados
            clientes, tempos = zip(*tempos_carga)

            # Gráfico de escalabilidade
            plt.figure(figsize=(10, 6))
            plt.plot(clientes, tempos, 'o-', color='green')
            plt.title('Análise de Escalabilidade do Servidor')
            plt.xlabel('Número de Clientes Simultâneos')
            plt.ylabel('Tempo de Processamento (s)')
            plt.grid(True, alpha=0.3)
            plt.savefig('graficos/escalabilidade.png')
            plt.close()

            # Complexidade computacional (O(n))
            x = np.array(clientes)
            y = np.array(tempos)

            # Tentativa de ajuste linear (O(n))
            coef = np.polyfit(x, y, 1)
            poly1d_fn = np.poly1d(coef)

            plt.figure(figsize=(10, 6))
            plt.plot(x, y, 'bo', label='Dados Reais')
            plt.plot(x, poly1d_fn(x), '--k', label=f'Ajuste O(n): {coef[0]:.4f}x + {coef[1]:.4f}')
            plt.title('Análise de Complexidade Computacional')
            plt.xlabel('Número de Clientes (n)')
            plt.ylabel('Tempo (s)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.savefig('graficos/complexidade.png')
            plt.close()
    except:
        print("Não foi possível realizar a análise de escalabilidade")

    print(f"Gráficos salvos no diretório 'graficos/'")


if __name__ == "__main__":
    PORTA = 5000
    TEMPO_EXECUCAO = 120  # segundos

    iniciar_servidor(PORTA, TEMPO_EXECUCAO)
