

import concurrent.futures


class No:
   def __init__(self, valor):
       self.valor = valor
       self.esquerda = None
       self.direita = None




class ArvoreBinaria:
   def __init__(self):
       self.raiz = None


   def inserir(self, valor):
       if self.raiz is None:
           self.raiz = No(valor)
       else:
           self._inserir(self.raiz, valor)


   def _inserir(self, no, valor):
       if valor < no.valor:
           if no.esquerda is None:
               no.esquerda = No(valor)
           else:
               self._inserir(no.esquerda, valor)
       elif valor > no.valor:
           if no.direita is None:
               no.direita = No(valor)
           else:
               self._inserir(no.direita, valor)


   def buscar(self, valor):
       return self._buscar(self.raiz, valor)


   def _buscar(self, no, valor):
       if no is None:
           return False
       if no.valor == valor:
           return True
       elif valor < no.valor:
           return self._buscar(no.esquerda, valor)
       else:
           return self._buscar(no.direita, valor)




class ArvoreBinariaParalela(ArvoreBinaria):
   def buscar_paralelo(self, valor):
       return self._buscar_paralelo(self.raiz, valor)


   def _buscar_paralelo(self, no, valor):
       if no is None:
           return False
       if no.valor == valor:
           return True


       with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
           futuro_esquerda = executor.submit(self._buscar_paralelo, no.esquerda, valor)
           futuro_direita = executor.submit(self._buscar_paralelo, no.direita, valor)


           return futuro_esquerda.result() or futuro_direita.result()
