import sys
import socket
import json
import time


def server(ip_add, port):
    """

    :param ip_add: the ip to connect to.
    :param port: "" port "".
    :return: None.
    """
    password = 'ff4F3sGPpgs12S'
    admin = 'some_user'
    ''' The output server messages in JSON format '''
    con_success = json.dumps({"result": "Connection success!"}, indent=4)
    con_exception = json.dumps({"result": "Exception happened during login"}, indent=4)
    con_wrong_pass = json.dumps({"result": "Wrong password!"}, indent=4)
    con_wrong_login = json.dumps({"result": "Wrong login!"}, indent=4)

    with socket.socket() as server_socket:
        server_socket.bind((ip_add, int(port)))
        server_socket.listen()
        conn, addr = server_socket.accept()
        print('Connected by', addr)
        while True:
            while True:
                data = conn.recv(1024)
                if len(data) <= 0: break
                re = json.loads(data.decode())

                if re["login"] == admin:
                    if re["password"] == password:
                        conn.sendall(con_success.encode())
                        break

                    if re["password"] in password:
                        ''' Put a sleeper to mimic a bug in the server that ables to crack the password '''
                        time.sleep(0.01)
                        conn.sendall(con_wrong_pass.encode())
                    else:
                        conn.sendall(''.join(con_wrong_pass).encode())
                else:
                    conn.sendall(''.join(con_wrong_login).encode())


server(sys.argv[1], sys.argv[2])
