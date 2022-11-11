import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
print(IP)
PORT = 8080
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def abrir_archivo(conn, addr):
    print("Aabrir archivo")
    file = conn.makefile()
    print(f'Conexión de {addr}')

    try:
        while True:
            line = file.readline()
            print(line)
            if line:
                with open('archivo.html', 'r') as f:
                    page_data= f.read()
                    print(page_data)
                    f.close()
                    conn.send(b"HTTP/1.0 200 OK\r\n")
                    conn.send(b'Content-Type: text/html\n')
                    conn.send(b'\n')
                    conn.send(page_data.encode())
                    return
    except IOError:
        conn.send("404 Not Found")
    finally:
        print(f'{addr} saliendo....')
        file.close()
        conn.close()

def main():
    print("[Iniciando] El servidor esta iniciado...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(ADDR)
    server.listen()

    while True:
        conn, addr = server.accept()
        print("Cliente conectados")
        thread = threading.Thread(target=abrir_archivo, args=(conn, addr))
        thread.start()




if __name__ == "__main__":
    main()


