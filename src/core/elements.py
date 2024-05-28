from PySide6.QtWidgets import QPushButton, QSpinBox, QComboBox


class Elements:
    def __init__(self, window=None):
        self.window = window

        self.search_button: QPushButton = self.window.findChild(QPushButton, "searchButton")
        self.connect_button: QPushButton = self.window.findChild(QPushButton, "connectButton")
        self.disconnect_button: QPushButton = self.window.findChild(QPushButton, "disconnectButton")
        self.set_button: QPushButton = self.window.findChild(QPushButton, "setButton")

        self.freqSpinBox: QSpinBox = self.window.findChild(QSpinBox, "freqSpinBox")
        self.d1SpinBox: QSpinBox = self.window.findChild(QSpinBox, "d1SpinBox")
        self.d2SpinBox: QSpinBox = self.window.findChild(QSpinBox, "d2SpinBox")
        self.d3SpinBox: QSpinBox = self.window.findChild(QSpinBox, "d3SpinBox")

        self.comboBox: QComboBox = self.window.findChild(QComboBox, "comboBox")

