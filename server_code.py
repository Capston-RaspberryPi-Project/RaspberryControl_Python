import switchControl as switch
import socket
import time
import test as checkSleep

host = '220.69.172.156' # 호스트 ip를 적어주세요
port = 8080            # 포트번호를 임의로 설정해주세요

isClosed = False
start_time = 0
end_time = 0
closeTime = 0
countsleep = 0

issleep = False

try :
    server_sock = socket.socket(socket.AF_INET)
    server_sock.bind((host, port))
    server_sock.listen(1)
    out_data = int(10)
except socket.error as err:
    print('error')

print("기다리는 중..")

try:
    switch.initSwitchControl()

    while True:
        client_sock, addr = server_sock.accept()

        if client_sock:
            print('Connect with' + addr[0] + ":" + str(addr[1]))
            buf = client_sock.recv(512)
            print(type(buf))

            # decode bytes to string
            result = buf.decode('utf-8')
            print(result)
            
            if (result[0] == "r"):
                switch.switchControl(result[1:])
            elif (result[0] == "s"):
                set_value = result[1:] # save setting values
                pass

            checkSleep.modelRun(isClosed, start_time, end_time, closeTime, countsleep, issleep, set_value)

            # time.sleep(5)
            
                # print("졸음 감지 !")
            # if (checkSleep.getIssleep()): # detect sleep
            #     switch.switchControl(set_value)
            #     checkSleep.setIssleep(False)
                     
except KeyboardInterrupt:
    switch.GPIO.cleanup()
    client_sock.close()
    server_sock.close()
    pass

switch.GPIO.cleanup()
client_sock.close()
server_sock.close()



