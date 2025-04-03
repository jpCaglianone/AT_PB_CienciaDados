
import socket
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class ServidorTCP:
    def __init__(self, host="127.0.0.1", porta=5000):
        self.host = host
        self.porta = porta
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientes = []
        self.estatisticas = {
            "conexoes": 0,
            "bytes_recebidos": 0,
            "get_requests": 0,
            "post_requests": 0,
            "tempo_processamento": []
        }
        self.rodando = False

    def iniciar(self):
        self.servidor.bind((self.host, self.porta))
        self.servidor.listen(5)
        self.rodando = True
        print(f"Servidor TCP iniciado em {self.host}:{self.porta}")

        thread_aceitar = threading.Thread(target=self.aceitar_conexoes)
        thread_aceitar.daemon = True
        thread_aceitar.start()

        try:
            while self.rodando:
                comando = input("Digite 'stats' para ver estatísticas ou 'sair' para encerrar: ")
                if comando.lower() == "stats":
                    self.mostrar_estatisticas()
                elif comando.lower() == "sair":
                    self.parar()
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.parar()

    def aceitar_conexoes(self):
        while self.rodando:
            try:
                cliente, endereco = self.servidor.accept()
                self.estatisticas["conexoes"] += 1
                print(f"Nova conexão de {endereco[0]}:{endereco[1]}")

                thread_cliente = threading.Thread(target=self.lidar_com_cliente, args=(cliente, endereco))
                thread_cliente.daemon = True
                thread_cliente.start()

                self.clientes.append(cliente)
            except:
                if self.rodando:
                    print("Erro ao aceitar conexão")
                break

    def lidar_com_cliente(self, cliente, endereco):
        inicio_processamento = time.time()
        try:
            dados = cliente.recv(1024).decode('utf-8')
            self.estatisticas["bytes_recebidos"] += len(dados)

            if dados:
                print(f"Recebido de {endereco[0]}:{endereco[1]}: {dados[:50]}...")

                linhas = dados.split('\n')
                primeira_linha = linhas[0] if linhas else ""

                resposta = ""

                if primeira_linha.startswith("GET"):
                    self.estatisticas["get_requests"] += 1
                    resposta = self.processar_get(dados)
                elif primeira_linha.startswith("POST"):
                    self.estatisticas["post_requests"] += 1
                    resposta = self.processar_post(dados)
                else:
                    resposta = self.gerar_resposta_padrao("Método não suportado", "400 Bad Request")

                cliente.send(resposta.encode('utf-8'))
        except Exception as e:
            print(f"Erro ao processar solicitação: {e}")
        finally:
            fim_processamento = time.time()
            self.estatisticas["tempo_processamento"].append(fim_processamento - inicio_processamento)

            if cliente in self.clientes:
                self.clientes.remove(cliente)
            cliente.close()

    def processar_get(self, dados):
        return self.gerar_resposta_padrao(
            f"<html><body><h1>Resposta GET</h1><p>Dados recebidos: {len(dados)} bytes</p><p>Data/Hora: {datetime.now()}</p></body></html>",
            "200 OK"
        )

    def processar_post(self, dados):
        corpo = ""
        parametros = {}

        linhas = dados.split('\n')
        separador_encontrado = False

        for linha in linhas:
            if linha.strip() == "":
                separador_encontrado = True
                continue

            if separador_encontrado:
                corpo += linha

        pares = corpo.split('&')
        for par in pares:
            if '=' in par:
                chave, valor = par.split('=', 1)
                parametros[chave] = valor

        return self.gerar_resposta_padrao(
            f"<html><body><h1>Resposta POST</h1><p>Parâmetros: {parametros}</p><p>Data/Hora: {datetime.now()}</p></body></html>",
            "200 OK"
        )

    def gerar_resposta_padrao(self, conteudo, status="200 OK"):
        resposta = f"HTTP/1.1 {status}\r\n"
        resposta += "Content-Type: text/html; charset=utf-8\r\n"
        resposta += f"Content-Length: {len(conteudo)}\r\n"
        resposta += "Connection: close\r\n"
        resposta += "\r\n"
        resposta += conteudo
        return resposta

    def mostrar_estatisticas(self):
        print("\n=== ESTATÍSTICAS DO SERVIDOR ===")
        print(f"Total de conexões: {self.estatisticas['conexoes']}")
        print(f"Bytes recebidos: {self.estatisticas['bytes_recebidos']}")
        print(f"Requisições GET: {self.estatisticas['get_requests']}")
        print(f"Requisições POST: {self.estatisticas['post_requests']}")

        if self.estatisticas["tempo_processamento"]:
            tempo_medio = np.mean(self.estatisticas["tempo_processamento"])
            print(f"Tempo médio de processamento: {tempo_medio:.4f} segundos")

            self.gerar_grafico_estatisticas()

    def gerar_grafico_estatisticas(self):
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        labels = ['GET', 'POST']
        values = [self.estatisticas['get_requests'], self.estatisticas['post_requests']]
        plt.bar(labels, values, color=['blue', 'green'])
        plt.title('Requisições por Método')
        plt.ylabel('Quantidade')

        plt.subplot(1, 2, 2)
        if len(self.estatisticas["tempo_processamento"]) > 1:
            plt.hist(self.estatisticas["tempo_processamento"], bins=10)
            plt.title('Distribuição de Tempos de Processamento')
            plt.xlabel('Tempo (segundos)')
            plt.ylabel('Frequência')
        else:
            plt.text(0.5, 0.5, 'Dados insuficientes', ha='center', va='center')

        plt.tight_layout()
        plt.savefig('estatisticas_servidor.png')
        print("Gráfico salvo em 'estatisticas_servidor.png'")
        plt.close()

    def parar(self):
        print("Encerrando servidor...")
        self.rodando = False

        for cliente in self.clientes:
            try:
                cliente.close()
            except:
                pass

        try:
            self.servidor.close()
        except:
            pass

        print("Servidor encerrado.")


def main():
    servidor = ServidorTCP()
    servidor.iniciar()


if __name__ == "__main__":
    main()
