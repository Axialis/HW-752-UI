import asyncio

import qasync
from PySide6.QtCore import QObject
from src.core.serial_communication import Communication
from src.core.elements import Elements


class ProcessHandler(QObject):
    def __init__(self, window):
        super().__init__()
        self.communication = Communication()
        self.elements = Elements(window)

        self.ports = None

        self.reader = None
        self.writer = None

        self.elements.freqSpinBox.valueChanged.connect(lambda value: self.change_field_value("F"))
        self.elements.d1SpinBox.valueChanged.connect(lambda value: self.change_field_value("D1"))
        self.elements.d2SpinBox.valueChanged.connect(lambda value: self.change_field_value("D2"))
        self.elements.d3SpinBox.valueChanged.connect(lambda value: self.change_field_value("D3"))

        self.elements.search_button.clicked.connect(self.update_devices_list)
        self.elements.connect_button.clicked.connect(self.connect_device)
        self.elements.disconnect_button.clicked.connect(self.disconnect_device)
        self.elements.set_button.clicked.connect(self.set_value)

        self.elements.set_button.setDisabled(True)
    def change_field_value(self, element):
        actions = {
            "F": lambda: self.communication.set_frequency(self.elements.freqSpinBox.value()),
            "D1": lambda: self.communication.set_duty(element, self.elements.d1SpinBox.value()),
            "D2": lambda: self.communication.set_duty(element, self.elements.d2SpinBox.value()),
            "D3": lambda: self.communication.set_duty(element, self.elements.d3SpinBox.value())
        }
        action = actions.get(element, lambda: None)
        action()

    def change_ui_value(self, element: str, value: int):
        actions = {
            "F": lambda: self.elements.freqSpinBox.setValue(value),
            "D1": lambda: self.elements.d1SpinBox.setValue(value),
            "D2": lambda: self.elements.d2SpinBox.setValue(value),
            "D3": lambda: self.elements.d3SpinBox.setValue(value)
        }
        action = actions.get(element, lambda: None)
        action()
    def update_devices_list(self):

        self.ports = self.communication.read_ports_list()
        self.elements.comboBox.clear()
        if self.ports:
            for port in self.ports:
                self.elements.comboBox.addItem(port.device)

    @qasync.asyncSlot()
    async def connect_device(self):
        await self.communication.connect_to_serial_port(self.elements.comboBox.currentText())
        self.elements.set_button.setDisabled(False)
        answer = await self.communication.read_all_parameters()
        parsed_answer = self.communication.parse_device_string(answer)
        for key, value in parsed_answer.items():
            if key == "F":
                self.communication.set_frequency(value)
                self.change_ui_value(key, value)
            if key in {"D1", "D2", "D3"}:
                self.communication.set_duty(key, value)
                self.change_ui_value(key, value)

    @qasync.asyncSlot()
    async def disconnect_device(self):
        await self.communication.disconnect_serial_port()

    @qasync.asyncSlot()
    async def set_value(self):
        self.elements.set_button.setDisabled(True)
        answer = await self.communication.read_all_parameters()
        parsed_answer = self.communication.parse_device_string(answer)

        parameter_map = {
            "F": self.elements.freqSpinBox,
            "D1": self.elements.d1SpinBox,
            "D2": self.elements.d2SpinBox,
            "D3": self.elements.d3SpinBox
        }

        tasks = []
        for key, spinbox in parameter_map.items():
            if key in parsed_answer and parsed_answer[key] != spinbox.value():
                tasks.append(self.communication.write_parameter_to_device(key, str(spinbox.value())))

        await asyncio.gather(*tasks)
        self.elements.set_button.setDisabled(False)

