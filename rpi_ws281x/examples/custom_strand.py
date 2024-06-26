#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import os
import time
from rpi_ws281x import PixelStrip, Color
import argparse
from PIL import Image


# LED strip configuration:
LED_COUNT = 201        # Number of LED pixels.
# LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

parent_folder_path = "../../Assets/frames_2"

# Function to load all .ppm images into memory
def load_ppm_images(folder_path):
    images = []
    for root, dirs, files in os.walk(folder_path):
        for file in sorted(files):
            if file.endswith(".ppm"):
                file_path = os.path.join(root, file)
                try:
                    img = Image.open(file_path)
                    images.append((file, img))
                    print(f"Loaded {file}")
                except IOError:
                    print(f"Could not load {file}")
    return images

''' OG FUNCTIONS
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def setPixelBrightness(strip, pixel_id, r, g, b, brightness):
    bright_r = int(r * brightness)
    bright_g = int(g * brightness)
    bright_b = int(b * brightness)
    strip.setPixelColor(pixel_id, Color(bright_g, bright_r, bright_b))
    strip.show()
'''


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def setPixelBrightness(strip, pixel_id, r, g, b, brightness):
    bright_r = int(r * brightness)
    bright_g = int(g * brightness)
    bright_b = int(b * brightness)
    strip.setPixelColor(pixel_id, Color(bright_g, bright_r, bright_b))
    strip.show()


strands = {
    0 : {
        "start_index" : 0, # index of starting LED in the segment
        "len" : 50, # number of LEDS in target segment
        "color" : ["r", "g", "b", "y"], # color for the segment for given style
        # "color" : [[200, 100, 50], [200, 100, 50], [200, 100, 50], [200, 100, 50]], # this can turn into a 
        "effect" : [0, 1, 2, 3], # mapping style
        "dir" : [0, 1, 0, 1], 
        "dim" : [], # dimness value for the strand at each frame that relates to video
        "count" : " 0" # number to 
    },
    1 : {
        "start_index" : 49,
        "len" : 50,
        "color" : ["r", "g", "b", "y"], 
        # "color" : [[200, 100, 50], [200, 100, 50], [200, 100, 50], [200, 100, 50]], # this can turn into a 
        "effect" : [0, 1, 2, 3], 
        "dir" : [0, 1, 0, 1], 
        "dim" : [], 
        "count" : " 0"
    },
    2 : {
        "start_index" : 99,
        "len" : 50,
        "color" : ["r", "g", "b", "y"], 
        # "color" : [[200, 100, 50], [200, 100, 50], [200, 100, 50], [200, 100, 50]], # this can turn into a 
        "effect" : [0, 1, 2, 3],
        "dir" : [0, 1, 0, 1], 
        "dim" : [], 
        "count" : " 0"
    },
    3 : {
        "start_index" : 149,
        "len" : 51,
        "color" : ["r", "g", "b", "y"], 
        # "color" : [[200, 100, 50], [200, 100, 50], [200, 100, 50], [200, 100, 50]], # this can turn into a 
        "effect" : [0, 1, 2, 3], 
        "dir" : [0, 1, 0, 1], 
        "dim" : [], 
        "count" : " 0"
    }
} 

effects = {
    0 : colorWipe,
    1 : theaterChase,
    2 : rainbow,
    3 : theaterChaseRainbow
}

style_durations = [10, 5, 5, 8]
strand_nums = 0

# Load all .ppm images
ppm_images = load_ppm_images(parent_folder_path)
frame_nums = len(ppm_images)

for _, img in ppm_images:
	img.close()
 
 
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    frame_count = 0

    while True:
        for style in range(len(style_durations)):
            for strand in range(len(strands)):
                cur_strand = strands[strand]
                effects[strand.effect[style]](strip, cur_strand,frame_count)
                frame_count = (frame_count%frame_nums)+1

    # try:
        # while True:
        #     print('Color wipe animations.')
        #     colorWipe(strip, Color(255, 0, 0))  # Red wipe
        #     colorWipe(strip, Color(0, 255, 0))  # Green wipe
        #     colorWipe(strip, Color(0, 0, 255))  # Blue wipe
        #     print('Theater chase animations.')
        #     theaterChase(strip, Color(127, 127, 127))  # White theater chase
        #     theaterChase(strip, Color(127, 0, 0))  # Red theater chase
        #     theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
        #     print('Rainbow animations.')
        #     rainbow(strip)
        #     rainbowCycle(strip)
        #     theaterChaseRainbow(strip)

    # except KeyboardInterrupt:
    #     if args.clear:
    #         colorWipe(strip, Color(0, 0, 0), 10)
