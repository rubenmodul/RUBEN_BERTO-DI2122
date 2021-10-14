import os

#Funciones Lambda

suma = lambda x,y: x + y
resta = lambda x,y: x - y
div = lambda x,y: x / y
multi = lambda x,y: x * y


#Ahora abriremos el fichero
try:
    f = open("operacions.txt", 'r')
except FileNotFoundError:
    print("EL fitcher no existix!!")
#Iniciamos un bucle para recorrer todo el fichero
for linia in f:
    try:
        llista = linia.split(" ")

        uno = int(llista[0])
        dos = llista[1]
        tres = int(llista[2])

        if (dos == "+"):
            resultado = suma(uno, tres)
            print(str(uno) + "+" + str(tres) + "=" + str(resultado))


        if (dos == "-"):
            resultado = resta(uno, tres)
            print(str(uno) + "-" + str(tres) + "=" + str(resultado))


        if (dos == "/"):
            try:
                resultado = div(uno, tres)
            except ZeroDivisionError:
                print("No se puede dividri entre 0")
            print(str(uno) + "/" + str(tres) + "=" + str(resultado))


        if (dos == "*"):
            resultado = multi(uno, tres)
            print(str(uno) + "*" + str(tres) + "=" + str(resultado))
        
    except ValueError:
        print("Error")    
    except SyntaxError:
        print("Error de sintaxis!!")

#Cerramos el fichero
f.close()

