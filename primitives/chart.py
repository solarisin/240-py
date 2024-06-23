from PIL import Image, ImageDraw, ImageColor
import numpy as np
import time


def limit(
        values: list[int | float],
        minv: int | float,
        maxv: int | float,
        *,
        copy: bool = True
) -> np.ndarray:
    """
    Limit array to specific range.

    Attributes
    ----------
    values: `list[int | float]`
        List of values.
    minv: `int | float`
        Minimum (bottom) value.
    maxv: `int | float`
        Maximum (top) value.
    copy: `bool`
        Copy an array or not.
    """
    array = np.array(values, copy=copy)
    _min, _max = min(array), max(array)

    if _max == _min:
        return array

    m = (maxv - minv) / (_max - _min)
    b = maxv - m * _max

    return m * array + b


class Graph:
    def draw(self) -> Image.Image:
        """
        Draw the graph.
        """
        raise NotImplementedError()


class LineOptions:
    def __init__(self,
                 color: tuple | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
                 thickness: int = 1
                 ) -> None:
        if color is ...:
            # TODO random color
            color = ImageColor.getrgb('white')
        self.color = color
        self.thickness = thickness


class FillOptions:
    def __init__(self,
                 color: tuple | tuple[int, int, int] | tuple[int, int, int, int] | None = ...
                 ) -> None:
        if color is ...:
            # TODO random color
            color = ImageColor.getrgb('white')
        self.color = color
        # TODO fill direction


class PointOptions:
    def __init__(self,
                 color: tuple | tuple[int, int, int] | tuple[int, int, int, int] | None = ...,
                 radius: float = 0.5
                 ) -> None:
        if color is ...:
            # TODO random color
            color = ImageColor.getrgb('white')
        self.color = color
        self.radius = radius


class ScaleOptions:
    def __init__(self,
                 ) -> None:
        # TODO
        return


class LineChart:
    """Class representing a line chart."""

    def __init__(
            self,
            size: tuple[int, int],
            *,
            line_options: LineOptions = LineOptions(),
            point_options: PointOptions = PointOptions(),
            fill_options: FillOptions = None,
            max_length: int = None,
    ) -> None:
        self.size = size
        self.line_options = line_options
        self.fill_options = fill_options
        self.point_options = point_options
        self.data = []
        self.max_length = max_length

    @property
    def size(self) -> tuple[int, int]:
        """Image width and height."""
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        if isinstance(value, tuple):
            if len(value) != 2:
                raise ValueError("size should contain 2 items")
            self._size = value
        else:
            raise TypeError(f"size must be a tuple, not {type(value).__name__}")

    def append_data(self, value: int | float | tuple[float, float | int]):
        if isinstance(value, tuple):
            self.data.append(value)
        else:
            self.data.append((time.time(), value))
        if len(self.data) > self.max_length:
            self.data.pop(0)

    def draw(self) -> Image.Image:
        image = Image.new('RGBA', self.size)
        data_length = len(self.data)

        if data_length < 2:
            return image

        draw = ImageDraw.Draw(image)

        w, h = self.size
        thickness = self.line_options.thickness
        max_value = max((value for _, value in self.data))
        radius = self.point_options.radius

        lim_xs = limit(
            [w / (data_length - 1) * i for i in range(data_length)],
            radius,
            w - radius
        )

        if max_value == 0:
            lim_ys = [h - radius] * data_length
        else:
            lim_ys = limit(
                [max_value - value for _, value in self.data],
                radius,
                h - radius
            )

        source_p = list(zip(lim_xs, lim_ys))

        if self.fill_options:
            draw.polygon(
                [(radius, h)] + source_p + [(w - radius, h)],
                fill=self.fill_options.color,
                width=0
            )

        if self.line_options:
            draw.line(
                source_p,
                fill=self.line_options.color,
                width=thickness,
                joint='curve'
            )

        if self.point_options:
            for x, y in source_p:
                draw.ellipse(
                    (
                        (x - radius, y - radius),
                        (x + radius, y + radius)
                    ),
                    fill=self.point_options.color,
                    width=0
                )

        return image
