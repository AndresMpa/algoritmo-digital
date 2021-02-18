def main():
    print('''hola bienvenido al algoritmo de reduccion de McCluskey")
    para que funcione debe ingresar los minterminos de la siguiente manera
    ej: 15,16,17,8,10,20''')
    minterminos = input("ingrese los minterminos: ")
    #print(f"datos ingresados por el usarios \n\n{minterminos}\n\n")
    minterminos = normalizar_datos(minterminos)
    #print(f"datos normalizados \n\n{minterminos}\n\n")
    minterminos_binario = representacion_binaria(minterminos)
    #print(f"representacion binaria \n\n{minterminos_binario}\n\n")
    datos_agrupados = agrupar(minterminos_binario)
    #print(f"datos agrupados \n\n{datos_agrupados}\n\n")
    combinaciones = combinar(datos_agrupados)
    #print(f"datos combinados \n\n{combinaciones}\n\n")
    #esto es el caso de que no exista primeras combinaciones
    #no se que se hacer en dicho caso , asumo que no se podra reducir el sistema
    if combinaciones == []:
        print("este sistema no se puede minimizar")
    else:
        implicantes = segunda_agrupacion(combinaciones)
        print(f"combinados {implicantes}\n\n")
        marcados = primeros_implicantes(combinaciones,implicantes)
        #print(f"implicantes {marcados}\n\n")
        limpiar_implicantes(implicantes,marcados)
        print(f"implicantes filtrados {marcados}")
        #nota esto se hace como caso particular para ver un error ignorar esta linea esta WIP
        

#determina cuantos elementos hay diferentes en cada string
def distancia_hamming(dato1,dato2):
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
    #recorre la lista de grupos, excepto el ultimo pues no tiene con quien combinarse
    while i < (len(datos_agrupados) - 1):
        #toma cada elemento de cada grupo (grupo al que estoy evaluando)
        for elemento_inicial in datos_agrupados[i]:
            #para cada elemento al grupo a evaluar
            #toma cada elemento del grupo siguiente al que se esta evaluando
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
            if dato[0] in implicante[0] or  dato[0] in comb:
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

#se usa para que todas las cadenas de bits tengan 8bits
def normalizar_cadena_bits(cadena_bits):
    salida=None
    if len(cadena_bits) < 8:
        sumar = 8-len(cadena_bits)
        salida = ("0"*sumar)+cadena_bits
    elif len(cadena_bits) == 8:
        salida = cadena_bits
    return salida
        
def representacion_binaria(minterminos):
    salida = {}
    for mintermino in minterminos:
        #se toma desde la pos 2 , porque el formato original es "0b001"
        #por tanto tomandolo desde el 2 se tiene solo la cadena de bits
        aux = bin(mintermino)[2:]
        aux = normalizar_cadena_bits(aux)
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
                datos.remove(dato)

def normalizar_datos(minterminos):
    aux = minterminos.strip()
    aux = aux.split(",")
    #valida que no se ingresen caracteres raros o no numericos
    try:
        #genera la lista de enteros menores a 256 ingresados por el usuario
        #el 256 es por el numero maximo representado con 8 bits
        salida = [int(dato) for dato in aux if int(dato) < 256]
        salida = sorted(set(salida))
        return salida
    except:
        print("a ingresado un dato no valido, reiniciando el programa")
        main()
main()