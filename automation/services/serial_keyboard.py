# https://stackoverflow.com/questions/21073086/wait-on-arduino-auto-reset-using-pyserial
import serial
import time

def new_arduino_connection(serial_port: str) -> serial.Serial:
    arduino = serial.Serial(
            serial_port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            xonxoff=0,
            rtscts=0
        )

    # Toggle DTR to reset Arduino
    arduino.setDTR(False)
    time.sleep(0.1)
    # toss any data already received, see
    # http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial.flushInput
    arduino.flushInput()
    arduino.setDTR(True)

    return arduino
