import random

class ErrorEnteroMasPequeño(Exception):
    pass

class ErrorEnteroMasGrande(Exception):
    pass

num_random = random.randint(1, 100)
numero = 0

while numero != num_random:
    try:
        numero = int(input("Disme un numero: "))

        if(numero > num_random):
            print("EL número introduzido es mayor")
        elif(numero<num_random):
            print("EL número introduzido es menor")
        else:
            print("Correcto, es el numero " + str(numero))
    except ErrorEnteroMasGrande:
        print(str(numero)+"es mas grande")
    except ErrorEnteroMasPequeño:
        print(str(numero)+"es mas pequeño")
    except ValueError:
        print("Hay algo mal!!")    
