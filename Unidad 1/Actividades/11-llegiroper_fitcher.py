#Crea una aplicació que vaja llegint operacions d'un fitxer (una operació per líniia) o
#afegisca els resultats. Per exemple, si llig: 4+4

#Haurà de generar: 4+4 = 8

#Utilitzan funcions anònimes per a implementar les operacions


#Funciones Lambda

suma = lambda x,y: x + y
resta = lambda x,y: x - y
div = lambda x,y: x / y
multi = lambda x,y: x * y


#Ahora abriremos el fichero

f = open("operacions.txt", 'r')


#Iniciamos un bucle para recorrer todo el fichero
for linia in f:
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
        resultado = div(uno, tres)
        print(str(uno) + "/" + str(tres) + "=" + str(resultado))


    if (dos == "*"):
        resultado = multi(uno, tres)
        print(str(uno) + "*" + str(tres) + "=" + str(resultado))

#Cerramos el fichero
f.close()
