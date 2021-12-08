import switchControl as switch
import socket
import time
import test as checkSleep
import speaker

host = '220.69.172.48'  # 호스트 ip를 적어주세요
port = 8080  # 포트번호를 임의로 설정해주세요

try:
    # speaker.ringAlarm()
    server_sock = socket.socket(socket.AF_INET)
    server_sock.bind((host, port))
    server_sock.listen(1)
    out_data = int(10)
    print("기다리는 중..")

    try:
        switch.initSwitchControl()

        while True:
            client_sock, addr = server_sock.accept()

            if client_sock:
                print('Connect with' + addr[0] + ":" + str(addr[1]))
                buf = client_sock.recv(512)
                result = buf.decode('utf-8')
                print(result)

                if (result[0] == "r"):
                    switch.switchControl(result[2:])
                elif (result[0] == "s"):
                    set_value = result[2:]  # save setting values
                    speaker.ringAlarm()
                    checkSleep.modelRun(set_value)


    except KeyboardInterrupt:
        switch.GPIO.cleanup()
        client_sock.close()
        server_sock.close()
        pass


except socket.error as err:
    print('error====================================')



