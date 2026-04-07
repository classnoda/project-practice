from config import *
from modules.BLE_Controller import BLE_Controller
from modules.Motor import Motor

motor = Motor(Config)

motor.set_speed(1023)

def handler(msg):
    if msg == b'w':
        motor.forward()
    elif msg == b'a':
        motor.left()
    elif msg == b's':
        motor.backward()
    elif msg == b'd':
        motor.right()
    elif msg == b'e':
        motor.stop()
    elif msg == b'r':
        motor.brake()


ble_controller = BLE_Controller('esp32-123', handler)



