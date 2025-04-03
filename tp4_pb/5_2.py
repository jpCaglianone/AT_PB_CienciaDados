import socket
import time
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def conectar_ao_servidor(host='127.0.0.1', porta=5000, mensagem='Olá, servidor!', mostrar_resposta=True):
    """Conecta ao servidor TCP, envia uma mensagem e retorna a resposta e o tempo de resposta"""

    tempo_inicio = time.time()

    try:
        # Cria o socket TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define um timeout para não bloquear indefinidamente
        cliente.settimeout(5.0)

        # Conecta ao servidor
        cliente.connect((host, porta))

        # Recebe a mensagem de boas-vindas
        resposta_boas_vindas = cliente.recv(1024).decode('utf-8')
        if mostrar_resposta:
            print(f"Mensagem do servidor: {resposta_boas_vindas}")

        # Envia a mensagem
        cliente.send(mensagem.encode('utf-8'))

        # Recebe a resposta
        resposta = cliente.recv(1024).decode('utf-8')
        if mostrar_resposta:
            print(f"Resposta do servidor: {resposta}")

        # Fecha a conexão
        cliente.close()

        # Calcula o tempo total
        tempo_total = (time.time() - tempo_inicio) * 1000  # em ms

        return resposta, tempo_total

    except socket.error as erro:
        print(f"Erro na conexão: {erro}")
        return None, (time.time() - tempo_inicio) * 1000


def testar_multiplas_conexoes(host='127.0.0.1', porta=5000, num_conexoes=100):
    """Testa múltiplas conexões ao servidor e mede o tempo de resposta"""

    tempos_resposta = []
    conexoes_bem_sucedidas = 0

    print(f"Iniciando teste com {num_conexoes} conexões...")

    tempo_inicio_total = time.time()

    for i in range(num_conexoes):
        mensagem = f"Mensagem de teste #{i + 1}"
        resposta, tempo = conectar_ao_servidor(host, porta, mensagem, mostrar_resposta=False)

        if resposta:
            tempos_resposta.append(tempo)
            conexoes_bem_sucedidas += 1

        # Breve pausa para não sobrecarregar o servidor
        time.sleep(0.01)

    tempo_total = time.time() - tempo_inicio_total

    print(f"\nTeste concluído em {tempo_total:.2f} segundos")
    print(f"Conexões bem-sucedidas: {conexoes_bem_sucedidas}/{num_conexoes}")

    if tempos_resposta:
        analisar_desempenho(tempos_resposta, tempo_total, num_conexoes)
    else:
        print("Não foi possível estabelecer conexões suficientes para análise.")


def testar_concorrencia(host='127.0.0.1', porta=5000, num_clientes=10):
    """Testa conexões concorrentes ao servidor"""

    resultados = []
    tempo_inicio = time.time()

    print(f"Iniciando teste de concorrência com {num_clientes} clientes simultâneos...")

    def tarefa_cliente(cliente_id):
        mensagem = f"Cliente concorrente #{cliente_id}"
        resposta, tempo = conectar_ao_servidor(host, porta, mensagem, mostrar_resposta=False)
        return cliente_id, resposta, tempo

    with ThreadPoolExecutor(max_workers=num_clientes) as executor:
        futures = [executor.submit(tarefa_cliente, i) for i in range(num_clientes)]

        for future in futures:
            try:
                cliente_id, resposta, tempo = future.result()
                resultados.append((cliente_id, tempo))
                print(f"Cliente {cliente_id}: Tempo de resposta = {tempo:.2f}ms")
            except Exception as e:
                print(f"Erro em cliente: {e}")

    tempo_total = time.time() - tempo_inicio

    print(f"\nTeste de concorrência concluído em {tempo_total:.2f} segundos")

    if resultados:
        # Extrai tempos de resposta
        tempos = [tempo for _, tempo in resultados]

        # Cria e salva gráfico
        analisar_concorrencia(tempos, num_clientes)
    else:
        print("Não foi possível obter resultados para análise de concorrência.")


