# IMPORTANTE:
# para debuggear y ver a detalle el programa
# descomentar las siguientes lineas
# 46, 47, 57, 60, 63, 71, 74, 79,
# 216, 227, 228, 237, 238, 276, 277, 285, 286, 303, 304 

def main():
    print(
        '''
         __  __      _            _             _
        |  \/  | ___| |_ ___   __| | ___     __| | ___
        | |\/| |/ _ \ __/ _ \ / _` |/ _ \   / _` |/ _ |
        | |  | |  __/ || (_) | (_| | (_) | | (_| |  __/
        |_|  |_|\___|\__\___/ \__,_|\___/   \__,_|\___|
                   _       _           _               _                   _
         _ __ ___ (_)_ __ (_)_ __ ___ (_)______ _  ___(_) ___  _ __     __| | ___
        | '_ ` _ \| | '_ \| | '_ ` _ \| |_  / _` |/ __| |/ _ \| '_ \   / _` |/ _ |
        | | | | | | | | | | | | | | | | |/ / (_| | (__| | (_) | | | | | (_| |  __/
        |_| |_| |_|_|_| |_|_|_| |_| |_|_/___\__,_|\___|_|\___/|_| |_|  \__,_|\___|
         __  __       ____ _           _
        |  \/  | ___ / ___| |_   _ ___| | _____ _   _
        | |\/| |/ __| |   | | | | / __| |/ / _ \ | | |
        | |  | | (__| |___| | |_| \__ \   <  __/ |_| |
        |_|  |_|\___|\____|_|\__,_|___/_|\_\___|\__, |
                                                |___/

                            Casos de ejemplo

        Ingrese esta cantidad de bits:

                    8               |                   4

        Ingrese los minterminos de la siguiente manera:

        15, 16, 17, 8, 10, 20       |       1, 4, 6, 7, 8, 9, 10, 11, 15

        ''',
        end='\n'
    )

    n_bits = 0
    while 9 > n_bits < 1:
        n_bits = int(input("Ingrese el numero de bits que requiere (Maximo 8): "))

    minterminos = input("Ingrese los minterminos: ")
    # print(f" -> Datos ingresados por el usarios \n\n\tNumero de bits: {n_bits}\n\n \t{minterminos}\n\n")

    minterminos = normalizar_datos(minterminos)
    print(f" -> Datos normalizados \n\n\t{minterminos}\n\n")

    # El numero que se pasa como segundo parametro hace referencia a cadenas de 
    # cuantos bits se van a tomar, el sistema funciona para cadenas hasta de 8 bits 
    # tener en cuenta entonces el numero maximo ingresado y sobre su representacion binaria
    # trabajar este numero

    minterminos_binario = representacion_binaria(minterminos, 8)
    print(f" -> Representacion binaria \n\n\t{minterminos_binario}\n\n")

    datos_agrupados = agrupar(minterminos_binario)
    print(f" -> Datos agrupados \n\n\t{datos_agrupados}\n\n")

    combinaciones = combinar(datos_agrupados)
    print(f" -> Datos combinados \n\n\t{combinaciones}\n\n")

    # Esto es el caso de que no exista primeras combinaciones
    # no se que se hacer en dicho caso , asumo que no se podra reducir el sistema
    if combinaciones == []:
        print("Este sistema no se puede minimizar")
    else:
        implicantes = segunda_agrupacion(combinaciones)
        print(f" -> Combinados \n\n\t{implicantes}\n\n")

        marcados = primeros_implicantes(combinaciones,implicantes)
        print(f" -> Implicantes \n\n\t{marcados}\n\n")

        # Se hace porque marcados esta funcionando como puntero
        limpiar_implicantes(implicantes,marcados)

        # print(f" -> Implicantes filtrados {marcados}")

        # Se modifica la estructura de los implicantes para poder agregarla a los marcados
        aux = None
        for implicante in range(0, len(implicantes)):
            aux = [((implicantes[implicante][0][0] + implicantes[implicante][0][1]), implicantes[implicante][1])]

        # Se reasigna el vector de marcados para la verificacion
        marcados = marcados + aux

        marcados = tabla_de_validacion(marcados, minterminos)

        expresion=""
        for elemento in range(0, len(marcados)):
            e = generar_expresion(marcados[elemento][1])
            if elemento < len(marcados) - 1:
                expresion = expresion + e +" + "
            else:
                expresion = expresion + e

        print('\t Expresion final: ', end="")
        print('\t ---> ', expresion)

