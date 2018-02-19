import urllib.request
import _thread
import socket
import json

import utils




class ServerConnection:

    address = None
    channel = None
    player = None
    parent = None

    def __init__(self, address, conn, player, parent):
        self.address = address
        self.channel = conn
        self.player = player
        self.parent = parent
        _thread.start_new_thread(self.start_receiving, ())

    def __del__(self):
        self.close()
        utils.log("Closed connection to client "+self.get_key())

    def set_player_data(self, player):
        self.player = player

    def get_key(self):
        return ":".join(str(i) for i in self.address)

    def close(self):
        if self.channel is not None: self.channel.close()
        if self.parent is not None and self.get_key() in self.parent.connection_list: del self.parent.connection_list[self.get_key()]

    def send(self, data):
        if isinstance(data, str):
            json_data = data
        else:
            json_data = json.dumps(data, indent=4, separators=(',', ': '))
        sent = self.channel.send(json_data.encode('utf-8'))
        if sent == 0:
            utils.log_err("Unable to send data to client; server connection to '"+self.get_key()+"' broken! Auto-cleaning connection...")
            self.close()
        else:
            utils.log("Sent data '"+json_data+"' to '"+self.get_key()+"'")

    def start_receiving(self):
        while True:
            data = self.channel.recv(Client.RECEIVE_MSG_BUFFER_SIZE).decode('utf-8')
            try:
                json_data = json.loads(data)
                utils.log("Got object from client '"+self.get_key()+"':\n"+data)
            except ValueError:
                utils.log("Got message from client '"+self.get_key()+"':\n"+data)




class Server:

    RECEIVE_MSG_BUFFER_SIZE = 2048

    server = ["localhost",12345]
    connection_list = {}

    def __init__(self):
        _thread.start_new_thread(self.start_receiving, ())

        while True:
            msg = input("Message: ")
            if msg == "exit": break
            for key in self.connection_list:
                self.connection_list[key].send(msg)

    def start_receiving(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(tuple(self.server))
        s.listen(5)
        while True:
            c, addr = s.accept()
            conn_key = ":".join(str(i) for i in addr)
            utils.log("Receiving connection from "+conn_key+"...")
            self.connection_list[conn_key] = ServerConnection(addr, c, None, self)
            utils.log("Connection to "+conn_key+" open!")

    @staticmethod
    def get_ip():
        return urllib.request.urlopen("https://api.ipify.org").read().decode('utf-8')



class Client:

    RECEIVE_MSG_BUFFER_SIZE = 2048

    server = ["localhost",12345]
    socket_to_server = None

    def __init__(self):
        self.socket_to_server = socket.socket()
        self.socket_to_server.connect(tuple(self.server))
        _thread.start_new_thread(self.start_receiving, ())

        while True:
            msg = input("Message: ")
            if msg == "exit": break
            self.send(msg)

    def __del__(self):
        self.close()
        utils.log("Closed connection to server "+self.get_key())

    def get_key(self):
        return ":".join(str(i) for i in self.server)

    def close(self):
        if self.socket_to_server is not None:
            self.socket_to_server.close()
            self.socket_to_server = None

    def send(self, data):
        if isinstance(data, str):
            json_data = data
        else:
            json_data = json.dumps(data, indent=4, separators=(',', ': '))
        sent = self.socket_to_server.send(json_data.encode('utf-8'))
        if sent == 0:
            utils.log_err("Unable to send data to server; client connection to '"+self.get_key()+"' broken! Auto-cleaning connection...")
            self.socket_to_server.close()
        else:
            utils.log("Sent data '"+json_data+"' to '"+self.get_key()+"'")

    def start_receiving(self):
        while True:
            data = self.socket_to_server.recv(Client.RECEIVE_MSG_BUFFER_SIZE).decode('utf-8')
            try:
                json_data = json.loads(data)
                utils.log("Got object from server '"+self.get_key()+"':\n"+data)
            except ValueError:
                utils.log("Got message from server '"+self.get_key()+"':\n"+data)



