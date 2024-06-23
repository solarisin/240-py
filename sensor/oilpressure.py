from sensor.generic import GenericChannel
import math
import numpy as np


class OilPressureChannel(GenericChannel):
    def __init__(self, name, analog_in, unit="psi"):
        super().__init__(name, analog_in, unit)

    def update(self):
        super().update()
        # sensor is 0psi (atmospheric at 0.5V) to 150psi (4.5V)
        self.scaled_value = (self.voltage-0.5040153813287759) * 37.5
        self.history.appendleft(self.scaled_value)
        if math.nan in self.history:
            adj_history = [x for x in list(self.history) if x is not math.nan]
            self.scaled_value_avg = np.sum(adj_history) / len(adj_history)
        else:
            self.scaled_value_avg = np.sum(self.history) / len(self.history)

    def display_text(self):
        return "{}:\n {:.2f}psi\n {:.3f}V".format(self.name, self.scaled_value, self.voltage)
