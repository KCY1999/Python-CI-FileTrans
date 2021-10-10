import socket, threading, struct, time as t, os, atexit

'''

Main=1  Sub=0 ---->基本聊天
                  Sub=1----->連線
Main=2 ----> Sub=0 送握手
　　　　　　　Sub=1 回握手
Main=3 ----> Sub=0 送檔名(所有人)
Main=3 ----> Sub=1 送檔名(單人)

都沒有------>傳檔案
**************************************************************
傳送檔案client要求server的資料:

輸入allsend(小寫) --->會發送給所有client->之後須在 get+空白+檔案名稱

輸入justsendtome(小寫)->只傳給本人 ->之後須在 get+空白+檔案名稱

輸入sendtosomeone(小寫)->指定傳給誰 ->對象(編號) -> 之後須在 get+空白+檔案名稱

********************以上由server方提供檔案**********************
從server要求client的資料:

輸入needfile(小寫)->要拿誰的資料 ->對象(編號) -> 之後須在 get+空白+檔案名稱


從c傳c:

輸入csendc->要拿誰的資料 ->對象(編號) -> 之後須在 get+空白+檔案名稱
********************以上由client方提供檔案**********************
'''


class ClientInt():
    def __init__(self):
        self.HEADER = 64
        PORT = 8080
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "192.168.64.1"
        self.ADDR = (self.SERVER, PORT)
        self.connected = True
        self.cconnect = True
        self.shack = True
        self.download_dir = r'C:\Users\andyg\Desktop\PyNetfile' #要下載在哪裡
        self.share_dir = r'C:\Users\andyg\Desktop\PyNetfile'
        self.recv_size = 0

    def wirt(self):
        while self.connected:
            a = input('>>: ').strip()
            if (a != ""):
                if(a=='allsend'):
                    a = input('Follow this format -> get filename   >>: ').strip()
                    if a[0:3]=='get':
                        bb=a[4:]
                        txt = struct.pack('3i15s', int(3), int(0),int(len(bb)), (a).encode(self.FORMAT))
                        self.client.send(txt)
                    else:
                        print('錯誤引數..')
                        break
                elif  (a=='justsendtome'):
                    a = input('Follow this format -> get filename   >>: ').strip()
                    if a[0:3]=='get':
                        bb=a[4:]
                        txt = struct.pack('3i15s', int(3), int(1),int(len(bb)), (a).encode(self.FORMAT))
                        self.client.send(txt)
                    else:
                        print('錯誤引數..')
                        break
                elif(a=='sendtosomeone'):
                    a = input('to whom>>: ').strip()
                    txt = struct.pack('3i15s', int(3), int(2), int(a),'nothing'.encode(self.FORMAT))
                    self.client.send(txt)
                    a = input('Follow this format -> get filename   >>: ').strip()
                    if a[0:3] == 'get':
                        bb = a[4:]
                        txt = struct.pack('3i15s', int(3), int(3), int(len(bb)), (a).encode(self.FORMAT))
                        self.client.send(txt)
                    else:
                        print('錯誤引數..')
                        break
                elif (a == 'csendc'):
                    whom = input('to whom>>: ').strip()

                    txt = struct.pack('3i15s', int(3), int(4), int(whom), whom.encode(self.FORMAT))
                    self.client.send(txt)

                    a = input('Follow this format -> get filename   >>: ').strip()
                    if a[0:3] == 'get':
                        bb = a[4:]
                        txt = struct.pack('3i15s', int(3), int(5), int(len(bb)), (a).encode(self.FORMAT))
                        self.client.send(txt)
                    else:
                        print('錯誤引數..')
                        break

                else:
                    txt = struct.pack('3i15s', int(1), int(0),int(len(a)),(a).encode(self.FORMAT))
                    self.client.send(txt)
                    if a == self.DISCONNECT_MESSAGE:
                        self.connected = False
                        self.cconnect = False
                        break
    def cc(self):
        while self.cconnect:
            #try:
                a = self.client.recv(4096)

                if len(a) == struct.calcsize('3i15s'):
                    head, sub,str1_len, str1 = struct.unpack('3i15s', a)
                    if head == 1 and sub == 0:
                        head = 0
                        sub = 0
                        print(str1.decode(self.FORMAT))
                    if head == 1 and sub == 1:
                        head = 0
                        sub = 0
                        print('你的編號是:' + str1.decode(self.FORMAT))
                    if head == 2 and sub == 0:
                        head = 0
                        sub = 0
                        self.Handshake()
                    if head == 3 and sub == 0:
                        f1 = ''
                        self.cmds = str1.decode('utf-8').split()
                        ff = self.cmds[1]

                        for i in range(str1_len):
                            f1 += ff[i:i + 1]

                        self.filename1 = f1

                        print(self.filename1)

                        self.passfile(sub)
                    if head == 3 and sub==5:
                        f1 = ''
                        self.cmds = str1.decode('utf-8').split()
                        ff = self.cmds[1]

                        for i in range(str1_len):
                            f1 += ff[i:i + 1]

                        self.filename1 = f1

                        print(self.filename1)

                        self.head_size = os.path.getsize(r'%s/%s' % (self.share_dir, self.filename1))

                        self.client.send(
                            struct.pack('4i35s', int(3), int(3), int(self.head_size), int(len(self.filename1)),
                                        (self.filename1).encode(self.FORMAT)))
                        self.c_pass_c()
                elif len(a)== struct.calcsize('4i35s'):
                    ff=''
                    head, sub,self.total_size,name_len,name = struct.unpack('4i35s', a)
                    if head==3 and sub==2:
                        aa=name.decode(self.FORMAT)
                        for i in range(name_len):
                            ff+=aa[i:i+1]

                        self.filename = ff
                        print(self.filename)
                        self.fileimg()
                    if head==3 and sub==3:

                        aa = name.decode(self.FORMAT)
                        for i in range(name_len):
                            ff += aa[i:i + 1]

                        self.filename = ff
                        print(self.filename)
                        self.fileimg()

    def fileimg(self):
            #print('---wait--')
            self.cconnect=False
            self.connected=False
            t.sleep(0.3)

            with open('%s\%s' % (self.download_dir, self.filename), 'wb') as f:
                self.recv_size=0
                f1=t.time()
                while self.recv_size < self.total_size:
                    w = self.client.recv(409600)
                    f.write(w)
                    self.recv_size += len(w)
                    w=''
                    #print('總大小：%s  已接收：%s' % (self.total_size, self.recv_size))
                f2 = t.time()
                print('接收完畢...時間:     ',(f2-f1))
            txt = struct.pack('2i15s', int(4), int(0),'ok'.encode(self.FORMAT))
            self.client.send(txt)

            self.cconnect = True
            self.connected = True

    def c_pass_c(self):
        self.cconnect = False
        self.connected = False
        self.shack = False
        # ==============================================================================================================
        t.sleep(5)
        print('---GO---')
        with open(r'%s/%s' % (self.share_dir, self.filename1), 'rb') as f:
            print('...')
            for line in f:
                print(len(line))

                self.client.send(line)
            print('傳送結束....')

        t.sleep(5)

        self.cconnect = True
        self.connected = True
        self.shack = True

    def passfile(self,how):  #哪種方式，要傳給誰，誰要傳的
            self.cconnect = False
            self.connected = False
            self.shack=False
            # ==============================================================================================================
            t.sleep(5)
            self.head_size=os.path.getsize(r'%s/%s' % (self.share_dir, self.filename1))

            with open(r'%s/%s' % (self.share_dir, self.filename1),'rb') as f:
                self.client.send(struct.pack('4i35s', int(3), int(2), int(self.head_size), int(len(self.filename1)),
                                        (self.filename1).encode(self.FORMAT)))
                for line in f:
                        print(len(line))
                        self.client.send(line)
                print('傳送結束....')
            t.sleep(5)

            self.cconnect = True
            self.connected = True
            self.shack = True

    def Handshake(self):
        #print('SERVER問')
            if self.shack:
                txt = struct.pack('2i15s', int(2), int(1), ('just handshake2').encode(self.FORMAT))
                self.client.send(txt)
        #print('已回傳封包')

    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

        self.thread = threading.Thread(target=self.wirt)
        self.thread.start()
        self.connected = True
        self.thread2 = threading.Thread(target=self.cc)
        self.thread2.start()
        self.cconnect = True

if __name__ == '__main__':
    ClientInt().start()