def main():
    print('''hola bienvenido al algoritmo de reduccion de McCluskey")
    para que funcione debe ingresar los minterminos de la siguiente manera
    ej: 15,16,17,8,10,20''')
    minterminos = input("ingrese los minterminos: ")
    minterminos = normalizar_datos(minterminos)
    minterminos_binario = representacion_binaria(minterminos)
    datos_agrupados = agrupar(minterminos_binario)
    combinaciones = combinar(datos_agrupados)
    #esto es el caso de que no exista primeras combinaciones
    #no se que se hacer en dicho caso , asumo que no se podra reducir el sistema
    if combinaciones == []:
        print("este sistema no se puede minimizar")
    else:
        print(combinaciones)
        #primeros_implicantes(combinaciones)

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
    salida = []
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
                    salida.append(dato)
        i = i + 1 
    return salida

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
    
def agrupar(minterminos):
    clave_base = "grupo"
    salida = {}
    for key in minterminos.keys():
        identificador_grupo = minterminos[key].count("1")
        clave = clave_base+str(identificador_grupo)
        #valida si el grupo ya existe
        if clave in salida.keys():
            dato = (minterminos[key],key)
            salida[clave].append(dato)
        else:
            salida[clave] = []
            dato = (minterminos[key],key)
            salida[clave].append(dato)
    #se hace esto porque la estructura original de los grupos 
    #era un diccionario con claves segun el nombre del grupo
    #esto lo volvia muy complicado de recorrer al momento de combinar
    #por ese se opto por convertirlo en una lista que contiene los grupos
    #algo similar a esto 
    #[[(1,'00000001'),(2,'00000001')],[(9,'00001001'),(10,'00001010')]]
    salida = aplanar_grupos(salida)
    return salida

#se usa para recorrer de manera mas sencilla el arreglo de grupos
def aplanar_grupos(minterminos):
    salida = []
    for key in minterminos.keys():
        salida.append(minterminos[key])
    return salida

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

