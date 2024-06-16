import time


class GenericChannel:
    def __init__(self, name, analog_in, unit="V"):
        self.name = name
        self.analog_in = analog_in
        self.unit = unit
        self.value = None
        self.voltage = None
        self.scaled_value = None
        self.last_update = None

    def update(self):
        self.value = self.analog_in.value
        self.voltage = self.analog_in.voltage
        self.scaled_value = self.analog_in.voltage
        self.last_update = time.time()

    def display_text(self):
        return "{: .3f}V ({:>10} FS)".format(self.scaled_value, self.value)


class NullChannel(GenericChannel):
    def __init__(self, name, analog_in):
        super().__init__(name, analog_in)

    def update(self):
        self.value = None
        self.scaled_value = None
        self.last_update = None

    def display_text(self):
        return None
