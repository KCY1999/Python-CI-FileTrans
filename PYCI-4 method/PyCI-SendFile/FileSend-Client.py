'''
    Client端
    2021/9/8修改
    單傳送檔案-無json
'''
import socket, struct, threading
import time as t
download_dir = r'C:\Users\andyg\Desktop\PyClientRecive' #要下載在哪裡
gd_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #網路通訊,tcp
gd_client.connect(('192.168.43.135', 5050))


try:
    while True:
        text = gd_client.recv(100)

        code1, code2, name = struct.unpack('2i50s', text)  # 2int(1i:code1, 2i:code2)15lnString
        if code1 == int(0) and code2 == int(1):

            yn = input('是否接收檔案?Y/N>>>>')
            if yn == 'Y':
                text = struct.pack('2i50s', int(0), len('Yes'), 'Yes'.encode('utf-8'))  # 確定接收檔案(傳送封包)
                gd_client.send(text)

                print('wait file.....')
                text = gd_client.recv(100)
                total_size, name_len, name = struct.unpack('2i50s', text)  # 2int(1i:total_size, 2i:name_len)15lnString
                ff = ''
                aa = name.decode('utf-8')
                for i in range(name_len):
                    ff += aa[i:i + 1]
                file_name = ff

                with open(r'%s/%s' % (download_dir, file_name), 'wb') as f:  # 真正收檔案(windows是"\",linux是"/")
                    recv_size = 0

                    time1 = t.time()
                    while recv_size < total_size:
                        line = gd_client.recv(10240000)  # 一次收1mb
                        f.write(line)
                        recv_size += len(line)
                        # print('總大小：%s  已下載大小：%s' % (total_size, recv_size))
                    time2 = t.time()

                    print('time: ' + str(time2 - time1) + ' seconds')

            elif yn == 'N':
                text = struct.pack('2i50s', int(0), int(1), 'No'.encode('utf-8'))  # 確定接收檔案(傳送封包)
                gd_client.send(text)

            elif yn == 'Bye':
                text = struct.pack('2i50s', int(0), int(1), 'Bye'.encode('utf-8'))  # 確定接收檔案(傳送封包)
                gd_client.send(text)
                gd_client.close()
                break
            else:
                print('wrong commond')
except:
    print('error client')
    # ================================================================

#gd_client.close()