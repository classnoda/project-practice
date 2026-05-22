from machine import PWM


class Servo:
    def __init__(self, servo_pin, zero_position):
        self.p = PWM(servo_pin, freq=50)
        self.angle = zero_position
        self.move()

    def set_angle(self, angle):
        self.angle = angle
        self.move()


    def change_angle(self, sub_angle):
        if sub_angle + self.angle > 180:
            self.angle = 180
        if sub_angle + self.angle < 0:
            self.angle = 0
        else:
            self.angle += sub_angle

        self.move()

    def move(self):
        self.p.duty(int(((self.angle / 180) * (123 - 26)) + 26))

