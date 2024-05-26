import serial.tools.list_ports
import serial as sp


class Communication:
    def __init__(self):
        self._frequency_1_ch: int = 100
        self._frequency_2_ch: int = 100
        self._frequency_3_ch: int = 100

        self._duty_1_ch: int = 50
        self._duty_2_ch: int = 50
        self._duty_3_ch: int = 50

        self.serial_port = None

    def set_frequency(self, channel: int, value: int):
        if channel == 1:
            self._frequency_1_ch = value
        if channel == 2:
            self._frequency_2_ch = value
        if channel == 3:
            self._frequency_3_ch = value

    def get_frequency(self, channel: int):
        if channel == 1:
            return self._frequency_1_ch
        if channel == 2:
            return self._frequency_2_ch
        if channel == 3:
            return self._frequency_3_ch

    @staticmethod
    def read_ports_list() -> list:
        return sp.tools.list_ports.comports()

    def connect_to_serial_port(self, port: str):
        try:
            self.serial_port = sp.Serial(
                port=port,
                baudrate=9600,
                stopbits=sp.STOPBITS_ONE,
                parity=sp.PARITY_NONE
            )
        except sp.SerialException as e:
            print(f"Can't open port {port}: {e}")

    def disconnect_serial_port(self):
        self.serial_port.close()

    def write_parameter_to_device(self, parameter: str, value: str) -> str:
        if parameter == "F":
            data = self.format_frequency(value)
        elif parameter in {"D1", "D2", "D3"}:
            data = self.format_duty(parameter, value)
        else:
            return

        if data:
            self.serial_port.write(data.encode('utf-8'))
            answer = self.serial_port.readline().decode('utf-8').strip()
            return answer

    def format_frequency(self, value: str) -> str:
        length = len(value)
        if length <= 3:
            return f"F{value}"
        elif length == 4:
            return f"F{value[0]}.{value[1:]}"
        elif length == 5:
            return f"F{value[:2]}.{value[2:]}"
        elif length == 6:
            return f"F{value[0]}.{value[1:3]}.{value[3:]}"
        return ""

    def format_duty(self, parameter: str, value: str) -> str:
        length = len(value)
        if length == 3:
            return f"{parameter}:{value}"
        elif length == 2:
            return f"{parameter}:0{value}"
        elif length == 1:
            return f"{parameter}:00{value}"
        return ""

    def read_all_parameters(self) -> str:
        self.serial_port.write(b'read')
        answer = self.serial_port.readline().decode('utf-8').strip()
        return answer
