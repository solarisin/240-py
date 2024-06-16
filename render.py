import subprocess
from random import randrange


    # def stats_get_line(line_num, data):
    #     if line_num == 0:
    #         cmd = "hostname -I | cut -d' ' -f1"
    #         text = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    #         color = "#FFFFFF"
    #     elif line_num == 1:
    #         # note: this can take ~150ms to execute
    #         cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    #         text = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #         color = "#FFFF00"
    #     elif line_num == 2:
    #         cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    #         text = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #         color = "#00FF00"
    #     elif line_num == 3:
    #         cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    #         text = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #         color = "#0000FF"
    #     elif line_num == 4:
    #         cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"
    #         text = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #         color = "#FF00FF"
    #     elif line_num == 5:
    #         text, color = get_fps_text(data)
    #     else:
    #         text = "Line " + str(line_num)
    #         color = "#{:06x}".format(randrange(0x1000000))
    #     return text, color

class LineRenderer:
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

    def _get_fps_text(self, data):
        frame_ms = data['render']['elapsed']
        if frame_ms == 0:
            frame_ms = 1
        fps = 1000 / frame_ms
        text = "FPS: {:.1f} ({} ms)".format(fps, frame_ms)
        color = "#F000FF"
        return text, color

    def get_line(self, line_num, data: dict):
        if line_num == 0:
            return self._get_fps_text(data)

        adc_num = line_num - 1
        if 0 <= adc_num < len(data['adc']):
            text = data['adc'][list(data['adc'])[adc_num]]
            color = self.line_colors[adc_num % len(self.line_colors)]
            return text, color

        return " ", "#FF0000"


class Renderer:
    def __init__(self, display, font):
        self.display = display
        self.font = font
        self.line_renderer = LineRenderer()

    def draw(self, data):
        self.display.clear()

        y_pos = self.display.top
        line = 0
        while y_pos < self.display.bottom:
            text, color = self.line_renderer.get_line(line, data)
            if not text:
                line += 1
                continue
            text_height = self.font.get_height(text[0] or ' ')
            if text_height == 0:
                line += 1
                continue
            if y_pos + text_height > self.display.bottom:
                break
            self.display.draw.text((0, y_pos), text, font=self.font.font(), fill=color)
            y_pos += text_height
            line += 1

        self.display.update()
