import socket
import threading
'''
https://alwaysfreesir.blogspot.com/2018/12/pythonsocket.html  
https://www.itread01.com/eieyl.html     #以上基本通訊函式

https://www.twblogs.net/a/5c897a1abd9eee35cd6a7b1d
https://docs.python.org/3/library/struct.html#format-characters  #以上struct.pack封包
'''
class ser():
  def __init__(self):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #要選擇通訊模式
    #a = self.server.settimeout(10)                                   #當沒有人連線時可以設定時間結束->(10)10秒
    ip = socket.gethostbyname(socket.gethostname())                 #找IP
    self.ti = True
    self.server.bind((ip, 5050))                                    #正式建立連線
    self.server.listen(1)                                           #client數量(從0開始算)
    print('建置完成,IP是', ip)
    self.DISCONNECT_MESSAGE = "!DISCONNECT"
    self.num=[]                                                     #宣告陣列->用在記錄client的address
    self.total=0

  def start(self):
    while self.ti:
      self.conn, self.addr = self.server.accept()
      w = threading.Thread(target=self.wirte)
      w.start()
      aaaa = threading.Thread(target=self.clien)
      aaaa.start()

  def clien(self):
    self.num.append(self.conn)
    self.total = len(self.num)
    res = ''
    print(f'人員{self.total}連接成功')
    while self.ti:
        res = self.num[self.total - 1].recv(8096)  # 收byte
        print(f'人員{self.total - 1}', res.decode('utf-8'))
        if not res:
            continue

        if res == self.DISCONNECT_MESSAGE:
          print(f'收到人員{self.total}斷線')
          break

  def wirte(self):
    while self.ti:
      cmd = input('>>: ').strip()
      print('ok')
      if not cmd:
        continue
      for i in range(self.total):
        print(i)
        self.num[i].send(cmd.encode('utf-8'))

if __name__ == '__main__':
    ser().start()