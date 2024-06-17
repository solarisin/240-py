import random
from PIL import Image, ImageDraw, ImageColor
import platform, sys
if 'arm' not in platform.processor():
    from deps.piligraphs.piligraphs import LineChart, Node, Interpolation
else:
    from piligraphs import LineChart, Node, Interpolation


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
        self.image = display.blank_image
        self.draw = ImageDraw.Draw(self.image)

    def _get_fps_text(self, data):
        render_ms = data['render']['elapsed']
        frame_ms = data['render']['total']
        if frame_ms == 0:
            frame_ms = 1
        if render_ms == 0:
            render_ms = 1
        fps = 1000 / frame_ms
        text = "FPS: {:.1f} ({} ms)".format(fps, render_ms)
        color = ImageColor.getrgb("white")
        return text, color

    def get_line(self, line_num, data: dict):
        if line_num == 0:
            return self._get_fps_text(data)

        adc_num = line_num - 1
        if 0 <= adc_num < len(data['adc']):
            text = data['adc'][list(data['adc'])[adc_num]]
            color = ImageColor.getrgb(self.line_colors[adc_num % len(self.line_colors)])
            return text, color

        return " ", ImageColor.getrgb("black")

    def draw_table(self, data):
        self.display.clear()

        y_pos = self.display.top
        line = 0
        while y_pos < self.display.bottom:
            text, color = self.get_line(line, data)
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

    def draw_graph(self, chan_name, data: dict) -> Image:
        if chan_name in data['adc']:
            # elements = list(data['adc'][chan_name])[-10:]

            nodes = [
                Node(weight=random.randint(1, 7)) for _ in range(10)
            ]

            # create a line chart
            chart = LineChart(
                size=self.display.size(),
                thickness=2,
                fill=(243, 14, 95, 156),
                outline=(194, 43, 132, 256),
                pwidth=6,
                onlysrc=True,
                npoints=len(nodes) * 8,
                interp='cubic'
            )

            # add nodes
            chart.add_nodes(*nodes)

            # draw the graph
            self.image = chart.draw()
            self.display.set_image(self.image, update=True)
        else:
            self.display.clear()
            self.draw.text((0, 0), "No data: {}".format(chan_name), font=self.font.font(), fill=ImageColor.getrgb('red'))
        self.display.update()
