import os
import asyncio
from PIL import Image, ImageFilter
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor




def processar_imagem(imagem_path, salvar_path):
   imagem = Image.open(imagem_path)
   imagem_filtrada = imagem.filter(ImageFilter.CONTOUR)
   nome_imagem = os.path.basename(imagem_path)
   imagem_filtrada.save(os.path.join(salvar_path, nome_imagem))




async def processar_imagens_assincronas(imagem_path, pasta_saida, num_threads):
   loop = asyncio.get_event_loop()
   executor = ThreadPoolExecutor(max_workers=num_threads)
   tarefas = []


   tarefas.append(loop.run_in_executor(executor, processar_imagem, imagem_path, pasta_saida))


   await asyncio.gather(*tarefas)




def medir_tempo_execucao(imagem_path, pasta_saida, num_threads):
   start_time = time.time()
   asyncio.run(processar_imagens_assincronas(imagem_path, pasta_saida, num_threads))
   return time.time() - start_time




def gerar_grafico():
   tempos = []
   num_threads_list = [1, 2, 4, 8, 16]


   imagem_path = r'C:\Users\jpCaglianone\Desktop\A.jpg'
   pasta_saida = r'C:\Users\jpCaglianone\Desktop'


   for num_threads in num_threads_list:
       tempo = medir_tempo_execucao(imagem_path, pasta_saida, num_threads)
       tempos.append(tempo)


   plt.plot(num_threads_list, tempos, marker='o')
   plt.xlabel('Número de Threads')
   plt.ylabel('Tempo de Execução (segundos)')
   plt.title('Tempo de Execução x Número de Threads')
   plt.show()




gerar_grafico()
