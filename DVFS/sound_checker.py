import subprocess
import time
import os

# 체크 주기 (초 단위)
interval = 1  

# 온도 임계값
threshold = 30000  

# 알림음 재생을 위한 명령어 (기본적인 리눅스 beep)
def play_sound():
    duration = 1  # 소리 길이(초)
    freq = 440    # 주파수(Hz)
    os.system(f'play -nq -t alsa synth {duration} sine {freq}')  # sox가 설치되어 있어야 함

# adb 명령어 실행 후 온도값 반환
def get_temperature():
    try:
        output = subprocess.check_output(['adb', 'shell', 'cat', '/dev/thermal/tz-by-name/battery/temp'])
        temp = int(output.strip())
        print(f"현재 온도: {temp}")
        return temp
    except subprocess.CalledProcessError as e:
        print("ADB 명령 실행 중 오류 발생:", e)
        return None
    except ValueError as e:
        print("값 변환 오류 발생:", e)
        return None

def monitor_temperature():
    while True:
        temp = get_temperature()
        if temp is not None and temp >= threshold:
            print("임계값 도달! 알림음을 재생합니다.")
            play_sound()
            break
        time.sleep(interval)

if __name__ == "__main__":
    monitor_temperature()
