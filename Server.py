import socket
import time
import pickle

server_ip = '127.0.0.1'
server_port = 50000
client = None
connection_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_address = (server_ip, server_port)
connection_socket.bind(my_address)


def Recv_con():
    while True:
            connection_socket.settimeout(None)
            print("Aguardando conexão")
            data, client = connection_socket.recvfrom(1024)
            tcpHeader = pickle.loads(data)
            Make_con(tcpHeader, client)

def Make_con(header, client):
    print("Validando conexão...")
    if header.syn == True:
        print('Conexão recebida, enviando confirmação...')
        time.sleep(1)
        connection_object = tcp_header(True, True)
        data_byte = pickle.dumps(connection_object)
        connection_socket.sendto(data_byte, client)
        Recv_files()


def Send_conf(tcpheader, client):
    print("Enviando confirmação de recebimento...")
    time.sleep(2)
    confirmation_object = tcpheader
    confirmation_object.file = None
    confirmation_object.acknowledgement_number = confirmation_object.sequence_number + 1
    data_byte = pickle.dumps(confirmation_object)
    connection_socket.sendto(data_byte, client)


def Recv_files():
    global client
    try:
        connection_socket.settimeout(5)
        tcpheader = tcp_header(False, False)
        while tcpheader.fin is False:
            print("Recebendo Arquivo...")
            data, client_ = connection_socket.recvfrom(664000)
            if client is None:
                client = client_
            tcpheader = pickle.loads(data)
            buffer = open("copia.txt", "ab")
            if tcpheader.file is not None and client == client_:
                buffer.write(tcpheader.file)
                Send_conf(tcpheader, client)
        buffer.close()
        client = None
        print("Arquivo recebido com sucesso!")
    except socket.timeout:
        print("TIMEOUT, encerrando conexão!")
        client = None
    except:
        print("Arquivo corrompido, encerrando conexão!")
        client = None


class tcp_header:
    sequence_number = None
    acknowledgement_number = None
    syn = False
    ack = False
    fin = False
    rst = False
    file = None

    def __init__(self, syn, ack):
        self.syn = syn
        self.ack = ack

Recv_con()