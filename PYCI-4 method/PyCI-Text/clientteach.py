import socket
import threading

class cli():
    def __init__(self):
        self.gd_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 網路通訊,tcp
        self.gd_client.connect(('192.168.1.106', 5050))
        self.connected = True
        self.DISCONNECT_MESSAGE = "!DISCONNECT"  #--------------------
    def start(self):
        threading.Thread(target=self.ref).start()
        while self.connected:
            cmd = input('>>: ').strip()
            if not cmd:
                continue
            self.gd_client.send(cmd.encode('utf-8'))

            if cmd == self.DISCONNECT_MESSAGE:#--------------------
                self.connected = False
                self.gd_client.close()
                break


    def ref(self):
        while self.connected:
            try:
                res = self.gd_client.recv(8096)
            except:
                print('斷線')
                break

            if not res:
                continue
            print(res.decode('utf-8'))

if __name__ == '__main__':
    cli().start()
