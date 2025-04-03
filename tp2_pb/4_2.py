import time
from functools import lru_cache
import matplotlib.pyplot as plt
import numpy as np


def fib_recursive(n):
   if n <= 1:
       return n
   return fib_recursive(n - 1) + fib_recursive(n - 2)


@lru_cache(maxsize=None)
def fib_memoized(n):
   if n <= 1:
       return n
   return fib_memoized(n - 1) + fib_memoized(n - 2)


def fib_memo_dict(n, memo=None):
   if memo is None:
       memo = {}
   if n <= 1:
       return n
   if n not in memo:
       memo[n] = fib_memo_dict(n - 1, memo) + fib_memo_dict(n - 2, memo)
   return memo[n]


def measure_time(func, n):
   start_time = time.time()
   result = func(n)
   end_time = time.time()
   return result, end_time - start_time


def plot_performance_comparison(ns, max_recursive):
   times_memo = []
   times_dict = []
   times_rec = []


   for n in ns:
       _, time_memo = measure_time(fib_memoized, n)
       times_memo.append(time_memo)


       _, time_dict = measure_time(lambda x: fib_memo_dict(x), n)
       times_dict.append(time_dict)


       if n <= max_recursive:
           _, time_rec = measure_time(fib_recursive, n)
           times_rec.append(time_rec)


   plt.figure(figsize=(12, 6))
   plt.plot(ns, times_memo, 'b-', label='Memorização (decorator)', marker='o')
   plt.plot(ns, times_dict, 'g-', label='Memorização (dicionário)', marker='s')


   if len(times_rec) > 0:
       plt.plot(ns[:len(times_rec)], times_rec, 'r-', label='Recursivo', marker='^')


   plt.xlabel('n')
   plt.ylabel('Tempo (segundos)')
   plt.title('Comparação de Desempenho das Implementações de Fibonacci')
   plt.grid(True)
   plt.legend()
   plt.yscale('log')
   plt.show()


def compare_implementations(n, max_recursive):
   print(f"\nComparando implementações para n = {n}:")


   result_memo, time_memo = measure_time(fib_memoized, n)
   print(f"Fibonacci com memorização (decorator):")
   print(f"Resultado: {result_memo}")
   print(f"Tempo: {time_memo:.6f} segundos")


   result_dict, time_dict = measure_time(lambda x: fib_memo_dict(x), n)
   print(f"\nFibonacci com memorização (dicionário):")
   print(f"Resultado: {result_dict}")
   print(f"Tempo: {time_dict:.6f} segundos")


   if n <= max_recursive:
       result_rec, time_rec = measure_time(fib_recursive, n)
       print(f"\nFibonacci sem memorização:")
       print(f"Resultado: {result_rec}")
       print(f"Tempo: {time_rec:.6f} segundos")
   else:
       print("\nFibonacci sem memorização não executado (n muito grande)")


if __name__ == "__main__":
   x = 30
   max_recursive = 30
   print(f" ---- {x} ------")
   compare_implementations(x, max_recursive)
   ns = range(5, x + 1, 5)
   plot_performance_comparison(ns, max_recursive)








