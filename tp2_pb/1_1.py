

import asyncio
import aiohttp
import time
import matplotlib.pyplot as plt
import numpy as np


async def download_url(session, url, semaphore):
   async with semaphore:
       try:
           async with session.get(url) as response:
               content = await response.text()
               return len(content)
       except Exception as e:
           print(f"Erro ao baixar {url}: {str(e)}")
           return 0




async def batch_download(urls, max_concurrent):
   semaphore = asyncio.Semaphore(max_concurrent)
   async with aiohttp.ClientSession() as session:
       tasks = [download_url(session, url, semaphore) for url in urls]
       results = await asyncio.gather(*tasks, return_exceptions=True)
       return results




def generate_urls(n):
   base_urls = [
       "https://jsonplaceholder.typicode.com/posts/",
       "https://jsonplaceholder.typicode.com/comments/",
       "https://jsonplaceholder.typicode.com/albums/",
       "https://jsonplaceholder.typicode.com/photos/",
       "https://jsonplaceholder.typicode.com/todos/",
       "https://jsonplaceholder.typicode.com/users/"
   ]


   urls = []
   for i in range(n):
       base_url = base_urls[i % len(base_urls)]
       urls.append(f"{base_url}{i + 1}")
   return urls




async def run_experiment(n_urls, max_concurrent):
   urls = generate_urls(n_urls)
   start_time = time.time()
   results = await batch_download(urls, max_concurrent)
   end_time = time.time()
   successful_downloads = sum(1 for r in results if isinstance(r, int) and r > 0)
   return end_time - start_time, successful_downloads




def plot_results(concurrent_values, times, successes, n_urls):
   plt.figure(figsize=(12, 6))


   plt.subplot(1, 2, 1)
   plt.plot(concurrent_values, times, 'b-o')
   plt.xlabel('Número de Downloads Simultâneos')
   plt.ylabel('Tempo Total (segundos)')
   plt.title('Tempo de Download vs. Concorrência')
   plt.grid(True)


   best_idx = np.argmin(times)
   plt.plot(concurrent_values[best_idx], times[best_idx], 'r*',
            label=f'Melhor tempo: {times[best_idx]:.2f}s\ncom {concurrent_values[best_idx]} threads')
   plt.legend()


   plt.subplot(1, 2, 2)
   plt.plot(concurrent_values, successes, 'g-o')
   plt.xlabel('Número de Downloads Simultâneos')
   plt.ylabel('Downloads com Sucesso')
   plt.title('Downloads Bem-sucedidos vs. Concorrência')
   plt.grid(True)


   plt.tight_layout()
   return plt




async def main():
   n_urls = 50
   concurrent_values = [1, 2, 5, 10, 20, 30, 40, 50]


   results = []
   print(f"\nIniciando experimento com {n_urls} URLs...")
   print("-" * 50)


   for concurrent in concurrent_values:
       print(f"Testando com {concurrent} downloads simultâneos...")
       time_taken, successful = await run_experiment(n_urls, concurrent)
       results.append((time_taken, successful))
       print(f"Tempo: {time_taken:.2f}s, Downloads com sucesso: {successful}/{n_urls}")


   times, successes = zip(*results)


   plt = plot_results(concurrent_values, times, successes, n_urls)


   best_time_idx = np.argmin(times)
   best_concurrent = concurrent_values[best_time_idx]
   best_time = times[best_time_idx]


   print("\nResultados da Análise:")
   print("-" * 50)
   print(f"Melhor número de downloads simultâneos: {best_concurrent}")
   print(f"Melhor tempo alcançado: {best_time:.2f} segundos")
   print(f"Média de downloads bem-sucedidos: {np.mean(successes):.1f}")


   plt.show()


if __name__ == "__main__":
   asyncio.run(main())
