

import ipaddress
import time
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import os




class TrieNode:
   def __init__(self):
       self.children = {}
       self.prefix = None




class IPv6Trie:
   def __init__(self):
       self.root = TrieNode()


   def insert(self, prefix):
       try:
           net = ipaddress.IPv6Network(prefix, strict=False)
           node = self.root
           ip_int = int(net.network_address)
           prefix_len = net.prefixlen


           for i in range(128):
               if i < prefix_len:
                   bit = (ip_int >> (127 - i)) & 1
                   if bit not in node.children:
                       node.children[bit] = TrieNode()
                   node = node.children[bit]
                   if i == prefix_len - 1:
                       node.prefix = prefix
       except ValueError as e:
           return None


   def longest_prefix_match(self, ip):
       try:
           ip_addr = ipaddress.IPv6Address(ip)
           node = self.root
           best_match = None
           ip_int = int(ip_addr)


           for i in range(128):
               bit = (ip_int >> (127 - i)) & 1
               if bit not in node.children:
                   break
               node = node.children[bit]
               if node.prefix is not None:
                   best_match = node.prefix
           return best_match
       except ValueError:
           return None




def generate_random_ipv6():
   segments = []
   for _ in range(8):
       segment = hex(randint(0, 65535))[2:].zfill(4)
       segments.append(segment)
   return ':'.join(segments)




def generate_random_prefix():
   ip = generate_random_ipv6()
   mask = randint(16, 64)
   return f"{ip}/{mask}"




def run_performance_test(num_prefixes, num_searches):
   prefixes = [generate_random_prefix() for _ in range(num_prefixes)]
   trie = IPv6Trie()


   start = time.time()
   for prefix in prefixes:
       trie.insert(prefix)
   end = time.time()
   insertion_time = end - start


   ips = [generate_random_ipv6() for _ in range(num_searches)]
   start = time.time()
   for ip in ips:
       trie.longest_prefix_match(ip)
   end = time.time()
   search_time = end - start


   return insertion_time, search_time




def run_all_tests(base_name="tp3_4.3"):
   prefix_counts = [100, 500, 1000, 5000, 10000]
   search_count = 1000
   insertion_results = {}
   search_results = {}


   for count in prefix_counts:
       print(f"Testing with {count} prefixes and {search_count} searches...")
       ins_time, search_time = run_performance_test(count, search_count)
       insertion_results[count] = ins_time
       search_results[count] = search_time
       print(f"Insertion time: {ins_time:.2f} seconds")
       print(f"Search time: {search_time:.2f} seconds")


   save_results(insertion_results, search_results, base_name)
   return insertion_results, search_results




def save_results(insertion_results, search_results, base_name):
   with open(f"{base_name}.txt", "w") as f:
       f.write("IPv6 Trie Performance Test Results\n")
       f.write("=" * 60 + "\n\n")
       f.write("INSERTION TIMES\n")
       f.write("-" * 40 + "\n")
       for count, time_taken in insertion_results.items():
           f.write(f"Prefix count: {count:5d} | Time: {time_taken:.4f} seconds\n")
       f.write("\nSEARCH TIMES\n")
       f.write("-" * 40 + "\n")
       for count, time_taken in search_results.items():
           f.write(f"Trie size: {count:5d} | Time for 1000 searches: {time_taken:.4f} seconds\n")


   plt.figure(figsize=(12, 6))


   counts = list(insertion_results.keys())
   plt.subplot(1, 2, 1)
   plt.plot(counts, list(insertion_results.values()), 'r-o', linewidth=2, markersize=8)
   plt.title('Tempo de Inserção vs Quantidade de Prefixos')
   plt.xlabel('Quantidade de Prefixos')
   plt.ylabel('Tempo de Execução (segundos)')
   plt.grid(True)


   plt.subplot(1, 2, 2)
   plt.plot(counts, list(search_results.values()), 'b-o', linewidth=2, markersize=8)
   plt.title('Tempo de Busca (1000 IPs) vs Tamanho da Trie')
   plt.xlabel('Quantidade de Prefixos na Trie')
   plt.ylabel('Tempo para 1000 Buscas (segundos)')
   plt.grid(True)


   plt.tight_layout()
   plt.savefig(f"{base_name}.png", dpi=300, bbox_inches='tight')
   plt.close()




if __name__ == "__main__":
   test_trie = IPv6Trie()
   test_prefixes = ["2001:db8::/32", "2001:db8:1234::/48"]
   for prefix in test_prefixes:
       test_trie.insert(prefix)


   test_ip = "2001:db8:1234:5678::1"
   result = test_trie.longest_prefix_match(test_ip)
   print(f"\nTest case result:")
   print(f"IP: {test_ip}")
   print(f"Longest prefix match: {result}")


   print("\nStarting performance tests...")
   run_all_tests()