# Determina cuantos elementos hay diferentes en cada string
def distancia_hamming(dato1, dato2):
    distancia = 0
    i = 0
    combinacion = ""
    for elemento in dato1:
        if elemento != dato2[i]:
            distancia = distancia + 1
            combinacion = combinacion+"-"
        else:
            combinacion = combinacion+elemento
        i = i + 1
    return (distancia,combinacion)

def combinar(datos_agrupados):
    i = 0
    salida = [[],[],[],[],[],[],[],[],[]]
    # Recorre la lista de grupos, excepto el ultimo pues no tiene con quien combinarse
    while i < (len(datos_agrupados) - 1):
        # Toma cada elemento de cada grupo (grupo al que estoy evaluando)
        for elemento_inicial in datos_agrupados[i]:
            # Para cada elemento al grupo a evaluar
            # toma cada elemento del grupo siguiente al que se esta evaluando
            for elemento_siguiente in datos_agrupados[i+1]:
                distancia,combinacion = distancia_hamming(elemento_inicial[0],elemento_siguiente[0])
                if distancia == 1:
                    dato = ((elemento_inicial[1],elemento_siguiente[1]),combinacion)
                    salida[i].append(dato)
        i = i + 1
    return salida

def primeros_implicantes(datos_agrupados,implicantes):
    aux = aplanar(datos_agrupados)
    for dato in aux:
        for implicante in implicantes:
            comb = combinaciones_implicantes(implicante[0])
            if dato[0] in implicante[0] or dato[0] in comb:
                try:
                    aux.remove(dato)
                except:
                    pass
    return aux

def combinaciones_implicantes(datos):
    i = 0
    salida = []
    while i < (len(datos) - 1):
        for elemento in datos[i]:
            for elemento2 in datos[i+1]:
                aux = (elemento,elemento2)
                salida.append(aux)
        i = i + 1
    return list(set(salida))

# Se usa para que todas las cadenas de bits tengan 8bits
def normalizar_cadena_bits(cadena_bits,n_bits):
    salida = None
    if len(cadena_bits) < n_bits:
        sumar = n_bits-len(cadena_bits)
        salida = ("0"*sumar)+cadena_bits
    elif len(cadena_bits) == n_bits:
        salida = cadena_bits
    return salida

def representacion_binaria(minterminos,n_bits):
    salida = {}
    for mintermino in minterminos:
        # Se toma desde la pos 2 , porque el formato original es "0b001"
        # por tanto tomandolo desde el 2 se tiene solo la cadena de bits
        aux = bin(mintermino)[2:]
        aux = normalizar_cadena_bits(aux,n_bits)
        salida[str(mintermino)] = aux
    return salida

def segunda_agrupacion(minterminos):
    i = 0
    salida = []
    while i < (len(minterminos)-1):
        for implicante in minterminos[i]:
            for implicante_2 in minterminos[i + 1]:
                distancia,combinacion = distancia_hamming(implicante[1],implicante_2[1])
                if distancia == 1:
                    dato = ((implicante[0],implicante_2[0]),combinacion)
                    minterminos[i].remove(implicante)
                    salida.append(dato)
        i = i + 1
    return salida

def aplanar(vector):
    salida = []
    for elemento in vector:
        for a in elemento:
            salida.append(a)
    return salida

def agrupar(minterminos):
    # La salida comprende un array que agrupa segun la cantidad
    # de 1 que tenga la respectiva conversion a binario de los
    # numero ordenado, de modo que sería: 0, 1, 2, ... 7 valores
    # iguales a 1
    salida = [[],[],[],[],[],[],[],[],[]]
    for key in minterminos.keys():
        identificador_grupo = minterminos[key].count("1")
        dato = (minterminos[key],key)
        salida[identificador_grupo].append(dato)
    return salida

def limpiar_implicantes(implicantes,datos):
    for dato in datos:
        for implicante in implicantes:
            comb = combinaciones_implicantes(implicante[0])
            if dato[0] in comb or dato[0] in implicante[0]:
                try:
                    datos.remove(dato)
                except:
                    pass

def tabla_de_validacion(marcados, numeros):
    # tabla_ejemplo(marcados, numeros)

    # Generacion de la matriz de validacion
    validacion=[]
    for i in range(0, len(marcados)):
        validacion.append([])
        for j in numeros:
            validacion[i].append(j)

    # print("Representacion de la tabla de numeros", end='\n')
    # representacion_de_expresiones(validacion)

    # Generaciones de X
    for i in range(0, len(validacion)):
        for j in range(0, len(validacion[0])):
            for nueva_x in marcados[i][0]:
                if str(validacion[i][j]) == nueva_x:
                    validacion[i][j] = 'X'

    # print("Representacion de la tabla de expresiones marcadas", end='\n')
    # representacion_de_expresiones(validacion)

    print("-> Simplificacion y validacion de expresiones", end='\n\n')
    expresion_validada = validacion_y_simplificacion(marcados, validacion)
    return expresion_validada

