import urllib.request
import threading
import socket
import json

import players
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
        #_thread.start_new_thread(self.start_receiving, ())
        receiving_thread = threading.Thread(target=self.start_receiving())
        receiving_thread.start()
        receiving_thread.join()

    def __del__(self):
        self.close()
        utils.log("Closed connection to client "+self.get_key())

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

        sent = 0
        try:
            sent = self.channel.send(json_data.encode('utf-8'))
        except socket.error:
            utils.log_err("Failed to send data!")

        if sent == 0:
            utils.log_wrn("Unable to send data to client; server connection to '"+self.get_key()+"' broken! Auto-cleaning connection...")
            self.close()
        else:
            utils.log("Sent data '"+json_data+"' to '"+self.get_key()+"'")

    def start_receiving(self):
        try:
            while True:
                data = self.channel.recv(Client.RECEIVE_MSG_BUFFER_SIZE).decode('utf-8')
                try:
                    json_data = json.loads(data)
                    utils.log("Got object from client '"+self.get_key()+"':\n"+data)

                    if isinstance(json_data, players.PlayerConnectionPackage):
                        self.player = players.Player(json_data)
                    elif isinstance(json_data, players.PlayerInputPackage):
                        pass
                    else:
                        utils.log_wrn("Could not interpret client package!")
                except ValueError:
                    utils.log("Got message from client '"+self.get_key()+"':\n"+data)
        except socket.error:
            utils.log_err("Message receiver thread stopped for client '"+self.get_key()+"'!")
            self.close()



class Server:

    RECEIVE_MSG_BUFFER_SIZE = 2048

    server = ["10.10.11.130",12345]

    open = True
    console = True
    connection_list = {}
    connection_socket = None

    def __init__(self, address=server[0], port=server[1]):
        self.server[0] = address
        self.server[1] = port

    def start(self):
        address = self.server[0]
        port = self.server[1]

        utils.log("Starting server at "+address+":"+str(port)+"...")
        self.server = [ address, port ]
        #_thread.start_new_thread(self.start_receiving, ())
        #_thread.start_new_thread(self.console_thread, ())
        receiving_thread = threading.Thread(target=self.start_receiving)
        console_thread = threading.Thread(target=self.start_console)
        receiving_thread.start()
        console_thread.start()
        utils.log("Started...")
        console_thread.join()

    def close(self):
        utils.log("Closing server and cleaning open connections...")
        for key in self.connection_list: self.connection_list[key].close()
        self.open = False
        self.console = False
        utils.log("Done - Server closed!")

    def start_receiving(self):
        utils.log("Starting server message receiver thread...")
        try:
            self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection_socket.bind(tuple(self.server))
            self.connection_socket.listen(5)
            utils.log("Ready for new incoming connections!")
            while self.open:
                c, addr = self.connection_socket.accept()
                conn_key = ":".join(str(i) for i in addr)
                utils.log("Receiving connection from "+conn_key+"...")
                self.connection_list[conn_key] = ServerConnection(addr, c, None, self)
                utils.log("Connection to "+conn_key+" open!")
        except socket.error:
            utils.log_err("Server message receiver thread stopped!")

    def start_console(self):
        utils.log("Starting console...")
        while self.console:
            try:
                user_entry = input("server >>")
                utils.log("Server Console: "+user_entry)
                exec(user_entry)
            except:
                utils.log_err("Error in console; ")

    @staticmethod
    def get_ip():
        return urllib.request.urlopen("https://api.ipify.org").read().decode('utf-8')



class Client:

    RECEIVE_MSG_BUFFER_SIZE = 2048

    server = ["10.10.11.130",12345]
    socket_to_server = None

    listen = True

    def __init__(self, address=server[0], port=server[1]):
        self.server[0] = address
        self.server[1] = port

    def start(self):
        address = self.server[0]
        port = self.server[1]

        utils.log("Attempting to connect to server at "+address+":"+str(port)+"...")
        self.server = [address, port]
        self.socket_to_server = socket.socket()
        self.socket_to_server.connect(tuple(self.server))
        utils.log("Connected to server at "+address+":"+str(port)+"!")

        receiving_thread = threading.Thread(target = self.start_receiving)
        receiving_thread.start()
        receiving_thread.join() # wait for listener thread to end

        utils.log("Closing connection to server...")
        self.socket_to_server.close()

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

        sent = 0
        try:
            sent = self.socket_to_server.send(json_data.encode('utf-8'))
        except socket.error:
            utils.log_err("Failed to send data!")

        if sent == 0:
            utils.log_wrn("Unable to send data to server; client connection to '"+self.get_key()+"' broken! Auto-cleaning connection...")
            self.socket_to_server.close()
        else:
            utils.log("Sent data '"+json_data+"' to '"+self.get_key()+"'")

    def start_receiving(self):
        try:
            plr_name = input("Enter your player name (ex. 'Paul'); ")
            plr_color = [int(x) for x in input("Enter your player's color (ex. '255 255 0'); ").split()]

            plr_conn_pkg = players.PlayerConnectionPackage(plr_name, plr_color)
            self.send(plr_conn_pkg)

            while self.listen:
                data = self.socket_to_server.recv(Client.RECEIVE_MSG_BUFFER_SIZE).decode('utf-8')
                try:
                    json_data = json.loads(data)
                    utils.log("Got object from server '"+self.get_key()+"':\n"+data)
                except ValueError:
                    utils.log("Got message from server '"+self.get_key()+"':\n"+data)
        except socket.error:
            utils.log_err("Client message receiver thread stopped!")


