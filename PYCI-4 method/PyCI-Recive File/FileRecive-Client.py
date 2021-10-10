'''
    Client端
    2021/9/8修改
    單傳送檔案-無json
'''
import socket, struct
import time as t
download_dir = r'C:\Users\芳羽\Desktop\下載區域' #要下載在哪裡
gd_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #網路通訊,tcp
gd_client.connect(('192.168.1.106',5050))


while True:
    cmd = input('>>: ').strip()  # get 1.txt
    if not cmd:
        continue
    gd_client.send(cmd.encode('utf-8'))

    text=gd_client.recv(100)

    total_size,name_len,name=struct.unpack('2i15s',text)
    ff=''
    aa=name.decode('utf-8')
    for i in range(name_len):
        ff += aa[i:i + 1]
    file_name=ff



    with open(r'%s\%s' % (download_dir, file_name), 'wb') as f:#真正收檔案
        recv_size = 0

        time1=t.time()
        while recv_size < total_size:
            line = gd_client.recv(10240000) #一次收1mb
            f.write(line)
            recv_size += len(line)
            print('總大小：%s  已下載大小：%s' % (total_size, recv_size))
        time2 = t.time()

        print('time: ' + str(time2 - time1) + ' seconds')
    # ================================================================

gd_client.close()
