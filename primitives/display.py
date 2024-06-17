import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageColor


class STT789Display:
    def __init__(self):
        # Setup SPI bus using hardware SPI:
        spi = board.SPI()

        # Create the ST7789 display:
        self.disp = st7789.ST7789(
            spi,
            cs=digitalio.DigitalInOut(board.CE0),
            dc=digitalio.DigitalInOut(board.D25),
            rst=None,
            baudrate=64000000,
            width=135,
            height=240,
            x_offset=53,
            y_offset=40,
        )

        self.backlight = digitalio.DigitalInOut(board.D22)
        self.backlight.switch_to_output()

        padding = -2
        self.height = self.disp.width
        self.width = self.disp.height
        self.top = padding
        self.bottom = self.height - padding

        self.blank_image = Image.new("RGB", (self.width, self.height), ImageColor.getrgb("black"))
        self.current_image = self.blank_image
        self.update()

    def clear(self, update=False):
        # Draw a black filled box to clear the image.
        # self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.image = self.blank_image
        if update:
            self.update()

    def set_backlight(self, state):
        # Turn on the backlight
        self.backlight.value = state

    def set_image(self, image, update=False):
        self.current_image = image
        if update:
            self.update()

    def get_image(self):
        return self.current_image

    def update(self):
        self.disp.image(self.current_image, 90)

    def size(self):
        return self.width, self.height