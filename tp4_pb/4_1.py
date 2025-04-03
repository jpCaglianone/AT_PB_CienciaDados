
import socket
import threading
import time
import matplotlib.pyplot as plt
import numpy as np
import statistics
from concurrent.futures import ThreadPoolExecutor


def iniciar_servidor(porta, max_conexoes, coleta_dados=False):
    tempos_conexao = []
    tempos_resposta = []

    # Criar socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permitir reutilização do endereço
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Vincular o socket ao endereço e porta
    servidor.bind(('localhost', porta))

    # Escutar conexões
    servidor.listen(max_conexoes)
    print(f"Servidor iniciado. Escutando na porta {porta}")

    conexoes_atendidas = 0

    # Tempo de início do servidor
    tempo_inicio_servidor = time.time()

    try:
        while conexoes_atendidas < max_conexoes:
            # Aceitar conexão
            tempo_inicio_conexao = time.time()
            conexao, endereco = servidor.accept()
            tempo_fim_conexao = time.time()

            if coleta_dados:
                tempos_conexao.append(tempo_fim_conexao - tempo_inicio_conexao)

            conexoes_atendidas += 1
            print(f"Conexão {conexoes_atendidas} aceita de {endereco}")

            # Enviar mensagem de boas-vindas
            tempo_inicio_resposta = time.time()
            conexao.sendall(f"Bem-vindo ao servidor TCP! Você é o cliente #{conexoes_atendidas}".encode('utf-8'))
            tempo_fim_resposta = time.time()

            if coleta_dados:
                tempos_resposta.append(tempo_fim_resposta - tempo_inicio_resposta)

            # Fechar conexão
            conexao.close()

    except KeyboardInterrupt:
        print("Servidor interrompido pelo usuário")
    finally:
        servidor.close()

    # Tempo total de execução do servidor
    tempo_total = time.time() - tempo_inicio_servidor

    return tempos_conexao, tempos_resposta, tempo_total


def cliente_tcp(porta, mensagem=None):
    try:
        # Criar socket TCP/IP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectar ao servidor
        cliente.connect(('localhost', porta))

        # Receber mensagem de boas-vindas
        dados = cliente.recv(1024)

        # Fechar socket
        cliente.close()

        return dados.decode('utf-8')

    except Exception as e:
        print(f"Erro no cliente: {e}")
        return None


def executar_teste(n_conexoes, porta):
    print(f"\nIniciando teste com {n_conexoes} conexões na porta {porta}...")

    # Iniciar servidor em uma thread separada
    thread_servidor = threading.Thread(target=iniciar_servidor, args=(porta, n_conexoes, True))
    thread_servidor.daemon = True
    thread_servidor.start()

    # Aguardar servidor iniciar
    time.sleep(1)

    # Armazenar tempos de resposta do cliente
    tempos_cliente = []

    # Criar clientes usando ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=min(50, n_conexoes)) as executor:
        # Iniciar cronômetro
        tempo_inicio = time.time()

        # Submeter tarefas de clientes
        futures = [executor.submit(cliente_tcp, porta) for _ in range(n_conexoes)]

        # Coletar resultados
        for future in futures:
            resultado = future.result()
            if resultado:
                tempo_cliente = time.time() - tempo_inicio
                tempos_cliente.append(tempo_cliente)

    # Aguardar o servidor terminar
    thread_servidor.join(timeout=30)

    # Executar o servidor diretamente para obter os tempos
    tempos_conexao, tempos_resposta, tempo_total = iniciar_servidor(porta + 1000, n_conexoes, True)

    return tempos_conexao, tempos_resposta, tempos_cliente, tempo_total


