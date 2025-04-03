
# !/usr/bin/env python3


from scapy.all import ARP, Ether, srp
import numpy as np
import matplotlib.pyplot as plt
import time
import ipaddress


def varredura_arp(endereco_rede):
    inicio = time.time()

    rede = ipaddress.IPv4Network(endereco_rede)
    hosts_ativos = []

    pacote_arp = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=endereco_rede)

    resultado = srp(pacote_arp, timeout=2, verbose=0)[0]

    for enviado, recebido in resultado:
        hosts_ativos.append({'ip': recebido.psrc, 'mac': recebido.hwsrc})

    fim = time.time()
    tempo_execucao = fim - inicio

    return hosts_ativos, tempo_execucao


def mostrar_resultados(hosts_ativos):
    print("Hosts ativos encontrados:")
    for host in hosts_ativos:
        print(f"IP: {host['ip']}, MAC: {host['mac']}")


def gerar_graficos(tempos, quantidades):
    plt.figure(figsize=(10, 6))
    plt.plot(quantidades, tempos, marker='o', linestyle='-')
    plt.xlabel('Quantidade de IPs')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.title('Tempo de Execução vs Quantidade de IPs')
    plt.grid(True)
    plt.savefig('grafico_tempo_execucao.png')

    plt.figure(figsize=(10, 6))
    plt.plot(quantidades, [quantidade for quantidade in quantidades], marker='o', linestyle='-', label='O(n)')
    plt.plot(quantidades, tempos, marker='x', linestyle='--', label='Tempo Real')
    plt.xlabel('Quantidade de IPs')
    plt.ylabel('Complexidade / Tempo')
    plt.title('Complexidade O(n) vs Tempo Real')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_complexidade.png')


def main():
    redes_teste = [
        "192.168.1.0/28",  # 14 IPs
        "192.168.1.0/26",  # 62 IPs
        "192.168.1.0/25",  # 126 IPs
        "192.168.1.0/24",  # 254 IPs
        "192.168.0.0/23"   # 510 IPs
    ]

    tempos = []
    quantidades = []

    for rede in redes_teste:
        numero_ips = len(list(ipaddress.IPv4Network(rede).hosts()))
        quantidades.append(numero_ips)

        print(f"\nRealizando varredura na rede {rede} ({numero_ips} IPs)...")
        hosts_ativos, tempo = varredura_arp(rede)
        tempos.append(tempo)

        mostrar_resultados(hosts_ativos)
        print(f"Tempo de execução: {tempo:.2f} segundos")

    gerar_graficos(tempos, quantidades)
    print("\nGráficos salvos: grafico_tempo_execucao.png e grafico_complexidade.png")


if __name__ == "__main__":
    main()
