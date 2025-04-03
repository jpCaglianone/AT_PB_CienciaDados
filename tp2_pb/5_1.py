#!/usr/bin/env python3

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_random_list(size, max_value=100):
    return np.random.randint(0, max_value, size=size).tolist()


def sequential_sum(numbers):
    start_time = time.time()
    result = sum(numbers)
    elapsed_time = time.time() - start_time
    return result, elapsed_time


def parallel_sum(numbers, n_threads):
    start_time = time.time()

    chunk_size = len(numbers) // n_threads

    def sum_chunk(start_idx):
        end_idx = min(start_idx + chunk_size, len(numbers))
        return sum(numbers[start_idx:end_idx])

    chunk_starts = range(0, len(numbers), chunk_size)

    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        partial_sums = list(executor.map(sum_chunk, chunk_starts))

    result = sum(partial_sums)
    elapsed_time = time.time() - start_time

    return result, elapsed_time


def run_tests():
    sizes = [10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]

    max_threads = min(cpu_count(), 16)
    thread_counts = list(range(1, max_threads + 1))

    all_results = {}

    for size in sizes:
        print(f"\nTestando com lista de tamanho {size:,}")

        numbers = create_random_list(size)

        seq_result, seq_time = sequential_sum(numbers)
        print(f"Soma sequencial: {seq_result} (tempo: {seq_time:.6f}s)")

        size_results = {
            'sequential': seq_time,
            'parallel': []
        }

        for n_threads in thread_counts:
            par_result, par_time = parallel_sum(numbers, n_threads)
            speedup = seq_time / par_time

            if par_result != seq_result:
                print(f"ERRO: Resultado paralelo ({par_result}) difere do sequencial ({seq_result})")

            print(f"Threads: {n_threads}, Tempo: {par_time:.6f}s, Speedup: {speedup:.2f}x")
            size_results['parallel'].append((n_threads, par_time, speedup))

        all_results[size] = size_results

    generate_graphs(all_results, thread_counts)

    print(f"\nGráficos salvos em: {SCRIPT_DIR}")


def generate_graphs(all_results, thread_counts):
    sizes = list(all_results.keys())

    plt.style.use('ggplot')

    plt.figure(figsize=(12, 8))
    for size in sizes:
        seq_time = all_results[size]['sequential']
        plt.axhline(y=seq_time, linestyle='--', alpha=0.3,
                    color=plt.cm.tab10(sizes.index(size) % 10),
                    label=f'Sequencial ({size:,})')

        threads, times, _ = zip(*all_results[size]['parallel'])
        plt.plot(threads, times, 'o-', linewidth=2, markersize=6,
                 label=f'Paralelo ({size:,})')

    plt.xlabel('Número de Threads')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Tempo de Execução vs. Número de Threads')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(SCRIPT_DIR, 'execution_time_vs_threads.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(12, 8))

    plt.plot(thread_counts, thread_counts, 'k--', alpha=0.7, label='Speedup Ideal')

    for size in sizes:
        threads, _, speedups = zip(*all_results[size]['parallel'])
        plt.plot(threads, speedups, 'o-', linewidth=2, markersize=6,
                 label=f'Tamanho: {size:,}')

    plt.xlabel('Número de Threads')
    plt.ylabel('Speedup (Tempo Sequencial / Tempo Paralelo)')
    plt.title('Speedup vs. Número de Threads')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(SCRIPT_DIR, 'speedup_vs_threads.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(12, 8))

    seq_times = [all_results[size]['sequential'] for size in sizes]

    best_par_times = []
    for size in sizes:
        min_time = min(all_results[size]['parallel'], key=lambda x: x[1])[1]
        best_par_times.append(min_time)

    x = np.arange(len(sizes))
    width = 0.35

    plt.bar(x - width / 2, seq_times, width, label='Sequencial')
    plt.bar(x + width / 2, best_par_times, width, label='Paralelo (melhor)')

    plt.xlabel('Tamanho da Lista')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Comparação Sequencial vs Paralelo (Melhor Caso)')
    plt.xticks(x, [f'{size:,}' for size in sizes], rotation=45)
    plt.grid(True, alpha=0.3)
    plt.legend()

    for i, (seq, par) in enumerate(zip(seq_times, best_par_times)):
        speedup = seq / par
        plt.text(i, par, f'{speedup:.2f}x', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'sequential_vs_parallel.png'), dpi=300, bbox_inches='tight')

    plt.figure(figsize=(12, 8))

    for size in sizes:
        threads, _, speedups = zip(*all_results[size]['parallel'])
        efficiency = [s / t for s, t in zip(speedups, threads)]

        plt.plot(threads, efficiency, 'o-', linewidth=2, markersize=6,
                 label=f'Tamanho: {size:,}')

    plt.axhline(y=1.0, linestyle='--', color='k', alpha=0.7, label='Eficiência Ideal')
    plt.xlabel('Número de Threads')
    plt.ylabel('Eficiência (Speedup / Número de Threads)')
    plt.title('Eficiência vs. Número de Threads')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(SCRIPT_DIR, 'efficiency_vs_threads.png'), dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    np.random.seed(42)

    print("Exercício 5.1: Soma de Elementos em uma Lista com OpenMP")
    print("=" * 70)
    print(f"Número de CPUs disponíveis: {cpu_count()}")
    print("=" * 70)

    run_tests()