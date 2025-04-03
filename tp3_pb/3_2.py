

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
       self.children = []




class Tree:
   def __init__(self):
       self.root = None
       self.result_queue = Queue()
       self.found_path = None
       self.path_lock = threading.Lock()


   def add_node(self, value, parent_value=None):
       new_node = Node(value)


       if not self.root:
           self.root = new_node
           return True


       if parent_value is not None:
           parent = self._find_node(self.root, parent_value)
           if parent:
               parent.children.append(new_node)
               return True
       return False


   def _find_node(self, node, value):
       if node.value == value:
           return node
       for child in node.children:
           result = self._find_node(child, value)
           if result:
               return result
       return None


   def sequential_dfs_with_path(self, node, target, current_path=None):
       if current_path is None:
           current_path = []


       if not node:
           return None


       current_path.append(node.value)


       if node.value == target:
           return current_path.copy()


       for child in node.children:
           path = self.sequential_dfs_with_path(child, target, current_path)
           if path:
               return path


       current_path.pop()
       return None


   def parallel_dfs_subtree(self, node, target, current_path):
       if not node or self.found_path:
           return


       path = current_path + [node.value]


       if node.value == target:
           with self.path_lock:
               if not self.found_path:
                   self.found_path = path
           return


       threads = []
       for child in node.children:
           thread = threading.Thread(
               target=self.parallel_dfs_subtree,
               args=(child, target, path)
           )
           threads.append(thread)
           thread.start()


       for thread in threads:
           thread.join()


   def parallel_dfs_with_path(self, target):
       if not self.root:
           return None


       self.found_path = None


       if self.root.value == target:
           return [self.root.value]


       threads = []
       for child in self.root.children:
           thread = threading.Thread(
               target=self.parallel_dfs_subtree,
               args=(child, target, [self.root.value])
           )
           threads.append(thread)
           thread.start()


       for thread in threads:
           thread.join()


       return self.found_path




def create_test_tree(size):
   tree = Tree()
   values = list(range(1, size + 1))
   tree.add_node(values[0])


   for i in range(1, size):
       parent_idx = random.randint(0, i - 1)
       tree.add_node(values[i], values[parent_idx])


   return tree, values




def run_performance_test(tree_size, num_searches):
   tree, values = create_test_tree(tree_size)
   search_values = random.choices(values, k=num_searches)


   start_time = time.time()
   for value in search_values:
       tree.sequential_dfs_with_path(tree.root, value)
   sequential_time = time.time() - start_time


   start_time = time.time()
   for value in search_values:
       tree.parallel_dfs_with_path(value)
   parallel_time = time.time() - start_time


   return sequential_time, parallel_time




def run_all_tests():
   tree_sizes = [100, 500, 1000, 2000, 5000]
   num_searches = 100
   sequential_results = []
   parallel_results = []


   for size in tree_sizes:
       print(f"Testing with tree size {size}...")
       seq_time, par_time = run_performance_test(size, num_searches)
       sequential_results.append(seq_time)
       parallel_results.append(par_time)
       print(f"Sequential time: {seq_time:.4f}s")
       print(f"Parallel time: {par_time:.4f}s")


   save_results(tree_sizes, sequential_results, parallel_results)




def save_results(sizes, sequential_times, parallel_times):
   with open("tp3_3.2.txt", "w") as f:
       f.write("DFS with Path Finding Performance Analysis\n")
       f.write("=" * 50 + "\n\n")
       f.write("Test Parameters:\n")
       f.write("- 100 searches per tree size\n")
       f.write("- Random tree structure\n\n")
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
   plt.title('Tempo de Busca DFS vs Tamanho da Árvore')
   plt.xlabel('Número de Nós')
   plt.ylabel('Tempo (segundos)')
   plt.legend()
   plt.grid(True)


   plt.subplot(1, 2, 2)
   speedups = [s / p for s, p in zip(sequential_times, parallel_times)]
   plt.plot(sizes, speedups, 'g-o')
   plt.title('Speedup da Busca DFS Paralela')
   plt.xlabel('Número de Nós')
   plt.ylabel('Speedup (Sequential/Parallel)')
   plt.grid(True)


   plt.tight_layout()
   plt.savefig('tp3_3.2.png', dpi=300, bbox_inches='tight')
   plt.close()




if __name__ == "__main__":
   example_tree = Tree()
   example_tree.add_node(1)
   example_tree.add_node(2, 1)
   example_tree.add_node(3, 1)
   example_tree.add_node(4, 2)
   example_tree.add_node(5, 2)
   example_tree.add_node(6, 3)


   print("Testing example search for value 5...")


   start = time.time()
   seq_path = example_tree.sequential_dfs_with_path(example_tree.root, 5)
   seq_time = time.time() - start


   start = time.time()
   par_path = example_tree.parallel_dfs_with_path(5)
   par_time = time.time() - start


   print(f"\nSequential search path: {seq_path}")
   print(f"Sequential search time: {seq_time:.6f} seconds")
   print(f"\nParallel search path: {par_path}")
   print(f"Parallel search time: {par_time:.6f} seconds")


   print("\nStarting performance tests...")
   run_all_tests()


