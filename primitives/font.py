from PIL import ImageFont
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
