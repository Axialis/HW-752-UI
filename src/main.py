from src.core.serial_communication import Communication


com = Communication()
com.connect_to_serial_port('COM15')
ans = com.write_parameter_to_device("D3", "50")
print(ans)

