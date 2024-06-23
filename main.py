import time
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
    data['chart'] = dict()
    data['chart']['length'] = 100
    data['adc'] = dict()
    data['render'] = dict()
    data['render']['elapsed'] = 0
    print('Starting render loop')
    x = 0
    while True:
        x += 1
        start = time.time()

        a_state = buttonA.update()
        b_state = buttonB.update()

        # press both buttons to exit
        if a_state and b_state:
            break

        # update all channel data and get display text
        for c in channels:
            c.update()
            if c.name not in data['adc']:
                data['adc'][c.name] = dict()
            data['adc'][c.name]['text'] = c.display_text()
            data['adc'][c.name]['value'] = c.scaled_value
            data['adc'][c.name]['value_avg'] = c.scaled_value_avg

        # renderer.draw_table(data)
        renderer.draw_graph("OilPress", data)
        data['render']['elapsed'] = int((time.time() - start)*1000)
        time.sleep(0.1)
        data['render']['total'] = int((time.time() - start) * 1000)
    print('Exiting render loop')
    display.clear(True)
    display.set_backlight(False)
