import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)
from primitives import GPIOButton, STT789Display, Font
from sensor.generic import NullChannel, GenericChannel
from sensor.oilpressure import OilPressureChannel
from render import Renderer


if __name__ == "__main__":
    display = STT789Display()
    font = Font(24)
    buttonA = GPIOButton(board.D23, inverted=True, on_high_to_low=lambda: font.inc_font())
    buttonB = GPIOButton(board.D24, inverted=True, on_high_to_low=lambda: font.dec_font())
    display.set_backlight(True)
    renderer = Renderer(display, font)

    channels = [
        NullChannel("A0", AnalogIn(ads, ADS.P0)),
        NullChannel("A1", AnalogIn(ads, ADS.P1)),
        NullChannel("A2", AnalogIn(ads, ADS.P2)),
        OilPressureChannel("OilPress", AnalogIn(ads, ADS.P3))
    ]

    data = dict()

    data['channels'] = channels
    data['buttons'] = [buttonA, buttonB]

    data['chart'] = dict()
    data['chart']['length'] = 100

    data['adc'] = dict()

    data['render'] = dict()
    data['render']['elapsed'] = 0
    data['render']['total'] = 0

    # start blocking render loop
    renderer.start(data)

    display.clear(True)
    display.set_backlight(False)
