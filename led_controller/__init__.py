import threading
import time
from datetime import datetime


class LEDController(threading.Thread):
    def __init__(self, world, client):
        super(LEDController, self).__init__()
        self.world = world
        self.client = client
        self.stopped = False
        self.symbols = []

    def run(self):
        while not self.stopped:
            self.symbols[:] = [s for s in self.symbols if not s.dead]
            now = datetime.now()
            pixels = self.world.draw(self.symbols, now)
            self.client.put_pixels(pixels)
            time.sleep(0.01)

    def stop(self):
        self.stopped = True
        self.off()

    def off(self):
        self.client.put_pixels([(0, 0, 0,)] * self.world.led_count)

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def remove_symbol(self, symbol):
        symbol.dead = True
