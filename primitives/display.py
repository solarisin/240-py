import board
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageColor


class Padding:
    def __init__(self, top: int, right: int, bottom: int, left: int):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


class PILDisplay:
    def __init__(self, width: int, height: int, rotation: int, padding: int | tuple[int, int] | tuple[int, int, int, int] | Padding):
        self._width = width
        self._height = height
        self.rotation = rotation

        # padding describes the space between the edge of the display and the content
        self.padding = None
        self.set_padding(padding)

        self.current_image = Image.new("RGBA", self.size(), ImageColor.getrgb("black"))

    def set_padding(self, padding: int | tuple[int, int] | tuple[int, int, int, int]):
        if isinstance(padding, int):
            self.padding = Padding(padding, padding, padding, padding)
        elif isinstance(padding, tuple):
            if len(padding) == 2:
                self.padding = Padding(padding[0], padding[1], padding[0], padding[1])
            elif len(padding) == 4:
                self.padding = Padding(padding[0], padding[1], padding[2], padding[3])
        elif isinstance(padding, Padding):
            self.padding = padding
        else:
            raise ValueError("Invalid padding value: must be int, tuple of 2 ints, tuple of 4 ints, or Padding object.")

    def size(self):
        # For some reason, the display is rotated 90 degrees, so we need to swap width and height
        # apply rotation to width and height
        if self.rotation in [0, 180]:
            return self._width, self._height
        else:
            return self._height, self._width

    def top(self):
        return self.padding.top

    def bottom(self):
        return self.height() - self.padding.bottom

    def left(self):
        return self.padding.left

    def right(self):
        return self.width() - self.padding.right

    def width(self):
        return self.size()[0]

    def height(self):
        return self.size()[1]

    def bounds(self, adjust: int | tuple[int, int] | tuple[int, int, int, int] = 0):
        x0 = x0a = self.left()
        x1 = x1a = self.right()
        y0 = y0a = self.top()
        y1 = y1a = self.bottom()
        if isinstance(adjust, int):
            x0a = x0 + adjust
            x1a = x1 - adjust
            y0a = y0 + adjust
            y1a = y1 - adjust
        elif isinstance(adjust, tuple):
            if len(adjust) == 2:
                x0a = x0 + adjust[0]
                x1a = x1 - adjust[0]
                y0a = y0 + adjust[1]
                y1a = y1 - adjust[1]
            elif len(adjust) == 4:
                x0a = x0 + adjust[0]
                x1a = x1 - adjust[1]
                y0a = y0 + adjust[2]
                y1a = y1 - adjust[3]

        x0a, x1a = min(x0a, x1a), max(x0a, x1a)
        y0a, y1a = min(y0a, y1a), max(y0a, y1a)
        return [(x0a, y0a), (x1a, y1a)]

    def set_image(self, image, update=False):
        self.current_image = image
        if update:
            self.update()

    def get_image(self):
        return self.current_image

    def update(self):
        raise NotImplementedError

    def set_backlight(self, state):
        raise NotImplementedError


class STT789Display(PILDisplay):
    def __init__(self):

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()

        # Create the ST7789 display:
        self.stt789 = st7789.ST7789(
            spi,
            cs=digitalio.DigitalInOut(board.CE0),
            dc=digitalio.DigitalInOut(board.D25),
            rst=None,
            baudrate=64000000,
            width=135,
            height=240,
            x_offset=53,
        # todo determine if x_offset/y_offset is necessary for a simulated display or if it specific to the hardware
            y_offset=40,
        )

        self.backlight = digitalio.DigitalInOut(board.D22)
        self.backlight.switch_to_output()

        super().__init__(self.stt789.width, self.stt789.height, 90, Padding(left=0, top=0, right=1, bottom=1))

    def update(self):
        self.stt789.image(self.get_image(), self.rotation)

    def set_backlight(self, state):
        # Turn on the backlight
        self.backlight.value = state
