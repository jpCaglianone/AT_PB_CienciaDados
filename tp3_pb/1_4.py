import matplotlib.pyplot as plt
import math


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
   def is_valid_bst(self, no, min_val=-math.inf, max_val=math.inf):
       if no is None:
           return True
       if no.valor <= min_val or no.valor >= max_val:
           return False
       return self.is_valid_bst(no.esquerda, min_val, no.valor) and self.is_valid_bst(no.direita, no.valor, max_val)


tree = ArvoreBinaria()
for v in [50, 30, 70, 20, 40, 60, 80]:
   tree.inserir(v)
valid_before = tree.is_valid_bst(tree.raiz)
tree.raiz.esquerda.valor = 100
valid_after = tree.is_valid_bst(tree.raiz)
results = [("Antes da alteração", valid_before), ("Depois da alteração", valid_after)]
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
for ax, (title, valid) in zip(axs, results):
   ax.bar([0], ([1] if valid else [0]), color=('green' if valid else 'red'))
   ax.set_xticks([])
   ax.set_ylim(0, 1.5)
   ax.set_title(title)
plt.tight_layout()
plt.savefig("tp3_1.4.png")
with open("tp3_1.4.txt", "w") as f:
   for title, valid in results:
       f.write(f"{title}: {valid}\n")
