import serial
import time


def start():
    port = 'COM3'  # замените на соответствующий порт вашего телефона
    baudrate = 9600  # скорость обмена данными

    ser = serial.Serial(port, baudrate, timeout=1)

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()

            if line:
                print(line)

            time.sleep(0.1)

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    start()
