import threading
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue
from concurrent.futures import ThreadPoolExecutor




class Node:
   def __init__(self, value):
       self.value = value
       self.left = None
       self.right = None




class BinaryTree:
   def __init__(self):
       self.root = None
       self.max_value = float('-inf')
       self.max_lock = threading.Lock()


   def insert(self, value):
       if not self.root:
           self.root = Node(value)
           return


       current = self.root
       while True:
           if value < current.value:
               if current.left is None:
                   current.left = Node(value)
                   break
               current = current.left
           else:
               if current.right is None:
                   current.right = Node(value)
                   break
               current = current.right


   def sequential_find_max(self, node):
       if not node:
           return float('-inf')


       left_max = self.sequential_find_max(node.left)
       right_max = self.sequential_find_max(node.right)


       return max(node.value, left_max, right_max)


   def parallel_find_max_subtree(self, node):
       if not node:
           return


       with self.max_lock:
           self.max_value = max(self.max_value, node.value)


       threads = []
       if node.left:
           left_thread = threading.Thread(
               target=self.parallel_find_max_subtree,
               args=(node.left,)
           )
           threads.append(left_thread)
           left_thread.start()


       if node.right:
           right_thread = threading.Thread(
               target=self.parallel_find_max_subtree,
               args=(node.right,)
           )
           threads.append(right_thread)
           right_thread.start()


       for thread in threads:
           thread.join()


   def parallel_find_max(self):
       if not self.root:
           return None


       self.max_value = float('-inf')
       self.parallel_find_max_subtree(self.root)
       return self.max_value




def create_balanced_tree(size):
   # Ensure range is at least twice the size needed to guarantee unique values
   range_max = size * 3
   values = random.sample(range(1, range_max), size)
   tree = BinaryTree()


   def insert_balanced(arr):
       if not arr:
           return
       mid = len(arr) // 2
       tree.insert(arr[mid])
       insert_balanced(arr[:mid])
       insert_balanced(arr[mid + 1:])


   insert_balanced(sorted(values))
   return tree, max(values)




def run_performance_test(tree_size):
   tree, actual_max = create_balanced_tree(tree_size)


   start_time = time.time()
   seq_max = tree.sequential_find_max(tree.root)
   sequential_time = time.time() - start_time


   start_time = time.time()
   par_max = tree.parallel_find_max()
   parallel_time = time.time() - start_time


   assert seq_max == par_max == actual_max, "Maximum values do not match!"
   return sequential_time, parallel_time




def run_all_tests():
   tree_sizes = [100, 500, 1000, 5000, 10000]
   sequential_results = []
   parallel_results = []


   for size in tree_sizes:
       print(f"Testing with tree size {size}...")
       seq_time, par_time = run_performance_test(size)
       sequential_results.append(seq_time)
       parallel_results.append(par_time)
       print(f"Sequential time: {seq_time:.4f}s")
       print(f"Parallel time: {par_time:.4f}s")


   save_results(tree_sizes, sequential_results, parallel_results)




def save_results(sizes, sequential_times, parallel_times):
   with open("tp3_3.3.txt", "w") as f:
       f.write("Maximum Value Search Performance Analysis\n")
       f.write("=" * 50 + "\n\n")
       f.write("Test Parameters:\n")
       f.write("- Random balanced binary trees\n")
       f.write("- Values randomly distributed\n\n")
       f.write("Results:\n")
       f.write("-" * 30 + "\n")


       for i, size in enumerate(sizes):
           f.write(f"\nTree Size: {size}\n")
           f.write(f"Sequential Search Time: {sequential_times[i]:.4f} seconds\n")
           f.write(f"Parallel Search Time: {parallel_times[i]:.4f} seconds\n")
           speedup = sequential_times[i] / parallel_times[i]
           f.write(f"Speedup: {speedup:.2f}x\n")


   plt.figure(figsize=(12, 6))


   plt.subplot(1, 2, 1)
   plt.plot(sizes, sequential_times, 'b-o', label='Sequential')
   plt.plot(sizes, parallel_times, 'r-o', label='Parallel')
   plt.title('Tempo de Busca do Máximo vs Tamanho da Árvore')
   plt.xlabel('Número de Nós')
   plt.ylabel('Tempo (segundos)')
   plt.legend()
   plt.grid(True)


   plt.subplot(1, 2, 2)
   speedups = [s / p for s, p in zip(sequential_times, parallel_times)]
   plt.plot(sizes, speedups, 'g-o')
   plt.title('Speedup da Busca Paralela')
   plt.xlabel('Número de Nós')
   plt.ylabel('Speedup (Sequential/Parallel)')
   plt.grid(True)


   plt.tight_layout()
   plt.savefig('tp3_3.3.png', dpi=300, bbox_inches='tight')
   plt.close()




if __name__ == "__main__":
   example_tree = BinaryTree()
   example_values = [15, 10, 20, 8, 12, 17, 25]
   for value in example_values:
       example_tree.insert(value)


   print("Testing example tree with values:", example_values)


   start = time.time()
   seq_max = example_tree.sequential_find_max(example_tree.root)
   seq_time = time.time() - start


   start = time.time()
   par_max = example_tree.parallel_find_max()
   par_time = time.time() - start


   print(f"\nSequential maximum value: {seq_max}")
   print(f"Sequential search time: {seq_time:.6f} seconds")
   print(f"\nParallel maximum value: {par_max}")
   print(f"Parallel search time: {par_time:.6f} seconds")


   print("\nStarting performance tests...")
   run_all_tests()


