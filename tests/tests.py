import unittest
from src.core.serial_communication import Communication


class Test(unittest.TestCase):
    def setUp(self):
        self.obj = Communication()

    def test_parse_device_string(self):
        self.assertEqual(self.obj.parse_device_string("F101"), {'F': 101})
        self.assertEqual(self.obj.parse_device_string("F1.05"), {'F': 1050})
        self.assertEqual(self.obj.parse_device_string("F10.5"), {'F': 10500})
        self.assertEqual(self.obj.parse_device_string("F1.0.5"), {'F': 105000})

    def test_format_frequency(self):
        self.assertEqual(self.obj.format_frequency("101"), "F101")
        self.assertEqual(self.obj.format_frequency("1050"), "F1.05")
        self.assertEqual(self.obj.format_frequency("10500"), "F10.5")
        self.assertEqual(self.obj.format_frequency("15000"), "F15.0")
        self.assertEqual(self.obj.format_frequency("105000"), "F1.0.5")
        self.assertEqual(self.obj.format_frequency("150000"), "F1.5.0")

    def test_format_duty(self):
        self.assertEqual(self.obj.format_duty("D", "50"), "D:050")
        self.assertEqual(self.obj.format_duty("D", "5"), "D:005")
        self.assertEqual(self.obj.format_duty("D", "100"), "D:100")
        self.assertEqual(self.obj.format_duty("D", "10"), "D:010")


if __name__ == '__main__':
    unittest.main()
