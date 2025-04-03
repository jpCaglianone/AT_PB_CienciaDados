#!/usr/bin/env python3

CYTHON_CODE = """
# distutils: language = c
# distutils: extra_compile_args = -fopenmp
# distutils: extra_link_args = -fopenmp

import numpy as np
cimport numpy as np
from cython.parallel import prange
import time

def parallel_sum_openmp(np.ndarray[double, ndim=1] arr, int num_threads):
    cdef double start_time = time.time()
    cdef double result = 0.0
    cdef int i
    cdef int n = arr.shape[0]

    cdef int old_num_threads
    from openmp cimport omp_get_max_threads, omp_set_num_threads, omp_get_thread_num

    old_num_threads = omp_get_max_threads()
    omp_set_num_threads(num_threads)

    with nogil:
        result = 0.0
        for i in prange(n, schedule='static'):
            result += arr[i]

    omp_set_num_threads(old_num_threads)

    cdef double elapsed_time = time.time() - start_time
    return result, elapsed_time
"""

SETUP_CODE = """
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        "sum_openmp",
        ["sum_openmp.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
        include_dirs=[numpy.get_include()]
    )
]

setup(
    name="sum_openmp",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    include_dirs=[numpy.get_include()]
)
"""

COMPILE_SCRIPT = """#!/usr/bin/env python3
import os
import sys

def main():
    print("Criando arquivo sum_openmp.pyx...")
    with open("sum_openmp.pyx", "w") as f:
        f.write(CYTHON_CODE)

    print("Criando arquivo setup.py...")
    with open("setup.py", "w") as f:
        f.write(SETUP_CODE)

    print("Compilando extensão Cython com OpenMP...")
    os.system(f"{sys.executable} setup.py build_ext --inplace")

    print("Limpando arquivos temporários...")
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build")

    if os.path.exists("sum_openmp.c") and (
        os.path.exists("sum_openmp.so") or
        os.path.exists("sum_openmp.pyd")
    ):
        print("Compilação concluída com sucesso!")
        return True
    else:
        print("Falha na compilação da extensão Cython.")
        return False

if __name__ == "__main__":
    main()
"""

COMPARE_SCRIPT = """#!/usr/bin/env python3
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import cpu_count

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    import sum_openmp
    HAS_OPENMP = True
    print("✓ Extensão OpenMP carregada com sucesso!")
except ImportError:
    HAS_OPENMP = False
    print("✗ A extensão OpenMP não está disponível. Será usado apenas ThreadPoolExecutor.")

from list_sum import sequential_sum, parallel_sum, create_random_list

def test_all_implementations():
    sizes = [10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]

    max_threads = min(cpu_count(), 16)
    thread_counts = list(range(1, max_threads + 1))

    results = {}

    for size in sizes:
        print(f"\nTestando com array de tamanho {size:,}")

        data = np.random.randint(0, 100, size=size).astype(np.float64)
        data_list = data.tolist()

        seq_result, seq_time = sequential_sum(data_list)
        print(f"Soma sequencial (Python): {seq_result} (tempo: {seq_time:.6f}s)")

        size_results = {
            'sequential': seq_time,
            'thread_pool': [],
            'openmp': [] if HAS_OPENMP else None
        }

        for n_threads in thread_counts:
            result, exec_time = parallel_sum(data_list, n_threads)
            speedup = seq_time / exec_time
            print(f"ThreadPool ({n_threads} threads): {result} (tempo: {exec_time:.6f}s, speedup: {speedup:.2f}x)")
            size_results['thread_pool'].append((n_threads, exec_time, speedup))

        if HAS_OPENMP:
            for n_threads in thread_counts:
                result, exec_time = sum_openmp.parallel_sum_openmp(data, n_threads)
                speedup = seq_time / exec_time
                print(f"OpenMP ({n_threads} threads): {result} (tempo: {exec_time:.6f}s, speedup: {speedup:.2f}x)")
                size_results['openmp'].append((n_threads, exec_time, speedup))

        results[size] = size_results

    generate_comparison_graphs(results, thread_counts)

def generate_comparison_graphs(results, thread_counts):
    sizes = list(results.keys())

    plt.style.use('ggplot')
    colors = plt.cm.Set1(np.linspace(0, 1, 3))

    plt.figure(figsize=(14, 10))

    for i, size in enumerate(sizes):
        x = np.arange(len(thread_counts)) + i * (len(thread_counts) + 2)
        width = 0.35

        seq_time = results[size]['sequential']
        thread_times = [t for _, t, _ in results[size]['thread_pool']]

        plt.bar(x - width/2, thread_times, width, color=colors[0], 
                label=f'ThreadPool ({size:,})' if i == 0 else "")

        if results[size]['openmp']:
            openmp_times = [t for _, t, _ in results[size]['openmp']]
            plt.bar(x + width/2, openmp_times, width, color=colors[1], 
                    label=f'OpenMP ({size:,})' if i == 0 else "")

        plt.plot([x[0] - 1, x[-1] + 1], [seq_time, seq_time], '--', color=colors[2],
                 label=f'Sequencial ({size:,})' if i == 0 else "")

        plt.text(x.mean(), 0, f"{size:,}", ha='center', va='bottom', 
                 fontweight='bold', fontsize=10)

        if i == 0:
            for j, t in enumerate(thread_counts):
                plt.text(x[j], 0, str(t), ha='center', va='bottom', 
                         rotation=90, alpha=0.6)

    plt.xlabel('Tamanho da Lista / Número de Threads')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Comparação de Tempo entre Implementações')
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'implementation_comparison.png'), dpi=300)

    plt.figure(figsize=(14, 10))

    plt.plot(thread_counts, thread_counts, 'k--', alpha=0.7, label='Speedup Ideal')

    for size in sizes:
        _, _, speedups_thread = zip(*results[size]['thread_pool'])
        plt.plot(thread_counts, speedups_thread, 'o-', linewidth=2, 
                 label=f'ThreadPool ({size:,})')

        if results[size]['openmp']:
            _, _, speedups_openmp = zip(*results[size]['openmp'])
            plt.plot(thread_counts, speedups_openmp, 's-', linewidth=2, 
                     label=f'OpenMP ({size:,})')

    plt.xlabel('Número de Threads')
    plt.ylabel('Speedup')
    plt.title('Comparação de Speedup entre Implementações')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'implementation_speedup.png'), dpi=300)

    print(f"\nGráficos comparativos salvos em: {SCRIPT_DIR}")

if __name__ == "__main__":
    np.random.seed(42)

    print("Comparação de Implementações para Soma de Lista")
    print("="*70)

    test_all_implementations()
"""

