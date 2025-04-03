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
       self.result_queue = Queue()


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


   def sequential_search(self, node, value):
       if not node:
           return None
       if node.value == value:
           return node
       if value < node.value:
           return self.sequential_search(node.left, value)
       return self.sequential_search(node.right, value)


   def parallel_search_subtree(self, node, value):
       if node and self.result_queue.empty():
           if node.value == value:
               self.result_queue.put(node)
           elif value < node.value:
               self.parallel_search_subtree(node.left, value)
           else:
               self.parallel_search_subtree(node.right, value)


   def parallel_search(self, value):
       if not self.root:
           return None


       if self.root.value == value:
           return self.root


       self.result_queue = Queue()
       threads = []


       if self.root.left:
           left_thread = threading.Thread(
               target=self.parallel_search_subtree,
               args=(self.root.left, value)
           )
           threads.append(left_thread)
           left_thread.start()


       if self.root.right:
           right_thread = threading.Thread(
               target=self.parallel_search_subtree,
               args=(self.root.right, value)
           )
           threads.append(right_thread)
           right_thread.start()


       for thread in threads:
           thread.join()


       return self.result_queue.get() if not self.result_queue.empty() else None




def create_balanced_tree(size):
   values = sorted(random.sample(range(1, size * 2), size))
   tree = BinaryTree()


   def insert_middle(arr):
       if not arr:
           return
       mid = len(arr) // 2
       tree.insert(arr[mid])
       insert_middle(arr[:mid])
       insert_middle(arr[mid + 1:])


   insert_middle(values)
   return tree, values




def run_performance_test(tree_size, num_searches):
   tree, values = create_balanced_tree(tree_size)
   search_values = random.choices(values, k=num_searches)


   start_time = time.time()
   for value in search_values:
       tree.sequential_search(tree.root, value)
   sequential_time = time.time() - start_time


   start_time = time.time()
   for value in search_values:
       tree.parallel_search(value)
   parallel_time = time.time() - start_time


   return sequential_time, parallel_time




def run_all_tests():
   tree_sizes = [100, 500, 1000, 5000, 10000]
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
   with open("tp3_3.1.txt", "w") as f:
       f.write("Binary Tree Search Performance Analysis\n")
       f.write("=" * 50 + "\n\n")
       f.write("Test Parameters:\n")
       f.write("- 100 searches per tree size\n")
       f.write("- Balanced binary trees\n\n")
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
   plt.title('Tempo de Busca vs Tamanho da Árvore')
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
   plt.savefig('tp3_3.1.png', dpi=300, bbox_inches='tight')
   plt.close()




if __name__ == "__main__":
   example_tree = BinaryTree()
   for value in [50, 30, 70, 20, 40, 60, 80]:
       example_tree.insert(value)


   print("Testing example search for value 60...")


   start = time.time()
   seq_result = example_tree.sequential_search(example_tree.root, 60)
   seq_time = time.time() - start


   start = time.time()
   par_result = example_tree.parallel_search(60)
   par_time = time.time() - start


   print(f"\nSequential search result: {seq_result.value if seq_result else None}")
   print(f"Sequential search time: {seq_time:.6f} seconds")
   print(f"\nParallel search result: {par_result.value if par_result else None}")
   print(f"Parallel search time: {par_time:.6f} seconds")


   print("\nStarting performance tests...")
   run_all_tests()


