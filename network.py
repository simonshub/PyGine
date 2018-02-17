import socket

import utils



class Server:

    def __init__(self):

        s = socket.socket()
        host = socket.gethostname()
        port = 12345
        s.bind((host,port))

        s.listen(5)
        while True:
            c, addr = s.accept()
            utils.log("Recieving connection from "+addr+"...")
            c.send("hello")
            c.close()



class Client:

    def __init__(self):
        s = socket.socket()
        host = socket.gethostname()
        port = 12345

        s.connect((host,port))
        utils.log("Recieved message; '"+s.recv(1024)+"' from "+host+":"+port)
        s.close()
