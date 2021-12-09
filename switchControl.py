import RPi.GPIO as GPIO  # 필요한 라이브러리를 불러오기
import time
import keyboard

# 사용할 GPIO핀의 번호를 선정(BCM 모드)
# all_pin = 4 #GPIO4
first_pin = 23  # GPIO23
second_pin = 24  # GPIO24
third_pin = 17  # GPIO17
fourth_pin = 27  # GPIO27
fifth_pin = 22  # GPIO22
sixth_pin = 10  # GPIO10

# 사용할 핀 배열
pins = [second_pin, third_pin, fourth_pin, fifth_pin, sixth_pin]


def initSwitchControl():
    # 불필요한 warning 제거
    GPIO.setwarnings(False)

    # GPIO핀의 번호 모드 설정
    GPIO.setmode(GPIO.BCM)

    # LED 핀의 IN/OUT 설정
    # GPIO.setup(all_pin, GPIO.OUT)
    GPIO.setup(first_pin, GPIO.OUT, initial=1)
    GPIO.setup(second_pin, GPIO.OUT, initial=1)
    GPIO.setup(third_pin, GPIO.OUT, initial=1)
    GPIO.setup(fourth_pin, GPIO.OUT, initial=1)
    GPIO.setup(fifth_pin, GPIO.OUT, initial=1)
    GPIO.setup(sixth_pin, GPIO.OUT, initial=1)
    GPIO.setup(sixth_pin, GPIO.OUT, initial=1)
    return


def individualSwitchControl():
    try:
        while 1:
            GPIO.output(first_pin, 0)  # 첫번째 스위치 ON
            print("1번")
            time.sleep(3)  # 3초동안 대기상태

            GPIO.output(second_pin, 0)  # 두번째 스위치 ON
            print("2번")
            time.sleep(3)  # 3초동안 대기상태

            GPIO.output(third_pin, 0)  # 세번째 스위치 ON
            print("3번")
            time.sleep(3)  # 3초동안 대기상태

            GPIO.output(fourth_pin, 0)  # 네번째 스위치 ON
            print("4번")
            time.sleep(3)  # 3초동안 대기상태

            GPIO.output(fifth_pin, 0)  # 다섯번째 스위치 ON
            print("5번")
            time.sleep(3)  # 3초동안 대기상태

            GPIO.output(sixth_pin, 0)  # 여섯번째 스위치 ON
            print("6번")
            time.sleep(3)  # 3초동안 대기상태

            # GPIO.output(all_pin,0) # 여섯번째 스위치 ON
            # print("모든 스위치 OFF")
            # time.sleep(3) # 3초동안 대기상태

    except KeyboardInterrupt:
        GPIO.cleanup()  # GPIO 설정 초기화
        pass


def checkOn():
    try:
        while 1:
            GPIO.output(sixth_pin, 0)  # 여섯번째 스위치 ONclea
            if (input_pin == GPIO.HIGH):
                print("전원 ON")
            else:
                print("전원 OFF")
            time.sleep(3)
    except KeyboardInterrupt:
        GPIO.cleanup()  # GPIO 설정 초기화
        pass


def switchControl(switch):
    for i in range(0, 5):
        if (switch[i] == '1'):
            GPIO.output(pins[i], 0)
            # print(str(i+1)+" 번 탭 ON")
        else:
            GPIO.output(pins[i], 1)
            # print(str(i+1)+" 번 탭 OFF")


def allSwitchOn():
    # 전체 전원 제어
    for i in range(0, 5):
        GPIO.output(pins[i], 0)
    print("모든 탭 ON")


def allSwitchOff():
    # 전체 전원 제어
    for i in range(0, 5):
        GPIO.output(pins[i], 1)
    print("모든 탭 OFF")
