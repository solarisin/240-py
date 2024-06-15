import time
import subprocess
from random import randrange

import board
from primitives import GPIOButton, STT789Display, Font


def read_adc():
    adc_data = [
        {'name': 'ADC0', 'value': 1.0},
        {'name': 'ADC1', 'value': 2.3242}
    ]
    return adc_data


def render_text(data):
    line_colors = [
        "#FF0000",
        "#00FF00",
        "#0000FF",
        "#FFFF00",
        "#FF00FF",
        "#00FFFF",
        "#FFFFFF",
        "#000000",
    ]
    
    def get_fps_text(data):
        frame_ms = data['render']['elapsed']
        if frame_ms == 0:
            frame_ms = 1
        fps = 1000 / frame_ms
        text = "FPS: {} ({} ms)".format(str(round(fps, 1)), str(frame_ms))
        color = "#F000FF"
        return text, color

    def stats_get_line(line_num, data):
        if line_num == 0:
            cmd = "hostname -I | cut -d' ' -f1"
            text = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
            color = "#FFFFFF"
        elif line_num == 1:
            # note: this can take ~150ms to execute
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
        elif line_num == 5:
            text, color = get_fps_text(data)
        else:
            text = "Line " + str(line_num)
            color = "#{:06x}".format(randrange(0x1000000))
        return text, color

    def adc_get_line(line_num, data):
        if line_num == 0:
            return get_fps_text(data)

        adc_num = line_num-1
        if 0 <= adc_num < len(data['adc']):
            adc_data = data['adc'][adc_num]
            text = "{}: {}".format(adc_data['name'], round(adc_data['value'], 3))
            color = line_colors[adc_num % 8]
            return text, color

        return " ", "#FF0000"

    def get_line(type, line_num, data):
        if type == 'stats':
            return stats_get_line(line_num, data)
        elif type == 'adc':
            return adc_get_line(line_num, data)
        else:
            return " ", "#FF0000"


    def print_text(text, color, font, ypos):
        display.draw.text((0, ypos), text, font=font.font(), fill=color)

    y_pos = display.top
    line = 0
    while y_pos < display.bottom:
        text, color = get_line('adc', line, data)
        text_height = font.get_height(text[0])
        if y_pos + text_height > display.bottom:
            break
        print_text(text, color, font, y_pos)
        y_pos += text_height
        line += 1


def render(data):
    display.clear()
    render_text(data)
    display.update()


if __name__ == "__main__":
    display = STT789Display()
    font = Font(24)
    buttonA = GPIOButton(board.D23, inverted=True, on_high_to_low=lambda: font.inc_font())
    buttonB = GPIOButton(board.D24, inverted=True, on_high_to_low=lambda: font.dec_font())
    display.set_backlight(True)

    data = dict()
    data['render'] = dict()
    data['render']['elapsed'] = 0
    while True:
        start = time.time()
        buttonA.update()
        buttonB.update()

        data['adc'] = read_adc()

        render(data)
        data['render']['elapsed'] = int((time.time() - start)*1000)
        time.sleep(0.1)
