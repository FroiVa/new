import string
import random
import socket

# Obtener cantidad de caracteres aleatorios entre 50 y 100
def cant_caracteres(cant_espacios):
    return random.randint(50 - cant_espacios, 100 - cant_espacios)

# Obtener cantidad de espacios aleatorios entre 3 y 5
def cant_espacios_blanco():
    return random.randint(3, 5)

# Obtener lista con los indíces aleatorios de los espacios en blanco
def index_list(cant_espacios, string_len):
    lista = random.sample(range(1, string_len-1), cant_espacios)
    lista.sort()
    for i in range(0, len(lista) - 1):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                lista[j] += 2
            if lista[i] + 1 == lista[j]:
                lista[j] = lista[j] + 1
                lista.sort()
    return lista

# Generar cadena
def generar_cadena():
    str = ""
    cant_whitespace = cant_espacios_blanco()
    cantidad_char = cant_caracteres(cant_whitespace)
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    cadena = random.choices(letters, k=cantidad_char)
    lista = index_list(cant_whitespace, len(cadena))

    a = list(cadena)

    for i in lista:
        a.insert(i, " ")

    str += "".join(a)
    return str

# Generar fichero dada una cantidad de cadenas
def generar_fichero(cantidad_cadenas):
    f = open("chain.txt", "w")
    for _ in range(cantidad_cadenas):
        str = generar_cadena()
        f.write(str + "\n")
    f.close()

# Envíar las cadenas generadas al servidor y obtener su métrica
def enviar_servidor():
    HOST = "127.0.0.1"
    PORT = 65123
    SIZE = 100


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(240)
    s.connect((HOST, PORT))

    f = open("chain.txt", "r")
    data_txt = f.readlines()
    # Eliminar "\n"
    data_txt = [i.rstrip() for i in data_txt]

    respuesta = []
    # Enviar cadenas al servidor
    for i in data_txt:
        data_len = len(i.encode("utf-8"))
        # Asegurar que las cadenas sean de tamaño igual a SIZE
        if data_len != SIZE:
            for _ in range(SIZE - data_len):
                i +=" "
        s.send(i.encode("utf-8"))
    c = 0
    # Reciviendo respuesta del servidor
    for i in range(len(data_txt)):
        a = s.recv(200).decode("utf-8")
        c += 1
        respuesta.append(f"{c}: {a.strip()}")

    return respuesta

def main():
    opcion = input(""" Selecciona una opción del menú.

    1. Generar fichero de cadenas
    2. Obtener métrica de cadenas
    3. Salir
    """)

    if opcion == "1":
        cant = input("Indique la cantidad de cadenas que desea generar: ")
        if not cant:
            cant = 1000000
        generar_fichero(int(cant))
        print("Fichero generado con éxito.")

    elif opcion == "2":
        lista_metrica = enviar_servidor()
        for i in lista_metrica:
            print(i)
    elif opcion == "3":
        exit()

    print("\n")
    main()

if __name__ == "__main__":
    main()

