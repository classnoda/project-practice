from machine import Pin, PWM
import micropython
from config import Config


class Motor:
    def __init__(self, freq : int=50000):
        self.bin2 = Pin(Config.BIN2, mode=Pin.OUT, pull=None)
        self.bin1 = Pin(Config.BIN1, mode=Pin.OUT, pull=None)
        self.ain2 = Pin(Config.AIN2, mode=Pin.OUT, pull=None)
        self.ain1 = Pin(Config.AIN1, mode=Pin.OUT, pull=None)
        self.stby = Pin(Config.STBY, mode=Pin.OUT, pull=None)
        self.a_pwm = PWM(Pin(Config.PWM_A), freq)
        self.b_pwm = PWM(Pin(Config.PWM_B), freq)

        self.a_offset = Config.offsetA
        self.b_offset = Config.offsetB

        self.a_pwm.duty(0)
        self.b_pwm.duty(0)
        self.stby.value(1)

    @micropython.native
    def __move(self, a : bool, b : bool):
        self.ain1.value(a)
        self.ain2.value(not a)

        self.bin1.value(b)
        self.bin2.value(not b)

    def forward(self):
        self.__move(self.a_offset, self.b_offset)

    def backward(self):
        self.__move(not self.a_offset, not self.b_offset)

    def right(self):
        self.__move(self.a_offset, not self.b_offset)

    def left(self):
        self.__move(not self.a_offset, self.b_offset)

    def set_speed(self, speed):
        self.a_pwm.duty(speed)
        self.b_pwm.duty(speed)

    def stop(self):
        self.ain1.value(0)
        self.ain2.value(0)

        self.bin1.value(0)
        self.bin2.value(0)

    def brake(self):
        self.ain1.value(1)
        self.ain2.value(1)

        self.bin1.value(1)
        self.bin2.value(1)

    @micropython.viper
    def sleep(self):
        self.stop()
        self.stby.value(0)

    @micropython.viper
    def wake_up(self):
        self.stby.value(1)

