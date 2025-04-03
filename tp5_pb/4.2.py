
# !/usr/bin/env python3

from scapy.all import Ether, sendp
import random
from scapy.all import ARP, sniff
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import threading


class DetectorArpSpoofing:
    def __init__(self):
        self.mapeamento_ip_mac = {}
        self.alertas = []
        self.tempos_processamento = []
        self.pacotes_processados = 0
        self.tempo_inicio = 0
        self.duracao_teste = 0
        self.lock = threading.Lock()

    def processar_pacote(self, pacote):
        if not pacote.haslayer(ARP):
            return

        inicio_processamento = time.time()

        if pacote[ARP].op == 2:  # Resposta ARP
            ip_origem = pacote[ARP].psrc
            mac_origem = pacote[ARP].hwsrc

            with self.lock:
                self.pacotes_processados += 1

                if ip_origem in self.mapeamento_ip_mac:
                    mac_anterior = self.mapeamento_ip_mac[ip_origem]
                    if mac_origem != mac_anterior:
                        alerta = f"Alerta: Possível ARP Spoofing detectado para IP {ip_origem}! MAC anterior: {mac_anterior}, MAC atual: {mac_origem}"
                        print(alerta)
                        self.alertas.append({
                            'ip': ip_origem,
                            'mac_anterior': mac_anterior,
                            'mac_atual': mac_origem,
                            'timestamp': time.time()
                        })

                self.mapeamento_ip_mac[ip_origem] = mac_origem

                tempo_processamento = time.time() - inicio_processamento
                self.tempos_processamento.append(tempo_processamento)

    def iniciar_monitoramento(self, interface="eth0", duracao=60):
        self.tempo_inicio = time.time()
        self.duracao_teste = duracao

        print(f"Iniciando monitoramento na interface {interface} por {duracao} segundos...")
        sniff(iface=interface, prn=self.processar_pacote, store=0, timeout=duracao)

        tempo_total = time.time() - self.tempo_inicio
        print(f"\nMonitoramento finalizado. Duração: {tempo_total:.2f} segundos")
        print(f"Total de pacotes ARP processados: {self.pacotes_processados}")
        print(f"Total de alertas de ARP Spoofing: {len(self.alertas)}")

        return {
            'pacotes_processados': self.pacotes_processados,
            'alertas': len(self.alertas),
            'tempo_total': tempo_total,
            'tempos_processamento': self.tempos_processamento
        }


def gerar_trafego_arp_falso(interface, quantidade_pacotes, intervalo=1):


    print(f"Gerando {quantidade_pacotes} pacotes ARP falsos para testes...")

    ips_teste = ["192.168.1." + str(i) for i in range(1, 11)]

    for _ in range(quantidade_pacotes):
        ip_alvo = random.choice(ips_teste)
        mac_falso = ":".join([format(random.randint(0, 255), "02x") for _ in range(6)])

        pacote_arp = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=2, psrc=ip_alvo, hwsrc=mac_falso)
        sendp(pacote_arp, iface=interface, verbose=0)

        time.sleep(intervalo)


def executar_teste(interface, duracao, gerar_falsos=True, quantidade_falsos=20):
    detector = DetectorArpSpoofing()

    if gerar_falsos:
        thread_geracao = threading.Thread(
            target=gerar_trafego_arp_falso,
            args=(interface, quantidade_falsos, duracao /quantidade_falsos)
        )
        thread_geracao.daemon = True
        thread_geracao.start()

    resultados = detector.iniciar_monitoramento(interface, duracao)
    return resultados


def gerar_graficos(resultados_testes):
    # Gráfico 1: Pacotes processados vs. Tempo total
    pacotes = [resultado['pacotes_processados'] for resultado in resultados_testes]
    tempos = [resultado['tempo_total'] for resultado in resultados_testes]

    plt.figure(figsize=(10, 6))
    plt.plot(pacotes, tempos, marker='o', linestyle='-')
    plt.xlabel('Quantidade de Pacotes Processados')
    plt.ylabel('Tempo Total (segundos)')
    plt.title('Tempo Total vs. Quantidade de Pacotes')
    plt.grid(True)
    plt.savefig('grafico_tempo_pacotes.png')

    # Gráfico 2: Comparação com a complexidade O(1) por pacote
    plt.figure(figsize=(10, 6))
    plt.plot(pacotes, [ p /1000 for p in pacotes], marker='o', linestyle='-', label='O(1) por pacote (normalizado)')
    plt.plot(pacotes, tempos, marker='x', linestyle='--', label='Tempo Real')
    plt.xlabel('Quantidade de Pacotes')
    plt.ylabel('Tempo (segundos)')
    plt.title('Complexidade Teórica vs. Tempo Real')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_complexidade.png')

    # Gráfico 3: Tempo médio de processamento por pacote vs. Quantidade de pacotes
    tempos_medios = []
    for resultado in resultados_testes:
        if resultado['pacotes_processados'] > 0:
            tempo_medio = sum(resultado['tempos_processamento']) / resultado['pacotes_processados']
        else:
            tempo_medio = 0
        tempos_medios.append(tempo_medio * 1000)  # Convertendo para milissegundos

    plt.figure(figsize=(10, 6))
    plt.plot(pacotes, tempos_medios, marker='o', linestyle='-')
    plt.xlabel('Quantidade de Pacotes Processados')
    plt.ylabel('Tempo Médio por Pacote (ms)')
    plt.title('Tempo Médio de Processamento por Pacote')
    plt.grid(True)
    plt.savefig('grafico_tempo_medio.png')


def main():
    interface = "eth0"  # Altere para a interface de rede correta
    resultados_testes = []

    duracoes_teste = [10, 20, 30, 60, 120]
    quantidades_falsos = [5, 15, 30, 60, 100]

    for i, duracao in enumerate(duracoes_teste):
        print(f"\n\n=== Teste { i +1}/{len(duracoes_teste)} ===")
        print(f"Duração: {duracao} segundos, Pacotes falsos: {quantidades_falsos[i]}")

        resultado = executar_teste(interface, duracao, True, quantidades_falsos[i])
        resultados_testes.append(resultado)

    gerar_graficos(resultados_testes)
    print("\nGráficos salvos: grafico_tempo_pacotes.png, grafico_complexidade.png e grafico_tempo_medio.png")


if __name__ == "__main__":
    main()
