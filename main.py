import time
import subprocess
from random import randrange

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
from primitives import GPIOButton


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


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
class Font:
    def __init__(self, size):
        self.size = size
        self.font = self.create_font(size)

    def create_font(self, size):
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)

    def inc_font(self):
        self.size += 1
        print("Recreating font, size=", self.size)
        self.font = self.create_font(self.size)

    def dec_font(self):
        self.size -= 1
        print("Recreating font, size=", self.size)
        self.font = self.create_font(self.size)


display = STT789Display()
font = Font(24)

buttonA = GPIOButton(board.D23, inverted=True, on_high_to_low=lambda: font.inc_font())
buttonB = GPIOButton(board.D24, inverted=True, on_high_to_low=lambda: font.dec_font())

display.set_backlight(True)


def start():
    def get_line(line):
        if line == 0:
            cmd = "hostname -I | cut -d' ' -f1"
            text = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#FFFFFF"
        elif line == 1:
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            text = subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#FFFF00"
        elif line == 2:
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
            text = subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#00FF00"
        elif line == 3:
            cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
            text = subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#0000FF"
        elif line == 4:
            cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"
            text = subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#FF00FF"
        else:
            text = "Line " + str(line)
            color = "#{:06x}".format(randrange(0x1000000))
        return text, color

    def print_text(text, color, font, ypos):
        display.draw.text((0, ypos), text, font=font.font, fill=color)

    while True:
        buttonA.update()
        buttonB.update()

        display.clear()

        ypos = display.top
        line = 0
        while ypos < display.bottom:
            text, color = get_line(line)
            text_height = font.font.getbbox(text[0])[3]
            if ypos+text_height > display.bottom:
                break
            print_text(text, color, font, ypos)
            ypos += text_height
            line += 1

        display.update()

        time.sleep(0.1)


start()