def analisar_desempenho(tempos_resposta, tempo_total, num_conexoes):
    """Analisa o desempenho das conexões e gera gráficos"""

    # Cria diretório para gráficos se não existir
    if not os.path.exists('graficos_cliente'):
        os.makedirs('graficos_cliente')

    # Converte para array numpy
    tempos = np.array(tempos_resposta)

    # Estatísticas básicas
    media = np.mean(tempos)
    mediana = np.median(tempos)
    maximo = np.max(tempos)
    minimo = np.min(tempos)
    throughput = num_conexoes / tempo_total

    print("\n=== Análise de Desempenho do Cliente ===")
    print(f"Tempo médio de resposta: {media:.2f}ms")
    print(f"Tempo mediano de resposta: {mediana:.2f}ms")
    print(f"Tempo máximo de resposta: {maximo:.2f}ms")
    print(f"Tempo mínimo de resposta: {minimo:.2f}ms")
    print(f"Throughput: {throughput:.2f} conexões/segundo")

    # Gráfico de histograma de tempos de resposta
    plt.figure(figsize=(10, 6))
    plt.hist(tempos, bins=20, alpha=0.7, color='green')
    plt.title('Distribuição dos Tempos de Resposta do Cliente')
    plt.xlabel('Tempo de Resposta (ms)')
    plt.ylabel('Frequência')
    plt.grid(True, alpha=0.3)
    plt.savefig('graficos_cliente/distribuicao_tempos_cliente.png')
    plt.close()

    # Gráfico de linha mostrando evolução dos tempos
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(tempos) + 1), tempos, 'b-', alpha=0.7)
    plt.axhline(y=media, color='r', linestyle='--', label=f'Média: {media:.2f}ms')
    plt.title('Evolução dos Tempos de Resposta')
    plt.xlabel('Número da Conexão')
    plt.ylabel('Tempo de Resposta (ms)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('graficos_cliente/evolucao_tempos.png')
    plt.close()

    print(f"Gráficos salvos no diretório 'graficos_cliente/'")


def analisar_concorrencia(tempos, num_clientes):
    """Analisa os tempos de resposta para conexões concorrentes"""

    # Cria diretório para gráficos se não existir
    if not os.path.exists('graficos_cliente'):
        os.makedirs('graficos_cliente')

    # Converte para array numpy
    tempos = np.array(tempos)

    # Estatísticas
    media = np.mean(tempos)
    mediana = np.median(tempos)

    # Gráfico de barras para clientes concorrentes
    indices = np.arange(len(tempos))

    plt.figure(figsize=(12, 6))
    plt.bar(indices, tempos, color='purple', alpha=0.7)
    plt.axhline(y=media, color='r', linestyle='--', label=f'Média: {media:.2f}ms')
    plt.title(f'Tempos de Resposta para {num_clientes} Clientes Concorrentes')
    plt.xlabel('ID do Cliente')
    plt.ylabel('Tempo de Resposta (ms)')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.savefig('graficos_cliente/concorrencia.png')
    plt.close()

    print(f"Análise de concorrência salva no diretório 'graficos_cliente/'")


def menu_principal():
    """Exibe menu de opções para o usuário"""

    host = '127.0.0.1'
    porta = 5000

    while True:
        print("\n===== CLIENTE TCP =====")
        print(f"Servidor configurado: {host}:{porta}")
        print("1. Conectar e enviar uma mensagem simples")
        print("2. Testar várias conexões sequenciais")
        print("3. Testar conexões concorrentes")
        print("4. Alterar configurações de conexão")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            mensagem = input("Digite a mensagem a ser enviada: ")
            print("\nConectando ao servidor...")
            conectar_ao_servidor(host, porta, mensagem)

        elif opcao == '2':
            try:
                num = int(input("Número de conexões para testar: "))
                testar_multiplas_conexoes(host, porta, num)
            except ValueError:
                print("Por favor, digite um número válido.")

        elif opcao == '3':
            try:
                num = int(input("Número de clientes concorrentes: "))
                testar_concorrencia(host, porta, num)
            except ValueError:
                print("Por favor, digite um número válido.")

        elif opcao == '4':
            try:
                novo_host = input(f"Novo endereço do servidor [{host}]: ")
                if novo_host:
                    host = novo_host

                nova_porta = input(f"Nova porta [{porta}]: ")
                if nova_porta:
                    porta = int(nova_porta)

                print(f"Configurações atualizadas: {host}:{porta}")
            except ValueError:
                print("Porta inválida. Configurações não alteradas.")

        elif opcao == '0':
            print("Encerrando cliente...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    # Se desejar executar em modo simples, descomente a linha abaixo:
    # conectar_ao_servidor()

    # Interface com menu
    menu_principal()
