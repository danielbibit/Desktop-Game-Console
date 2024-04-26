# https://stackoverflow.com/questions/21073086/wait-on-arduino-auto-reset-using-pyserial
import serial
import time


hid_keycodes = {
    'ESC': 41,
    'WIN_LEFT': 227,
    'WIN_RIGHT': 231,
    'L_CTRL': 224,
    'R_CTRL': 228,
    'L_SHIFT': 225,
    'R_SHIFT': 229,
    'L_ALT': 226,
    'R_ALT': 230,
    'BACKSPACE': 42,
    'TAB': 43,
    'ENTER': 40,
    'SPACE': 44,
    'CAPS_LOCK': 57,
}

class SerialKeyboard():
    def __init__(self, com_port: str):
        self.com_port = com_port
        self.serial_terminator = b'\n'

    def _new_arduino_connection(self) -> serial.Serial:
        arduino = serial.Serial(
                self.com_port,
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

    def write_ascii(self, code: int) -> None:
        try:
            with self._new_arduino_connection() as stream:
                stream.write(b'write:' + str(code).encode() + self.serial_terminator)

        except Exception as e:
            print('Error while writing to keyboard')
            print(e)

    def write_keycode(self, code: int) -> None:
        try:
            with self._new_arduino_connection() as stream:
                stream.write(b'keycode:' + str(code).encode() + self.serial_terminator)

        except Exception as e:
            print('Error while writing to keyboard')
            print(e)

    def type_string(self, string: str) -> None:
        try:
            with self._new_arduino_connection() as stream:
                for char in string:

                    ascii_int = ord(char)
                    ascii_int_bytes = str(ascii_int).encode('ascii')

                    print('writing: ' + repr(char) + ' ascii: ' + str(ascii_int))

                    data_send = 'write:'.encode('ascii') + ascii_int_bytes + self.serial_terminator

                    stream.write( data_send)

                    time.sleep(0.01)

        except Exception as e:
            print('Error while writing to keyboard')
            print(e)

    def send_hotkey(self, *args):
        # TODO implement hotkey sending
        # 'hotkey:9,10,17\n
        pass
