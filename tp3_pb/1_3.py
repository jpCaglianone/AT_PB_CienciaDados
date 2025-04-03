import matplotlib.pyplot as plt


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
       else:
           if no.direita is None:
               no.direita = No(valor)
           else:
               self._inserir(no.direita, valor)


   def em_ordem(self, no, resultado=None):
       if resultado is None:
           resultado = []
       if no is not None:
           self.em_ordem(no.esquerda, resultado)
           resultado.append(no.valor)
           self.em_ordem(no.direita, resultado)
       return resultado


   def remover(self, valor):
       self.raiz = self._remover(self.raiz, valor)


   def _remover(self, no, valor):
       if no is None:
           return no
       if valor < no.valor:
           no.esquerda = self._remover(no.esquerda, valor)
       elif valor > no.valor:
           no.direita = self._remover(no.direita, valor)
       else:
           if no.esquerda is None:
               return no.direita
           elif no.direita is None:
               return no.esquerda
           sucessor = self._minValueNode(no.direita)
           no.valor = sucessor.valor
           no.direita = self._remover(no.direita, sucessor.valor)
       return no


   def _minValueNode(self, no):
       atual = no
       while atual.esquerda is not None:
           atual = atual.esquerda
       return atual


tree = ArvoreBinaria()
for valor in [50, 30, 70, 20, 40, 60, 80]:
   tree.inserir(valor)


inorder_original = tree.em_ordem(tree.raiz)
tree.remover(20)
inorder_after_20 = tree.em_ordem(tree.raiz)
tree.remover(30)
inorder_after_30 = tree.em_ordem(tree.raiz)
tree.remover(50)
inorder_after_50 = tree.em_ordem(tree.raiz)


steps = [("Original", inorder_original), ("After deleting 20", inorder_after_20), ("After deleting 30", inorder_after_30), ("After deleting 50", inorder_after_50)]


fig, axs = plt.subplots(2, 2, figsize=(10, 8))
axs = axs.flatten()
for i, (title, seq) in enumerate(steps):
   axs[i].plot(range(len(seq)), seq, marker='o', linestyle='-')
   axs[i].set_title(title)
   axs[i].set_xticks(range(len(seq)))
   axs[i].set_xticklabels(seq)
plt.tight_layout()
plt.savefig("tp3_1.3.png")


with open("tp3_1.3.txt", "w") as f:
   for title, seq in steps:
       f.write(f"{title}: {seq}\n")




