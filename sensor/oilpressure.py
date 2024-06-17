from sensor.generic import GenericChannel


class OilPressureChannel(GenericChannel):
    def __init__(self, name, analog_in, unit="psi"):
        super().__init__(name, analog_in, unit)

    def update(self):
        super().update()
        # sensor is 0psi (atmospheric at 0.5V) to 150psi (4.5V)
        self.scaled_value = (self.voltage-0.504) * 37.5

    def display_text(self):
        return "{}:\n {:.2f}psi\n {:.3f}V".format(self.name, self.scaled_value, self.voltage)
