'''
    Server端
    2021/9/23修改
    單傳送檔案-無json
'''
import socket, os, struct, time, threading

share_dir = r'C:\Users\andyg\Desktop\PyServerSend'                            #可存取的路徑
gd_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #連線設定(網路通訊,TCP)

SERVER = '172.17.194.128'#socket.gethostbyname(socket.gethostname())
gd_server.bind(('172.20.10.2', 5050))  #(SERVER, 5050)                       #建立本機的IP
#下方Terminal獲取本機IP指令
#python -c "import socket;print([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])"
gd_server.listen(5)                                              #可連線數量為6(包含0)
print('建置成功  ip:', SERVER)

try:
  while True:
    conn, addr = gd_server.accept()                               #開始等待接收client連線要求
    while True:
      text = struct.pack('2i50s', int(0), int(1), 'recive?'.encode('utf-8'))  #詢問是否接收
      conn.send(text)

      text = conn.recv(100)
      total_size, name_len, name = struct.unpack('2i50s', text)

      ff = ''
      aa = name.decode('utf-8')
      for i in range(name_len):
        ff += aa[i:i + 1]
      name = ff

      if name == 'Yes':
        filename = input('filename>>').strip()
        # windows是"\",linux是"/"
        text = struct.pack('2i50s', os.path.getsize(r'%s\%s' % (share_dir, filename)), len(filename), filename.encode('utf-8'))
        conn.send(text)

        time.sleep(0.5)
        file = open(r'%s/%s' % (share_dir, filename), 'rb')

        sfile = file.read(409600)
        while sfile:
          conn.send(sfile)
          sfile = file.read(409600)
        print('傳送結束....')
      elif name == 'No':
        text = struct.pack('2i50s', int(0), int(1), 'recive?'.encode('utf-8'))  # 詢問是否接收
        conn.send(text)

      elif name == 'Bye':
        print('client disconnect')
      else:
        print('wrong commond')
except:
  print('error server')

