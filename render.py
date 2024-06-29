import random
import time
import numpy as np
from PIL import Image, ImageDraw, ImageColor
from primitives import LineChart
import math


class Renderer:
    line_colors = [
        "yellow",
        "orange",
        "blue",
        "purple",
        "red",
        "green",
        "black",
        "white",
    ]

    def __init__(self, display, font):
        self.display = display
        self.font = font
        self.image = Image.new("RGBA",  display.size(), ImageColor.getrgb("red"))
        self.chart = None

        # timing
        self.render_start = None
        self.frame_start = None

    def draw(self):
        return ImageDraw.Draw(self.image, "RGBA")

    def draw_table(self, data):
        def get_line(self, line_num, data: dict):
            def _get_fps_text(dict_data):
                render_ms = dict_data['render']['elapsed']
                frame_ms = dict_data['render']['total']
                if frame_ms == 0:
                    frame_ms = 1
                if render_ms == 0:
                    render_ms = 1
                fps = 1000 / frame_ms
                fps_text = "FPS: {:.1f} ({} ms)".format(fps, render_ms)
                fps_color = ImageColor.getrgb("white")
                return fps_text, fps_color

            if line_num == 0:
                return _get_fps_text(data)

            adc_num = line_num - 1
            if 0 <= adc_num < len(data['adc']):
                text = data['adc'][list(data['adc'])[adc_num]]['text']
                color = ImageColor.getrgb(self.line_colors[adc_num % len(self.line_colors)])
                return text, color

            return " ", ImageColor.getrgb("black")

        y_pos = self.display.top()
        line = 0
        while y_pos < self.display.bottom:
            text, color = get_line(line, data)
            if not text:
                line += 1
                continue
            text_height = self.font.get_height(text[0] or ' ')
            if text_height == 0:
                line += 1
                continue
            if y_pos + text_height > self.display.bottom:
                break
            self.display.draw_text((0, y_pos), text, color)
            y_pos += text_height
            line += 1
        print("Rendered {} lines".format(line))
        self.display.update()

    def draw_graph(self, size, chan_name, data: dict) -> Image:
        if chan_name in data['adc']:
            # elements = list(data['adc'][chan_name])[-10:]

            # create a line chart if not created already
            if self.chart is None:
                chart_length = data['chart']['length']
                self.chart = LineChart(
                    size=size,
                    max_length=chart_length
                )

            # append value
            value = data['adc'][chan_name]['value_avg']
            if value is None or value is math.nan:
                return
            self.chart.append_data(value)

            # draw the graph
            return self.chart.draw()
        else:

            return None

    def bounds_test(self, data):
        def clear():
            self.draw().rectangle(self.display.bounds(), fill="black")

        print("> Elapsed: {} ms - Total: {} ms".format(data['render']['elapsed'], data['render']['total']))
        # draws a 1px rectangle around the outer bounds of the display that can be seen
        clear()
        self.draw().rectangle(
            self.display.bounds(),
            outline="yellow",
            width=1,
            fill=None)
        self.display.set_image(self.image, update=True)

    def start(self, data: dict):
        def clear():
            self.draw().rectangle(self.display.bounds(), fill="black")

        def update_inputs(dict_data):
            # update button states
            button_a, button_b = dict_data['buttons']
            dict_data['button_states'] = [button_a.update(), button_b.update()]

        def update_adc(dict_data):
            # update all channel data and store display text
            channels = data['channels']
            for c in channels:
                c.update()
                if c.name not in data['adc']:
                    data['adc'][c.name] = dict()
                data['adc'][c.name]['text'] = c.display_text()
                data['adc'][c.name]['value'] = c.scaled_value
                data['adc'][c.name]['value_avg'] = c.scaled_value_avg

        def check_exit(dict_data):
            # check if exit condition is met, press both buttons to exit
            a_state, b_state = dict_data['button_states']
            return a_state and b_state

        print('Starting render loop')
        self.render_start = time.time()
        while True:
            frame_start = time.time()

            update_inputs(data)
            if check_exit(data):
                break

            update_adc(data)

            # draw the image for this frame
            chart_size = (self.display.width(), self.display.height()-30)
            chart_image = self.draw_graph(chart_size, "OilPress", data)
            if chart_image is not None:
                clear()
                self.image.paste(chart_image, (self.display.left(), self.display.top()+28))
                # draw a box in the top right corner
                txt = data['adc']['OilPress']['text']
                self.draw().text([self.display.left()+35, self.display.top()], font=self.font.font(), text=txt)
                self.display.set_image(self.image, update=True)

            # self.draw_table(data)
            # self.bounds_test(data)

            elapsed_sec = time.time() - frame_start
            data['render']['elapsed'] = int(elapsed_sec * 1000)
            time.sleep(max(0.1 - elapsed_sec, 0.01))
            data['render']['total'] = int((time.time() - frame_start) * 1000)

        print('Exiting render loop')
