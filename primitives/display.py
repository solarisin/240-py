import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw, ImageFont


class Font:
    def __init__(self, size, font_path=None):
        self.size = size
        if font_path is not None:
            self.path = font_path
        else:
            self.path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        self.debug = False

        self.ft_font = self.create_font(size)

    def create_font(self, size):
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        return ImageFont.truetype(self.path, size)

    def font(self):
        return self.ft_font

    def get_height(self, text):
        return self.ft_font.getbbox(text)[3]

    def inc_font(self):
        self.size += 1
        if self.debug:
            print("Recreating font, size=", self.size)
        self.ft_font = self.create_font(self.size)

    def dec_font(self):
        self.size -= 1
        if self.debug:
            print("Recreating font, size=", self.size)
        self.ft_font = self.create_font(self.size)


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

        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        self.clear(True)

    def clear(self, update=False):
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        if update:
            self.update()

    def set_backlight(self, state):
        # Turn on the backlight
        self.backlight.value = state

    def update(self):
        self.disp.image(self.image, 90)
