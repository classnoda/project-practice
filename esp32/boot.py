import _thread
from machine import Pin
from modules.BLE_Controller import BLE_Controller
from modules.Motor import Motor
from modules.RfId import RfId
from modules.Servo import Servo
import neopixel


motor = Motor()

motor.set_speed(1023)
servo = Servo(23, 70)
servo2 = Servo(22, 175) # 90

rfid = RfId()

_thread.start_new_thread(rfid.loop, ())


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
    elif msg == b'1':
        servo.set_angle(10)
    elif msg == b'2':
        servo.set_angle(70)
    elif msg == b'3':
        servo2.set_angle(175)
    elif msg == b'4':
        servo2.set_angle(70)
    elif msg == b't':
        motor.set_speed(1023)
    elif msg == b'g':
        motor.set_speed(512)

ble_controller = BLE_Controller('esp32-123', handler)



