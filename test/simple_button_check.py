import time
from primitives import GPIOButton
import board


buttonA = GPIOButton(board.D23, inverted=True,
                 on_low_to_high=lambda: print("Button A pressed!"),
                 on_high_to_low=lambda: print("Button A released!"))
buttonB = GPIOButton(board.D24, inverted=True,
                 on_low_to_high=lambda: print("Button B pressed!"),
                 on_high_to_low=lambda: print("Button B released!"))

while True:
    buttonA.update()
    buttonB.update()
    time.sleep(0.01)
