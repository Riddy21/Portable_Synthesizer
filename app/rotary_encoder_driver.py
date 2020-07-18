
from time import sleep, time
import random


class Driver(object):
    def __init__(self, counter, scalar=True, factor=1):
        self.counter = counter
        self.scalar = scalar
        self.factor = factor

    def set_factor(self, factor):
        self.factor = factor

    def set_scalar(self, scalar):
        self.scalar = scalar

    def reset_counter(self, counter=None):
        if counter is None:
            counter = [0, 0, 0, 0]
        self.counter = counter

    def start_mac_tester(self):
        while True:
            sleep(1)
            for i in range(4):
                self.counter[i] = random.randint(0, 30)

    def start_driver(self):
        import RPi.GPIO as GPIO
        clk = [40, 36, 37, 33]
        dt = [38, 32, 35, 31]
        clkLastState = [False] * 4

        GPIO.setmode(GPIO.BOARD)
        for i in range(4):
            GPIO.setup(clk[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(dt[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            clkLastState[i] = GPIO.input(clk[i])

        double = True
        clkState = [False] * 4
        dtState = [False] * 4

        try:
            end = time()
            while True:
                for i in range(4):
                    clkState[i] = GPIO.input(clk[i])
                    dtState[i] = GPIO.input(dt[i])

                    if clkState[i] != clkLastState[i]:
                        if double:
                            start = end
                            end = time()
                            if dtState[i] != clkState[i]:
                                if not self.scalar:
                                    self.counter[i] += self.factor * 1 / (100 * (end - start))
                                else:
                                    self.counter[i] += 1
                            else:
                                if not self.scalar:
                                    self.counter[i] -= self.factor * 1 / (100 * (end - start))
                                else:
                                    self.counter[i] -= 1

                            double = False
                        else:
                            double = True
                    clkLastState[i] = clkState[i]
                    sleep(0.002)

        finally:
            GPIO.cleanup()
