from machine import Pin
from neopixel import NeoPixel
from config import Config

class Led:
    def __init__(self):
        self.np = NeoPixel(Pin(Config.LED_PIN), 1)

    def set(self, rgb):
        self.np[0] = rgb
        self.np.write()

    def handler(self, colour = ''):
        if colour == 'violet':
            self.set((255, 0, 255))
        elif colour == 'white':
            self.set((255, 255, 255))
        elif colour == 'red':
            self.set((255, 0, 0))
        elif colour == 'black':
            self.set((0, 0, 0))
        elif colour == 'yellow':
            self.set((255, 255, 0))
        elif colour == 'green':
            self.set((0, 255, 0))
        elif colour == 'blue':
            self.set((0, 0, 255))
        elif colour == 'orange':
            self.set((255, 165, 0))
        elif colour == 'pink':
            self.set((255, 192, 203))
        elif colour == 'purple':
            self.set((148, 0, 211))
        elif colour == 'brown':
            self.set((165, 42, 42))
        elif colour == 'grey':
            self.set((128, 128, 128))
        else:
            self.set((10, 10, 10))

