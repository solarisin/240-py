import time
import subprocess
from random import randrange

import board
from primitives import GPIOButton
from display import STT789Display, Font


def start():
    def get_line(line_num):
        if line_num == 0:
            cmd = "hostname -I | cut -d' ' -f1"
            text = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#FFFFFF"
        elif line_num == 1:
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            text = subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#FFFF00"
        elif line_num == 2:
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
            text = subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#00FF00"
        elif line_num == 3:
            cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
            text = subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#0000FF"
        elif line_num == 4:
            cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"
            text = subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#FF00FF"
        else:
            text = "Line " + str(line_num)
            color = "#{:06x}".format(randrange(0x1000000))
        return text, color

    def print_text(text, color, font, ypos):
        display.draw.text((0, ypos), text, font=font.font, fill=color)

    while True:
        buttonA.update()
        buttonB.update()

        display.clear()

        y_pos = display.top
        line = 0
        while y_pos < display.bottom:
            text, color = get_line(line)
            text_height = font.get_height(text[0])
            if y_pos+text_height > display.bottom:
                break
            print_text(text, color, font, y_pos)
            y_pos += text_height
            line += 1

        display.update()

        time.sleep(0.1)


if __name__ == "__main__":
    display = STT789Display()
    font = Font(24)
    buttonA = GPIOButton(board.D23, inverted=True, on_high_to_low=lambda: font.inc_font())
    buttonB = GPIOButton(board.D24, inverted=True, on_high_to_low=lambda: font.dec_font())
    display.set_backlight(True)
    start()
