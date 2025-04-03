import numpy as np
import time
import matplotlib.pyplot as plt
from cython import boundscheck, wraparound
import pyximport;

pyximport.install(language_level=3)

import os

cython_code = """
from cython.parallel cimport prange
import cython

@cython.boundscheck(False)
@cython.wraparound(False)
def parallel_sum(int[:] arr):
    cdef long total = 0
    cdef int i
    for i in prange(arr.shape[0], nogil=True, schedule='static'):
        total += arr[i]
    return total
"""

with open("parallel_sum.pyx", "w") as f:
    f.write(cython_code)

import parallel_sum


def sequential_sum(arr):
    return sum(arr)


input_sizes = [10000, 50000, 100000, 500000, 1000000]
sequential_times = []
parallel_times = []

for size in input_sizes:
    arr = np.random.randint(1, 100000, size, dtype=np.int32)

    start = time.time()
    s_result = sequential_sum(arr)
    end = time.time()
    sequential_times.append(end - start)

    start = time.time()
    p_result = parallel_sum.parallel_sum(arr)
    end = time.time()
    parallel_times.append(end - start)

plt.figure()
plt.plot(input_sizes, sequential_times, label='Sequencial')
plt.plot(input_sizes, parallel_times, label='Paralelo (OpenMP)')
plt.xlabel('Tamanho do Vetor')
plt.ylabel('Tempo de Execução (s)')
plt.title('Comparação de Desempenho: Soma Sequencial vs Paralela')
plt.legend()
plt.grid(True)
plt.savefig("comparacao_tempo_soma.png")
plt.show()
