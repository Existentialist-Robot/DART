import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
            
options = RGBMatrixOptions()
options.rows = 64
options.rows = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit->

matrix = RGBMatrix(options = options)

def display_frames(directory, frame_delay):
    frame_count = 1
    while True:
        try:
            print("debug 1")

            
            frame_number = str(frame_count).zfill(3)
            image_path = f"{directory}/{frame_number}.ppm"
            print(image_path)
            print("debug 2")

            image = Image.open(image_path)
            print(image.size)

            image.thumbnail((matrix.rows, matrix.height), Image.ANTIALIAS)

            matrix.SetImage(image.convert('RGB'))

            time.sleep(frame_delay)
            frame_count += 1
        except FileNotFoundError:
            break

print("debug")

display_frames("./frames2", 0.1)
