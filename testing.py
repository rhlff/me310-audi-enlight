from led_controller.led_objects import *
from led_controller.led_world import LEDWorldBuilder, ObjectLocation

import curses
import threading
import time

import opc

FC_SERVER = '172.16.20.233:7890'
# FC_SERVER = '192.168.2.1:7890'
client = opc.Client(FC_SERVER)

START_ANGLE = 40

class curses_screen:
    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(1)
        SCREEN_HEIGHT, SCREEN_WIDTH = self.stdscr.getmaxyx()
        return self.stdscr
    def __exit__(self,a,b,c):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

class TestingMode(threading.Thread):
    def __init__(self, client):
        super(TestingMode, self).__init__()
        builder = LEDWorldBuilder()
        builder.add_led_strip(0,   60, -0.5, 0.5, 0.5, 0.5, 1.0/60 * -1)
        builder.add_led_strip(60,  60, -0.5, 0.5, 0.5, 0.5, 1.0/60 *  0)
        builder.add_led_strip(120, 60, -0.5, 0.5, 0.5, 0.5, 1.0/60 *  1)
        self.world = builder.build()
        self.client = client
        self.stopped = False
        self.symbols = []

    def run(self):
        while not self.stopped:
            now = datetime.now()
            pixels = self.world.draw(self.symbols, now)
            self.client.put_pixels(pixels)
            self.symbols[:] = [s for s in self.symbols if not s.dead]
            time.sleep(0.02)

    def stop(self):
        self.stopped = True
        self.off()


    def create(self):
        pass

    def move(self, angle):
        pass

    def off(self):
        self.client.put_pixels([(0, 0, 0,)] * self.world.led_count)

class BaseTestingMode(TestingMode):
    def __init__(self, client):
        super(BaseTestingMode, self).__init__(client)
        self.spot = None

    def create(self):
        color = (255, 255, 255)
        location = ObjectLocation(START_ANGLE, 1.414213562)
        self.spot = LEDSpot(color, 0, location, 1.0/60 * 20)
        self.symbols.append(self.spot)

    def move(self, angle):
        if self.spot:
            self.spot.location.angle += angle

class TestingMode1(BaseTestingMode):
    def create(self):
        color = (255, 0, 0)
        location = ObjectLocation(START_ANGLE, 1.414213562)
        led_drop = LEDDrop(color, 0, location, 1.0/60 * 10 * 1.4, 0.05)
        self.symbols.append(led_drop)
        time.sleep(0.1)
        color = (128, 255, 128)
        self.spot = LEDSpot(color, 0, location, 1.0/60 * 20)
        self.symbols.append(self.spot)

class TestingMode2(BaseTestingMode):
    def create(self):
        color = (200, 200, 200)
        location = ObjectLocation(START_ANGLE, 1.414213562)
        led_drop = LEDDrop(color, 0, location, 1.0/60 * 10 * 1.4, 0.05)
        self.symbols.append(led_drop)
        time.sleep(0.1)
        color = (255, 255, 255)
        self.spot = LEDSpot(color, 0, location, 1.0/60 * 20)
        self.symbols.append(self.spot)

class TestingMode3(BaseTestingMode):
    def create(self):
        color = (255, 0, 0)
        location = ObjectLocation(START_ANGLE, 1.414213562)
        led_drop = LEDDrop(color, 0, location, 1.0/60 * 10 * 2.0, 0.05)
        self.symbols.append(led_drop)
        time.sleep(0.1)
        color = (128, 255, 128)
        self.spot = LEDSpot(color, 0, location, 1.0/60 * 20 * 1.5)
        self.symbols.append(self.spot)

class TestingMode4(TestingMode):
    def __init__(self, client):
        super(TestingMode4, self).__init__(client)
        color = (255, 0, 0)
        self.puls = LEDAllPulsing(color, 0, 0.1)

    def create(self):
        if self.puls in self.symbols:
            self.symbols.remove(self.puls)
        else:
            self.symbols.append(self.puls)

class TestingMode5(BaseTestingMode):
    def create(self):
        color = (128, 255, 128)
        location = ObjectLocation(START_ANGLE, 1.414213562)
        self.spot = LECContinuousDrop(color, 0, location, 1.0/60 * 10 * 2.0, 1.0, 0.25, 0.01)
        self.symbols.append(self.spot)


def main():
    with curses_screen() as stdscr:
        mode = TestingMode(client)
        stdscr.addstr(0, 0, "Choose Mode [0-5]")
        while 1:
            c = stdscr.getch()
            if c == ord('1'):
                mode.stop()
                stdscr.addstr(0, 0, "Mode 1           ")
                mode = TestingMode1(client)
                mode.start()
            elif c == ord('0'):
                mode.stop()
                stdscr.addstr(0, 0, "Mode 0           ")
                mode = BaseTestingMode(client)
                mode.start()
            elif c == ord('2'):
                mode.stop()
                stdscr.addstr(0, 0, "Mode 2           ")
                mode = TestingMode2(client)
                mode.start()
            elif c == ord('3'):
                mode.stop()
                stdscr.addstr(0, 0, "Mode 3           ")
                mode = TestingMode3(client)
                mode.start()
            elif c == ord('4'):
                mode.stop()
                stdscr.addstr(0, 0, "Mode 4           ")
                mode = TestingMode4(client)
                mode.start()
            elif c == ord('5'):
                mode.stop()
                stdscr.addstr(0, 0, "Mode 5           ")
                mode = TestingMode5(client)
                mode.start()
            elif c == ord('q'):
                mode.stop()
                break  # Exit
            elif c == curses.KEY_LEFT:
                mode.move(1.5)
                stdscr.addstr(0, 0, "Mode 1       LEFT")
            elif c == curses.KEY_RIGHT:
                mode.move(-1.5)
                stdscr.addstr(0, 0, "Mode 1      RIGHT")
            elif c == ord(' '):
                mode.create()
                stdscr.addstr(0, 0, "Mode 1     CREATE")
            stdscr.refresh()


if __name__ == '__main__':
    main()
