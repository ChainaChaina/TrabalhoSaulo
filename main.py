from arvore import AVLTree
from fila import Queue

tree = AVLTree()  #estanciando objeto arvore
queue = Queue()  #estanciando objeto fila

# abrindo um arquivo na variável 'File'.


def openArquivo():
  print("digite o nome do arquivo com os dados:\n")
  arquivo = input()
  with open(arquivo, "r", encoding="UTF-8") as file:
    for item in file:
      words = item.strip()
      tree.insert(words)


def tenta():
  try:
   openArquivo()
  except:
    print(" ")
    print("Arquivo nao existe, tente de novo")
    tenta()


tenta()


entrada = "0"
while entrada != "3":
  print("\nDigite a opção:\n 1- Mudar arquivo de entrada\n 2- Imprimir arvore por nível\n 3- Encerrar\n")
  entrada = input()
  if entrada == "1":
    tenta()
  elif entrada == "2":
    print(" ")
    print("CAMINHAMENTO POR NÍVEL:")
    tree.levelorder(0)
    print(" ")

  elif entrada == "3":
    print("Encerrado!")
    print("Me passa ai, Saulo, por favor!")
    break
  else:
    print("entrada invalida")




