#!/usr/bin/env python3
"""
137 Hz Field Generator
Room-Temp Superconductor RT-287
License: CC0
"""

import time
import math
from typing import Tuple

try:
    import RPi.GPIO as GPIO
    _HAS_GPIO = True
except ImportError:
    _HAS_GPIO = False

# ========= CONFIG =========
FREQ_HZ   = 137.0          # Prime resonance
DUTY      = 0.5            # 50 % square wave
AMPLITUDE = 3.3            # Volts (3.3 V for Pi GPIO)
PIN       = 18             # BCM pin 18 (hardware PWM on Pi)

# ========= DRIVER =========
class FieldGenerator:
    """Generates 137 Hz square wave with precise timing."""
    def __init__(self, freq=FREQ_HZ, duty=DUTY, amplitude=AMPLITUDE):
        self.freq = freq
        self.period = 1.0 / freq
        self.high = self.period * duty
        self.low  = self.period * (1 - duty)
        self.amplitude = amplitude
        self._setup_gpio()

    def _setup_gpio(self):
        if _HAS_GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(PIN, GPIO.OUT)
            self.pwm = GPIO.PWM(PIN, int(freq))
            self.pwm.start(50)  # 50 % duty
        else:
            print("[INFO] No GPIO - running simulation mode")

    def start(self):
        if _HAS_GPIO:
            self.pwm.ChangeFrequency(self.freq)
            print(f"137 Hz field active on pin {PIN}")
        else:
            self._simulate()

    def _simulate(self):
        """Console-based simulation for testing on any OS."""
        print(f"Simulating {self.freq} Hz square wave...")
        while True:
            print("HIGH", end=" ")
            time.sleep(self.high)
            print("LOW",  end=" ")
            time.sleep(self.low)

    def stop(self):
        if _HAS_GPIO:
            self.pwm.stop()
            GPIO.cleanup()
        print("Field generator stopped.")

# ========= CLI =========
if __name__ == "__main__":
    gen = FieldGenerator()
    try:
        gen.start()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        gen.stop()
