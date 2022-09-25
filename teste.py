from DoubleinkedListIterator import DoubleinkedListIterator
from random import randint
from DoubleinkedListIterator import *

######################  Adiciona 30 passageiros aleatórios
def random30(lista):
    i = 0
    while i < 30:
        i = i+1
        people = {
            "nome": i,
            'sobrenome': 'sobrenome',
            'rg': '12345678',
            'status': 'ativo'
        }

        # lista.addNode(randint(0,50))
        lista.addNode(people)
    print('LISTA DE PASSAGEIROS:')
    printLista(lista)

####################### Faz lista de espera
def random10Fila(lista):
    i = 0
    while i < 10:
        i = i+1
        people = {
            "nome": i ,
            'sobrenome': 'sobrenome',
            'rg': '12345678',
            'status': 'espera'
        }

        # lista.addNode(randint(0,50))
        lista.addNode(people)
    print('LISTA DE ESPERA:')
    printLista(lista)


def printLista(lista):
    lista.first_Node() # lista.iterator = lista.iterator.firstNode
    while lista.iterator:
        print(f'{lista.iterator.data}') 
        lista.nextNode() # lista.iterator = lista.iterator.nextNode

def desistir(lista, num):
    i = 0
    while i < num:
        lista.first_Node()
        lista.elimNode()


################# tira da lista
####escolhe um numero aleatório, bota o iterator naquele local e tira a pessoa dali.
def removeRandom(lista, num):
    i = 0
    while i < num:
        if (lista.posNode(randint(0,30))):    
            lista.elimNode()
            i = i+1
            print('entrou')
            print(lista.iterator)
        

passageiros = DoubleinkedListIterator()
random30(passageiros)

espera  = DoubleinkedListIterator()
random10Fila(espera)
removeRandom(passageiros, 5)
print('LISTA COM PASSAGEIROS RETIRADOS: ')
printLista(passageiros)

### TO DO: pegar um passageiro randomico da lista de espera e colocar ele no avião
###good to have: um gerador de rg e nome mais realistico