import socket
import threading
import sys
import time
import pickle

local = '127.0.0.1', 50001
con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
con.bind(local)
dest = '127.0.0.1', 50000


class tcp_header:
    sequence_number = None
    acknowledgement_number = None
    syn = False
    ack = False
    fin = False
    rst = False
    file = None

    def __init__(self, syn, sequence_number, file, fin):
        self.syn = syn
        self.sequence_number = sequence_number
        self.file = file
        self.fin = fin


class table():
    buffer_list = []
    tcpHeader = tcp_header


count = 100


def End_connection():
    print("enviando confirmção...")
    connection_object = tcp_header(False, None, None, True)
    data_byte = pickle.dumps(connection_object)
    con.sendto(data_byte, server)


def Wait_confirmation():
    global count
    print("Esperando confirmação...")
    data, server = con.recvfrom(2048)
    table.tcpHeader = pickle.loads(data)
    while table.tcpHeader.acknowledgement_number != count - 99:
        print("Retransmitindo dado...")
        time.sleep(2)
        connection_object = tcp_header(False, count - 100, table.buffer_list[-1], False)
        data_byte = pickle.dumps(connection_object)
        con.sendto(data_byte, server)
        print("Esperando confirmação...")
        data, server = con.recvfrom(2048)
        table.tcpHeader = tcpHeader
        table.tcpHeader = pickle.loads(data)


def Send_file(buffer):
    global count
    connection_object = tcp_header(False, count, buffer, False)
    table.buffer_list.append(connection_object)
    data_byte = pickle.dumps(connection_object)
    con.sendto(data_byte, server)
    count = count + 100
    print("Enviando arquivo...")
    buffer = None
    time.sleep(0.3)
    Wait_confirmation()
    return buffer


def Split_file():
    buffer_size = 64000
    f = open("enviar.txt", "rb")
    buffer = f.read(buffer_size)
    while buffer:
        Send_file(buffer)
        buffer = f.read(buffer_size)
    End_connection()


try:
    con.settimeout(5)
    connection_object = tcp_header(True, None, None, False)
    data_string = pickle.dumps(connection_object)
    print("Iniciando conexão")
    con.sendto(data_string, dest)
    print("Esperando confirmação de conexão")
    data, server = con.recvfrom(2048)
    tcpHeader = pickle.loads(data)
    if tcpHeader.syn and tcpHeader.ack:
        Split_file()
except socket.timeout:
    print("TIMEOUT, encerrando conexão...")
