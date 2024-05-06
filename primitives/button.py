from datetime import datetime
import RPi.GPIO as GPIO
import digitalio


class GPIOButton:
    def __init__(self, pin, is_input=True, inverted=False, initial=GPIO.LOW, on_low_to_high=None, on_high_to_low=None):
        if inverted:
            self.HIGH = GPIO.LOW
            self.LOW = GPIO.HIGH
        else:
            self.HIGH = GPIO.HIGH
            self.LOW = GPIO.LOW
        self.on_low_to_high = on_low_to_high
        self.on_high_to_low = on_high_to_low
        self.pin = digitalio.DigitalInOut(pin)
        if is_input:
            self.pin.switch_to_input()
        else:
            self.pin.switch_to_output()
            self.pin.value = initial
        self.last_update = datetime.now()
        self.value = self.pin.value

    def update(self):
        self.last_update = datetime.now()
        value = self.pin.value
        if self.value != value:
            self.value = value
            if value == self.HIGH:
                if self.on_low_to_high:
                    self.on_low_to_high()
            else:
                if self.on_high_to_low:
                    self.on_high_to_low()
        return self.value == self.HIGH
