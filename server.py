import pickle
import socket
import logging
import time

def fichero_log(cadena, metrica):
    logging.basicConfig(filename="logfile.log", level=logging.INFO,
                        format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    if metrica == 1000:
        logging.info(f"Double ‘a’ rule detected >> '{cadena}'")
    elif "tiempo" in cadena:
        logging.info(f"{cadena} >> '{metrica}'")
    else:
        logging.info(f"La métrica para la cadena '{cadena}' es >> {metrica}")

def cant_numeros(cadena):
    c = 0
    for i in cadena:
        if i.isnumeric():
            c += 1
    return c

def cant_espacios(cadena):
    return float(cadena.count(" "))

def cant_caracteres(cadena):
    return float(len(cadena) - cant_numeros(cadena) - cant_espacios(cadena))

def metrica(cadena):
    tmp_cadena = cadena.lower()
    if "aa" in tmp_cadena:
        return 1000
    a = cant_caracteres(cadena)
    b = cant_numeros(cadena)
    c = cant_espacios(cadena)

    if c != 0:
        return ( a * 1.5 +  b * 2) / c

    return 0


def receive():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', 65123))
        SIZE = 100
        sock.listen()
        conn, addr = sock.accept()
        print(f"Connected by: {addr}")
        start = time.perf_counter()
        data_list = []

        with conn:
            while True:
                # Recibo los datos del cliente
                a = conn.recv(SIZE).decode("utf-8")
                if not a:
                    break
                # Cálculo de la métrica y añadir evento en logs
                metric = metrica(a.strip())
                fichero_log(a.strip(), metric)
                msg = ""
                if metric == 1000:
                    msg = f"Double ‘a’ rule detected >> '{a.strip()}'. Métrica >> 1000"
                else:
                    msg = f"La métrica para la cadena '{a.strip()}' es >> '{metric}'"
                RES_SIZE = len(msg.encode('utf-8'))

                data_list.append(a)
                if RES_SIZE != 200:
                    for _ in range(200 - RES_SIZE):
                        msg += " "
                conn.sendall(msg.encode("utf-8"))


    end = time.perf_counter()
    msg = "El tiempo de procesamiento es: "
    fichero_log(msg, end - start)

    for i in data_list:
        print(i)
    print(end - start)
    print("Procesamiento terminado")
    receive()

if __name__ == "__main__":
    receive()