INSTALL_SCRIPT = """#!/usr/bin/env bash

echo "Instalando dependências necessárias para o exercício 5.1..."
sudo apt update
sudo apt install -y python3-dev python3-pip cython build-essential

echo "Instalando pacotes Python necessários..."
pip3 install numpy matplotlib cython

echo "Compilando a extensão Cython com OpenMP..."
python3 compile_cython.py

echo "Instalação concluída!"
"""

README = """# Exercício 5.1: Soma de Elementos em uma Lista com OpenMP

Este conjunto de scripts demonstra a soma de elementos em uma lista usando diferentes implementações:
1. Sequencial pura (Python)
2. Paralela com ThreadPoolExecutor (Python)
3. Paralela com OpenMP nativo (via Cython)

## Requisitos
- Ubuntu Linux
- Python 3.6+
- Compilador C (gcc)
- Pacotes Python: numpy, matplotlib, cython

## Instalação
Execute o script de instalação para configurar o ambiente:
```
chmod +x install.sh
./install.sh
```

## Uso
1. Execute o script principal para testar a implementação ThreadPool:
```
python3 list_sum.py
```

2. Execute o script de comparação para testar todas as implementações:
```
python3 compare_implementations.py
```

## Arquivos Gerados
- `execution_time_vs_threads.png`: Tempo de execução por número de threads
- `speedup_vs_threads.png`: Speedup por número de threads
- `sequential_vs_parallel.png`: Comparação sequencial vs paralelo
- `efficiency_vs_threads.png`: Eficiência por número de threads
- `implementation_comparison.png`: Comparação entre implementações
- `implementation_speedup.png`: Speedup entre implementações
"""

EXTRACT_ALL = """#!/usr/bin/env python3
import os
import sys

FILES = {
    "list_sum.py": LIST_SUM_CODE,
    "compile_cython.py": COMPILE_SCRIPT,
    "compare_implementations.py": COMPARE_SCRIPT,
    "install.sh": INSTALL_SCRIPT,
    "README.md": README
}

def extract_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Criando arquivos para o Exercício 5.1 em: {current_dir}")

    for filename, content in FILES.items():
        file_path = os.path.join(current_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)

        if filename.endswith(".sh") or filename.endswith(".py"):
            os.chmod(file_path, 0o755)

    print("Todos os arquivos foram criados com sucesso.")
    print("\nPara instalar as dependências, execute:")
    print("  ./install.sh")
    print("\nPara executar os testes:")
    print("  python3 list_sum.py")
    print("  python3 compare_implementations.py")

if __name__ == "__main__":
    extract_files()
"""