def gerar_graficos(resultados):
    # Extrair dados dos resultados
    n_conexoes = [res[0] for res in resultados]
    tempos_totais = [res[4] for res in resultados]
    media_tempo_conexao = [statistics.mean(res[1]) if res[1] else 0 for res in resultados]
    media_tempo_resposta = [statistics.mean(res[2]) if res[2] else 0 for res in resultados]
    media_tempo_cliente = [statistics.mean(res[3]) if res[3] else 0 for res in resultados]

    # Gráfico 1: Tempo total vs Número de conexões
    plt.figure(figsize=(10, 6))
    plt.plot(n_conexoes, tempos_totais, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Número de Conexões')
    plt.ylabel('Tempo Total (segundos)')
    plt.title('Tempo Total de Processamento vs Número de Conexões')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('tempo_total_vs_conexoes.png')
    plt.close()

    # Gráfico 2: Comparação dos tempos médios
    plt.figure(figsize=(12, 7))
    width = 0.25
    x = np.arange(len(n_conexoes))

    plt.bar(x - width, media_tempo_conexao, width, label='Tempo Médio de Conexão')
    plt.bar(x, media_tempo_resposta, width, label='Tempo Médio de Resposta')
    plt.bar(x + width, media_tempo_cliente, width, label='Tempo Médio Cliente')

    plt.xlabel('Número de Conexões')
    plt.ylabel('Tempo Médio (segundos)')
    plt.title('Comparação dos Tempos Médios por Número de Conexões')
    plt.xticks(x, n_conexoes)
    plt.legend()
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('comparacao_tempos_medios.png')
    plt.close()

    # Gráfico 3: Eficiência por conexão
    eficiencia = [tempos_totais[i] / n for i, n in enumerate(n_conexoes)]

    plt.figure(figsize=(10, 6))
    plt.plot(n_conexoes, eficiencia, 'ro-', linewidth=2, markersize=8)
    plt.xlabel('Número de Conexões')
    plt.ylabel('Tempo por Conexão (segundos)')
    plt.title('Eficiência do Servidor: Tempo por Conexão')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('eficiencia_por_conexao.png')
    plt.close()

    # Gráfico 4: Distribuição dos tempos para cada cenário
    plt.figure(figsize=(14, 8))

    for i, n in enumerate(n_conexoes):
        plt.subplot(2, 2, i+ 1)

        dados_conexao = resultados[i][1]
        dados_resposta = resultados[i][2]
        dados_cliente = resultados[i][3]

        if dados_conexao and dados_resposta and dados_cliente:
            plt.boxplot([dados_conexao, dados_resposta, dados_cliente],
                        labels=['Tempo de Conexão', 'Tempo de Resposta', 'Tempo Cliente'])
            plt.title(f'Distribuição dos Tempos para {n} Conexões')
            plt.ylabel('Tempo (segundos)')
            plt.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig('distribuicao_tempos.png')
    plt.close()


def executar_experimentos():
    # Configurações de teste
    n_conexoes_lista = [5, 10, 50, 100]
    porta_base = 8000

    resultados = []

    for i, n in enumerate(n_conexoes_lista):
        porta = porta_base + i
        tempos_conexao, tempos_resposta, tempos_cliente, tempo_total = executar_teste(n, porta)
        resultados.append((n, tempos_conexao, tempos_resposta, tempos_cliente, tempo_total))

        print(f"\nResultados para {n} conexões:")
        print(f"Tempo total: {tempo_total:.4f} segundos")
        if tempos_conexao:
            print(f"Tempo médio de conexão: {statistics.mean(tempos_conexao):.6f} segundos")
        if tempos_resposta:
            print(f"Tempo médio de resposta: {statistics.mean(tempos_resposta):.6f} segundos")
        if tempos_cliente:
            print(f"Tempo médio do cliente: {statistics.mean(tempos_cliente):.6f} segundos")

        # Pequena pausa entre testes
        time.sleep(2)

    print("\nGerando gráficos...")
    gerar_graficos(resultados)
    print("Gráficos salvos com sucesso!")

    return resultados


if __name__ == "__main__":
    resultados = executar_experimentos()


    