def tabla_ejemplo(marcados, numeros):
    print("________________________")
    print("\tExpresiones\t", end='  ')
    [print(numero, end=' ') for numero in numeros]
    print("\n------------------------")
    [print(marcado, end='\n') for marcado in marcados]
    print()

def representacion_de_expresiones(validacion):
    # Matriz de representacion de expresiones
    for i in range(0, len(validacion)):
        for j in range(0, len(validacion[1])):
            print(validacion[i][j], end='\t')
        print()
    print()

# Se elimina de la tabla de marcados lo que no cumplen la validacion
def validacion_y_simplificacion(marcados, validacion):
    # Nos da la lista de expresiones ya validada con la que se limpia el puntero de los marcados
    lista_de_expresiones = []

    for i in range(0, len(validacion[1])):
        nueva_expresion = []
        agregar_expresion = 0
        for j in range(0, len(validacion)):
            if validacion[j][i] == 'X':
                agregar_expresion += 1
                nueva_expresion = [j, i]
        if agregar_expresion == 1:
            validacion[nueva_expresion[0]][nueva_expresion[1]] = 'O'
            lista_de_expresiones.append(nueva_expresion)

    # print(lista_de_expresiones)
    # representacion_de_expresiones(validacion)

    for i in range(0, len(validacion)):
        for j in range(0, len(validacion[1])):
            if validacion[i][j] == 'O' and validacion[i][1+j] == 'X' and validacion[i][j-1] == 'X':
                validacion[i][j] = 'X'
                lista_de_expresiones.pop(lista_de_expresiones.index([i, j]))

    # print(lista_de_expresiones)
    # representacion_de_expresiones(validacion)

    for i in range(0, len(validacion[1])):
        nueva_expresion = []
        codo_encontrado = 0
        for j in range(0, len(validacion)):
            if validacion[j][i] == 'X':
                codo_encontrado += 1
                try:
                    if codo_encontrado == 2 and validacion[j][i+1] == 'X':
                        validacion[j][i+1] = 'C'
                        validacion[j][i] = 'L'
                except:
                     if codo_encontrado == 2 and validacion[j][i-1] == 'X':
                        validacion[j][i-1] = 'C'
                        validacion[j][i] = 'L'

    # print(lista_de_expresiones)
    # representacion_de_expresiones(validacion)
    for i in range(0, len(validacion)):
        nueva_x_de_simplificacion = True
        for j in range(0, len(validacion[1])):
            if validacion[i][j] == 'O' or validacion[i][1] == 'L' or validacion[i][j] == 'C':
                nueva_x_de_simplificacion = False
            if validacion[i][j] == 'X' and nueva_x_de_simplificacion == True:
                lista_de_expresiones.append([i, j])
                nueva_x_de_simplificacion = False

    expresion_validada = [marcados[resultado[0]] for resultado in lista_de_expresiones]
    print('\t', expresion_validada, end='\n\n')

    return expresion_validada

def generar_expresion(cadena_bits):
    salida=""
    i = 0
    for bit in cadena_bits:
        if bit != "-":
            aux = determinar_negacion(bit)
            if aux:
                salida = salida+"~"
            salida = salida+deteminar_letra(i)
        i = i + 1
    return salida

def determinar_negacion(bit):
    if bit == "0":
        return True
    else:
        return False

def deteminar_letra(pos):
    salida = None
    if pos == 0:
        salida = "A"
    elif pos == 1:
        salida = "B"
    elif pos == 2:
        salida = "C"
    elif pos == 3:
        salida = "D"
    elif pos == 4:
        salida = "E"
    elif pos == 5:
        salida = "F"
    elif pos == 6:
        salida = "G"
    elif pos == 7:
        salida = "H"
    return salida


def normalizar_datos(minterminos):
    aux = minterminos.strip()
    aux = aux.split(",")
    # Valida que no se ingresen caracteres raros o no numericos
    try:
        # Genera la lista de enteros menores a 256 ingresados por el usuario
        # el 256 es por el numero maximo representado con 8 bits
        salida = [int(dato) for dato in aux if int(dato) < 256]
        salida = sorted(set(salida))
        return salida
    except:
        print("A ingresado un dato no valido... \n\nReiniciando el programa.")
        main()

main()
