'''
    Server端
    2021/9/8修改
    單傳送檔案-無json
'''
import socket,os,struct,time

share_dir = r'C:\Users\芳羽\Desktop\work\Test'                            #可存取的路徑
gd_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #連線設定(網路通訊,TCP)

SERVER = socket.gethostbyname(socket.gethostname())
gd_server.bind((SERVER, 5050))                         #建立本機的IP
gd_server.listen(5)                                              #可連線數量為6(包含0)
print('建置成功  ip:',SERVER)

while True:
  conn, addr = gd_server.accept()                               #開始等待接收client連線要求
  while True:
    try:
      res = conn.recv(8096)  # 接收訊息(會收到get 1.txt等)
    except:
      print('傳送訊息出問題')

    cmds = res.decode('utf-8').split()  # 接收檔案名稱
    print(cmds)
    filename = cmds[1]
    print('收到的檔案名稱為',filename)

    text=struct.pack('2i15s',os.path.getsize(r'%s\%s'%(share_dir,filename)),len(filename),filename.encode('utf-8'))
    conn.send(text)

    time.sleep(0.5)
    file = open(r'%s/%s' % (share_dir, filename), 'rb')

    sfile = file.read(409600)
    while sfile:
      conn.send(sfile)
      sfile = file.read(409600)
    print('傳送結束....')
