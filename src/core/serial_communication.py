import asyncio
import serial.tools.list_ports
import serial_asyncio as sa


class Communication:
    def __init__(self):
        self._frequency: int = 100
        self._duty_1_ch: int = 50
        self._duty_2_ch: int = 50
        self._duty_3_ch: int = 50

        self.serial_reader = None
        self.serial_writer = None
        self.lock = asyncio.Lock()

    def set_frequency(self, value: int):
        self._frequency = value

    def get_frequency(self):
        return self._frequency

    def set_duty(self, duty_channel: str, value: int):
        duty_map = {
            "D1": "_duty_1_ch",
            "D2": "_duty_2_ch",
            "D3": "_duty_3_ch"
        }
        if duty_channel in duty_map:
            setattr(self, duty_map[duty_channel], value)

    def get_duty(self, duty_channel: str):
        duty_map = {
            "D1": "_duty_1_ch",
            "D2": "_duty_2_ch",
            "D3": "_duty_3_ch"
        }
        if duty_channel in duty_map:
            return getattr(self, duty_map[duty_channel])
        return None

    @staticmethod
    def read_ports_list() -> list:
        return list(serial.tools.list_ports.comports())

    async def connect_to_serial_port(self, port: str):
        try:
            self.serial_reader, self.serial_writer = await sa.open_serial_connection(
                url=port,
                baudrate=9600,
                stopbits=sa.serial.STOPBITS_ONE,
                parity=sa.serial.PARITY_NONE
            )
        except sa.serial.SerialException as e:
            print(f"Can't open port {port}: {e}")

    async def disconnect_serial_port(self):
        self.serial_writer.close()
        await self.serial_writer.wait_closed()

    async def write_parameter_to_device(self, parameter: str, value: str) -> str:
        async with self.lock:
            if parameter == "F":
                data = self.format_frequency(value)
            elif parameter in {"D1", "D2", "D3"}:
                data = self.format_duty(parameter, value)

            if data:
                self.serial_writer.write(data.encode('utf-8'))
                await self.serial_writer.drain()
                answer = await self.serial_reader.readline()
                return answer.decode('utf-8').strip()

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

    async def read_all_parameters(self) -> str:
        async with self.lock:
            self.serial_writer.write(b'read')
            await self.serial_writer.drain()
            answer = await self.serial_reader.readline()
            return answer.decode('utf-8').strip()

    def parse_device_string(self, data: str) -> dict:
        values = {}
        parts = data.split(',')
        for item in parts:
            if item.startswith('F'):
                values['F'] = int(item[1:])
            elif ':' in item:
                key, value = item.split(':')
                values[key] = int(value)
        return values