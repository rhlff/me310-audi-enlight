import copy
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
        self.animations = {}
        self.symbol_lock = threading.Lock()

    def run(self):
        while not self.stopped:
            self.symbol_lock.acquire()
            self.symbols[:] = [s for s in self.symbols if not s.dead]
            self.symbol_lock.release()
            now = datetime.now()
            pixels = self.world.draw(self.symbols, now)
            self.client.put_pixels(pixels)
            time.sleep(0.01)

    def stop(self):
        [a.stop() for k, a in self.animations.items()]
        self.stopped = True
        self.off()

    def off(self):
        self.client.put_pixels([(0, 0, 0,)] * self.world.led_count)

    def add_symbol(self, symbol):
        self.symbol_lock.acquire()
        symbol.dead = False
        self.symbols.append(symbol)
        self.symbol_lock.release()

    def remove_symbol(self, symbol):
        symbol.dead = True

    def add_animation(self, symbol, animaton_type, end_value, duration):
        animations = symbol.animations()
        if animaton_type not in animations:
            print "Failed to animate %s of symbol %s" % (animaton_type, symbol)
        else:
            start_value, animation_func = animations[animaton_type]
            key = (symbol, animation_func)

            if key in self.animations:
                # stop old animation
                self.animations[key].stop()

            animation = SymbolAnimation(copy.copy(start_value), end_value, duration,
                                        animation_func)
            self.animations[key] = animation
            animation.start()


class SymbolAnimation(threading.Thread):
    def __init__(self, start_value, end_value, duration, animation_func):
        super(SymbolAnimation, self).__init__()
        self.start_time = datetime.now()
        self.duration = duration
        self.start_value = start_value
        self.end_value = end_value
        self.animation_func = animation_func
        self.stopped = False

    def run(self):
        self.start_time = datetime.now()
        _current_life_time = self._current_life_time()
        while _current_life_time <= self.duration and not self.stopped:
            self.animation_func(self.start_value, self.end_value,
                                _current_life_time, self.duration)
            time.sleep(0.01)
            _current_life_time = self._current_life_time()

    def stop(self):
        self.stopped = True

    def _current_life_time(self):
        return (datetime.now()-self.start_time).total_seconds()
