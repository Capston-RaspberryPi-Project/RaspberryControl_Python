import RPi.GPIO as GPIO # 필요한 라이브러리를 불러오기
import time
import keyboard


# 사용할 GPIO핀의 번호를 선정(BCM 모드)
all_pin = 4 #GPIO4
first_pin = 23 #GPIO23
second_pin = 24 #GPIO24
third_pin = 17 #GPIO17
fourth_pin = 27 #GPIO27
fifth_pin = 22 #GPIO22
sixth_pin = 10 #GPIO10

# 불필요한 warning 제거
GPIO.setwarnings(False)

# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)

# LED 핀의 IN/OUT 설정
GPIO.setup(all_pin, GPIO.OUT)
GPIO.setup(first_pin, GPIO.OUT, initial=1)
GPIO.setup(second_pin, GPIO.OUT, initial=1)
GPIO.setup(third_pin, GPIO.OUT, initial=1)
GPIO.setup(fourth_pin, GPIO.OUT, initial=1)
GPIO.setup(fifth_pin, GPIO.OUT, initial=1)
GPIO.setup(sixth_pin, GPIO.OUT, initial=1)

# # 전체 전원 제어
# for i in range(10): # 0~9(10-1)까지 10번 반복
#     GPIO.output(all_pin,1) # 멀티탭 ON
#     time.sleep(5) # 3초동안 대기상태
#     GPIO.output(all_pin,0) # 멀티탭 OFF
#     time.sleep(5) # 3초동안 대기상태

# # 개별 제어
# GPIO.output(all_pin, 1) #전체 전원 ON

try:
    while 1:
        GPIO.output(first_pin,0) # 첫번째 스위치 ON
        print("1번")
        time.sleep(3) # 3초동안 대기상태
        

        GPIO.output(second_pin,0) # 두번째 스위치 ON
        print("2번")
        time.sleep(3) # 3초동안 대기상태
        

        GPIO.output(third_pin,0) # 세번째 스위치 ON
        print("3번")
        time.sleep(3) # 3초동안 대기상태
        

        GPIO.output(fourth_pin,0) # 네번째 스위치 ON
        print("4번")
        time.sleep(3) # 3초동안 대기상태
        

        GPIO.output(fifth_pin,0) # 다섯번째 스위치 ON
        print("5번")
        time.sleep(3) # 3초동안 대기상태
        
        GPIO.output(sixth_pin,0) # 여섯번째 스위치 ON
        print("6번")
        time.sleep(3) # 3초동안 대기상태

        GPIO.output(all_pin,0) # 여섯번째 스위치 ON
        print("모든 스위치 OFF")
        time.sleep(3) # 3초동안 대기상태
        
except KeyboardInterrupt:
    GPIO.cleanup() # GPIO 설정 초기화
    pass

