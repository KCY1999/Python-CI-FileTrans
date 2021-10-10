import socket, threading, struct, os
import time as t

'''

Main=1  Sub=0 ---->基本聊天
                  Sub=1----->連線
Main=2 ----> Sub=0 送握手
　　　　　　　Sub=1 回握手
Main=3 ----> Sub=0 送檔名(所有人)
Main=3 ----> Sub=1 送檔名(單人)

都沒有------>傳檔案

********************以上由server方提供檔案**********************
從server要求client的資料:

輸入needfile(小寫)->要拿誰的資料 ->對象(編號) -> 之後須在 get+空白+檔案名稱


從c傳c:

輸入needclientfile->要拿誰的資料 ->對象(編號) -> 之後須在 get+空白+檔案名稱
********************以上由client方提供檔案**********************
'''

class ServerInt():
    def __init__(self):
        #--------------------------變數設定---------------------------
        self.share_dir = r'C:\Users\andyg\Desktop\PyServerPost'
        self.download_dir= r'C:\Users\andyg\Desktop\PyServerPost'
        self.HEADER = 64
        PORT = 8080
        self.inputs = []
        self.fd_name = {}
        self.num = []
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.bb=''
        self.filename1=''
        self.checktstop=[]                                              #確認封包有無回傳時間->無就斷線
        self.checktime=[]
        self.lose=[]#0正常1段縣
        self.want=0
        self.wwho=0
        self.connected=True
    def con(self):

        print('runing....')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.server.listen(3)
        return self.server
    def handle_client(self):
        self.num.append(self.conn)
        self.checktstop.append(0)
        self.checktime.append(0)
        self.lose.append(0)
        total=len(self.num)
        self.total1=total

        if(self.total1>4):
            self.connected=False
            self.shack=False
            self.full_m()
            total=len(self.num)
            print(f"[新連線] 人員  {self.total1+1} connected.")
            self.connected = True
            self.shack=True

        else:
            txt = struct.pack('3i15s', int(1), int(1),int(total), (str(total)).encode(self.FORMAT))
            self.num[total-1].send(txt)
            print(f"[新連線] 人員  {total} connected.")
            self.connected = True
            self.shack = True

        while self.connected:
            try:
                if(self.lose[total-1]==1):
                    break
                self.bb = self.num[total - 1].recv(2048)
            except :
                if self.num[total - 1] and (self.lose[total-1] != 1):
                        self.lose[total-1]=1
                        self.bb=''
                        self.num[total - 1] = ''
                        print(self.num[total-1])
                        print(f"人員{total}斷線33")
                        break

            if len(self.bb) == struct.calcsize('3i15s'):
                self.head, self.sub,str1_len ,self.str1 = struct.unpack('3i15s', self.bb)
            # ----------------------------------------------------------------------------
                if self.head==1 and self.sub==0:
                    if self.bb == self.DISCONNECT_MESSAGE:
                        self.head = 0
                        self.sub = 0
                        self.lose[total-1]=1
                        self.num[total-1]=''
                        print(f"[人員{total}斷線22]")
                        break
                    else:
                        print(self.bb)
                        print(self.head)
                        print(self.sub)
                        print(f"[人員{total}]"+self.str1.decode(self.FORMAT))
            #-----------------------------------------------------------------------------
                elif self.head==2 and self.sub==1:
                    '''if(self.num[total-1]!=''):
                        print(f'收到{total}的回傳握手')'''
            # ----------------------------------------------------------------------------
                elif self.head==3 and self.sub==0 or self.sub==1:
                    f1=''
                    self.cmds = self.str1.decode('utf-8').split()
                    ff = self.cmds[1]

                    for i in range(str1_len):
                        f1+=ff[i:i+1]

                    self.filename1=f1

                    print(self.filename1)
                    self.passfile(self.sub,(total-1),(total-1))
                elif self.head==3 and self.sub==2:
                    who=str1_len-1
                    print('送給',who)
                    self.head = 0
                    self.sub = 0

                elif self.head==3 and self.sub==3:
                    f1 = ''
                    self.cmds = self.str1.decode('utf-8').split()
                    ff = self.cmds[1]

                    for i in range(str1_len):
                        f1 += ff[i:i + 1]

                    self.filename1 = f1

                    print(self.filename1)

                    self.passfile(self.sub, who,(total-1))
                    break
                elif self.head==3 and self.sub==4:

                    self.wwho=str1_len-1

                elif self.head==3 and self.sub==5:

                    self.num[self.wwho].send(self.bb)
                    self.want=total-1
                    break
                else:
                    print('下一輪')

            elif len(self.bb) == struct.calcsize('4i35s'):
                ff = ''
                head, sub, self.total_size, name_len, name = struct.unpack('4i35s', self.bb)
                if head == 3 and sub == 2:
                    aa = name.decode(self.FORMAT)
                    for i in range(name_len):
                        ff += aa[i:i + 1]

                    self.filename = ff
                    print(self.filename)

                    self.fileimg((total-1))
                    break
                if head == 3 and sub == 3:
                    self.num[self.want].send(self.bb)

                    self.c_pass_c(int(self.wwho), (self.want))

            else:
                self.head = 0
                self.sub = 0
                self.bb = ''
        #self.conn.close()
    def c_pass_c(self,whom,want):
        self.shack = False
        self.connected=False
        self.recv_size=0
        # ==============================================================================================================
        while self.recv_size<self.total_size:
            self.bb = self.num[whom].recv(2048)
            self.num[want].send(self.bb)
            print(len(self.bb))
            self.recv_size+=len(self.bb)


        self.connected= True
        self.shack = True

    def full_m(self):
            self.n=0
            for i in range(len(self.num)-1):
                if self.lose[i]==1:
                    self.num[i]=self.num[len(self.num)-1]
                    a = i + 1
                    t = str(a)
                    txt = struct.pack('3i15s', int(1), int(1), int(len(t)),t.encode(self.FORMAT))
                    self.num[i].send(txt)
                    self.lose[i]=0
                    self.lose[len(self.num)-1]=0
                    self.n=i
                    break

            if (len(self.num) > 4):
                self.num.pop()
                self.total1=self.n
            else:
                self.total1 = len(self.num)

    def passmem(self):
        for i in range(len(self.num) - 1):
            if self.lose[i] == 1:
                self.num[i] = self.num[i + 1]
                a = i + 1
                t = str(a)
                txt = struct.pack('3i15s', int(1), int(1), int(len(t)), t.encode(self.FORMAT))
                self.num[i].send(txt)
                self.lose[i] = 0
                self.lose[i + 1] = 1

        if self.lose[len(self.num) - 1] == 1:
            self.num[len(self.num) - 1] = ''

    def wirttime(self):
        while self.connected:
            a = input('>>: ').strip()
            if(a!=''):
                self.wirt(a)

    def wirt(self,a):
                if a != "":
                    if (a == 'needfile'):
                        whom = input('to whom>>: ').strip()
                        a = input('Follow this format -> get filename   >>: ').strip()
                        if a[0:3] == 'get':
                            bb = a[4:]
                            txt = struct.pack('3i15s', int(3), int(0), int(len(bb)), (a).encode(self.FORMAT))
                            self.num[int(whom)].send(txt)
                        else:
                            print('錯誤引數..')

                    elif a[0:2]!='al':
                        message = a.encode(self.FORMAT)
                        r = len(self.num)
                        for i in range(r):
                            if(self.lose[i]!=1 and self.num[i]!=''):
                                txt = struct.pack('3i15s', int(1), int(0), int(len(message)), message)
                                self.num[i].send(txt)
                    elif a[0:2]=='al':
                        al = int(a[2:3])
                        if (self.lose[al] != 1 and self.num[al]!=''):
                            me=a[3:]
                            message = me.encode(self.FORMAT)
                            txt = struct.pack('3i15s', int(1), int(0), int(len(message)), message)
                            self.num[al].send(txt)

    def timclick(self):
        while self.shack:
            t.sleep(5)
            self.connec()

    def connec(self):
        if self.shack:
            for i in range(len(self.num)):
                if (self.lose[i] != 1):
                    txt = struct.pack('3i15s', int(2), int(0),len('just handshake'), ('just handshake').encode(self.FORMAT))
                    self.num[i].send(txt)
                    self.checktime[i] = t.time()

    def checkpkg(self):
        while self.shack:
            r = len(self.num)
            self.checktstop[r - 1] = t.time()
            for i in range(r):
                if(self.checktime[i] - self.checktstop[i]) > 10000:
                    self.lose[i] = 1
                    self.num[i] = ''
                    print(f"人員{i + 1}斷線11",self.checktime[i])
                    self.checktime[i]=0
                    self.checktstop[i]=0

    def fileimg(self,whom):#---------------------------------------------

            self.shack=False
            self.connected=False

            t.sleep(0.3)

            with open('%s\%s' % (self.download_dir, self.filename), 'wb') as f:
                self.recv_size=0
                while self.recv_size < self.total_size:
                    w = self.num[whom].recv(4096)
                    f.write(w)
                    self.recv_size += len(w)
                    w=''
                    print('總大小：%s  已接收：%s' % (self.total_size, self.recv_size))

            print('接收完畢......')
            f.close()
            txt = struct.pack('2i15s', int(4), int(0),'ok'.encode(self.FORMAT))
            self.num[whom].send(txt)

            t.sleep(5)
            self.shack = True
            self.connected = True

    def passfile(self,how,who,no):  #哪種方式，要傳給誰，誰要傳的
            self.shack = False
            # ==============================================================================================================
            t.sleep(5)
            self.head_size=os.path.getsize(r'%s/%s' % (self.share_dir, self.filename1))

            if how == 0:
                for i in range(len(self.num)):
                    self.num[i].send(
                        struct.pack('4i35s', int(3), int(2), int(self.head_size), int(len(self.filename1)),
                                    (self.filename1).encode(self.FORMAT)))
            elif how == 1 or how == 3:
                self.num[who].send(
                    struct.pack('4i35s', int(3), int(2), int(self.head_size), int(len(self.filename1)),
                                (self.filename1).encode(self.FORMAT)))

            file= open(r'%s/%s' % (self.share_dir, self.filename1),'rb')

            f1 = t.time()
            sfile=file.read(409600)  #200mb

            while sfile:
                if how==0:#全體

                    for i in range(len(self.num)):
                        try:
                            self.num[i].send(sfile)
                        except:
                            self.lose[i] = ''
                            self.num[i] = ''
                            print(f"[人員{i+1}傳檔案時斷線]")
                            break

                if how==1 or how==3:  #給誰
                        #print(len(line))
                        try:
                            self.num[who].send(sfile)
                        except:
                            self.lose[who] = ''
                            self.num[who] = ''
                            print(f"[人員{who + 1}傳檔案時斷線]")
                            break
                sfile = file.read(409600)
            f2 = t.time()
            print('傳送完畢...時間:     ', (f2 - f1))


            self.shack = True


    def start(self):
        ss = self.con()
        ss.listen()
        self.inputs.append(ss)
        print(f"[LISTENING] IP: {self.SERVER}")
        try:
            while True:
                self.conn, self.addr = ss.accept()
                aaaa = threading.Thread(target=self.handle_client)
                aaaa.start()
                thread2 = threading.Thread(target=self.wirttime)
                thread2.start()
                thread4 = threading.Thread(target=self.timclick)
                thread4.start()
                thread5 = threading.Thread(target=self.checkpkg)
                thread5.start()
        except Exception:
            print('thread出現錯誤')

if __name__ == '__main__':
    ServerInt().start()