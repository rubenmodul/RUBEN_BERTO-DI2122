##Definix una llista i utilitzant filter, que la separe en dues llistes, una amb elements parells i l'altra amb els senars

llista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

nova_llista_parells = list(filter(lambda x: x%2 == 0, llista))

nova_llista_imparells = list(filter(lambda x: x%2 != 0, llista))


print(nova_llista_parells)
print(nova_llista_imparells)