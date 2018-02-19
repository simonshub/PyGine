import socket
import urllib.request

import env



class Server:

    def __init__(self):
        s = socket.socket()
        #host = Server.get_ip()
        host = "localhost"
        port = 12345
        s.bind((host,port))

        s.listen(5)
        while True:
            c, addr = s.accept()
            print("Receiving connection from "+",".join(str(i) for i in addr)+"...")
            msg = ""
            with open(env.Environment.SETTINGS_FILE_PATH, 'r') as content_file:
                msg = content_file.read()
            c.send(msg.encode('utf-8'))
            c.close()

    @staticmethod
    def get_ip():
        return urllib.request.urlopen("https://api.ipify.org").read().decode('utf-8')



class Client:

    def __init__(self):
        s = socket.socket()
        host = "localhost"
        port = 12345

        s.connect((host,port))
        print("Received message; '"+s.recv(1024).decode('utf-8')+"' from "+host+":"+str(port))
        #utils.log("Received message; '"+s.recv(1024)+"' from "+host+":"+port)
        s.close()



