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
import random

# LED strip configuration:
LED_COUNT = 199        # Number of LED pixels.
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

# if the target pixel in the segment is at the end
# reset segment to start of segment by seting the strand count equal to zero
def maintainIndex(strip, strand):
    # print("count: {}".format(type(strand["count"])))
    # print("len: {}".format(type(strand["len"])))
    reset = False
    
    if strand["count"] >= strand["len"]:
        strand["count"] = 0
        reset = True
        
    return reset
        
def wipeStrand(strand):
    for i in range(strand["len"]):
        strip.setPixelColor(strand["start_index"] + i, 0)
                
# implement brightness
def setBright(strand, style, count):

    r = int(strand["color"][style][0] * strand["bright"][style])
    g = int(strand["color"][style][1] * strand["bright"][style])
    b = int(strand["color"][style][2] * strand["bright"][style])
    
    '''
    r = int(strand["color"][style][0] * 1)
    g = int(strand["color"][style][1] * 1)
    b = int(strand["color"][style][2] * 1)
    '''
    
    '''
        r = int(strand["color"][style][0] * strand["dim"][count])
        g = int(strand["color"][style][1] * strand["dim"][count])
        b = int(strand["color"][style][2] * strand["dim"][count])
    '''

    return r, g, b
   
def get_targ_pixel(strand,style):
    if strand["dir"][style] == 1:
        targ_pixel = strand["start_index"] + strand["count"]
    else:
        targ_pixel = strand["start_index"] + strand["len"] - strand["count"]
    return targ_pixel

# Define functions which animate LEDs in various ways.
def colorWipe(strip, strand, count, style, durs):
    """Wipe color across display a pixel at a time."""
    reset = maintainIndex(strip, strand)
    if reset == True:
            wipeStrand(strand)
    r, g, b = setBright(strand, style, count)
    targ_pixel = get_targ_pixel(strand, style)
    strip.setPixelColor(targ_pixel, Color(r, g, b))
    print("Strand: {}, Pixel Number: {}".format(list(strands.values()).index(strand), targ_pixel))
    strip.show()
    strand["count"] += 1

def signalTransmit(strip, strand, count, style, durs):
    """Wipe color across display a pixel at a time."""
    reset = maintainIndex(strip, strand)
    r, g, b = setBright(strand, style, count)
    targ_pixel = get_targ_pixel(strand, style)
    
    strip.setPixelColor(targ_pixel - 1 , 0)
    strip.setPixelColor(targ_pixel, Color(r, g, b))
    if strand["count"] != strand["len"]:
        strip.setPixelColor(targ_pixel + 1, Color(r, g, b))
    print("Strand: {}, Pixel Number: {}".format(list(strands.values()).index(strand), targ_pixel))
    strip.show()
    strand["count"] += 1

def randoSignal(strip, strand, count, style, durs):
    """Wipe color across display a pixel at a time."""
    reset = maintainIndex(strip, strand)
    r, g, b = setBright(strand, style, count)
    wipeStrand(strand)
    for i in range(3):
        x = random.randrange(strand["start_index"],strand["start_index"] + strand["len"])
        strip.setPixelColor(x, Color(r, g, b))
    # print("Strand: {}, Pixel Number: {}".format(list(strands.values()).index(strand), targ_pixel))
    strip.show()
    strand["count"] += 1

def buildUp(strip, strand, count, style, durs):
    """Wipe color across display a pixel at a time."""
    reset = maintainIndex(strip, strand)
    r = int(strand["color"][style][0] * 0.1 * strand["count"])
    g = int(strand["color"][style][1] * 0.1 *  strand["count"])
    b = int(strand["color"][style][2] * 0.1 *  strand["count"])
    print(r,g,b)
    # wipeStrand(strand)
    for i in range(strand["len"]):
        strip.setPixelColor(strand["start_index"] + i, Color(r, g, b))
        
    # print("Strand: {}, Pixel Number: {}".format(list(strands.values()).index(strand), targ_pixel))
    strip.show()
    strand["count"] += 1

def theaterChase(strip, strand, count, style, durs):
    """Movie theater light style chaser animation."""
    maintainIndex(strip, strand)
    r, g, b = setBright(strand, style, count)
    targ_pixel = strand["start_index"] + strand["count"]
    strip.show()

    for i in range(strand["start_index"],strand["start_index"] + strand["len"], int(strand["len"]/3)):
        strip.setPixelColor(i + targ_pixel + strand["count"], Color(r, g, b))
        strip.show()
    strand["count"] += 1
    if strand["count"] > int(strand["len"]/3):
        strand["count"] = 0
        
    print("Strand: {}, Pixel Number: {}".format(list(strands.values()).index(strand), targ_pixel))
    # print("Bin: {}".format(strand["bin"]))

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

strands = {
    0 : { 
        # strand
        "start_index" : 18, # index of starting LED in the segment
        "len" : 17, # number of LEDS in target segment
        "color" : [[255, 255, 255], [150, 255, 255], [255, 255, 255]], # this can turn into a 
        "effect" : [0, 2, 1], # mapping style
        "dir" : [1, 1, 0], 
        "dim" : [], # dimness value for the strand at each frame that relates to video
        "count" : 0, # index of target
        "bin" : 0,
        "bright" : [0.1, 1, 1]
        },
    1 : {
        # ball
        "start_index" : 35,
        "len" : 16,
        "color" : [[255, 255, 255], [0, 255, 0], [255, 255, 255]], # this can turn into a 
        "effect" : [3, 3, 3], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [0.1, 1, 1]
        },
    2 : {
        # strand
        "start_index" : 52,
        "len" : 11,
        "color" : [[0, 0, 0], [255, 150, 255], [255, 255, 255]], # this can turn into a 
        "effect" : [0, 2, 1], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [1, 0.5, 1]
        },
    3 : {
        # ball
        "start_index" : 64,
        "len" : 9,
        "color" : [[255, 255, 255], [0, 255, 0], [255, 255, 255]], # this can turn into a 
        "effect" : [3, 3, 3], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [0.5, 1, 1]
    },
    4 : {
        # strand
        "start_index" : 74,
        "len" : 15,
        "color" : [[255, 255, 255], [255, 255, 150], [255, 255, 255]], # this can turn into a 
        "effect" : [0, 2, 1], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [1, 0.5, 1]
        },
   5 : {
        # strand
        "start_index" : 101,
        "len" : 9,
        "color" : [[255, 255, 255], [150, 255, 255], [255, 255, 255]], # this can turn into a 
        "effect" : [0, 2, 1], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [1, 0.5, 1]
        },
    6 : {
        # ball
        "start_index" : 110,
        "len" : 4,
        "color" : [[255, 255, 255], [255, 255, 255], [255, 255, 255]], # this can turn into a 
        "effect" : [3 , 3, 3], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [0.05, 1, 1]
        },
    7 : {
        # strand
        "start_index" : 114,
        "len" : 12,
        "color" : [[255, 255, 255], [255, 150, 255], [255, 255, 255]], # this can turn into a 
        "effect" : [0, 2, 1], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [1, 0.5, 1]
        },
    8 : {
        # strand
        "start_index" : 127,
        "len" : 14,
        "color" : [[255, 255, 255], [255, 255, 150], [255, 255, 255]], # this can turn into a 
        "effect" : [0, 2, 1], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [0.5, 1, 1]        
        },
    9 : {
        # strand
        "start_index" : 142,
        "len" : 13,
        "color" : [[255, 255, 255], [255, 255, 255], [255, 255, 255]], # this can turn into a 
        "effect" : [0, 2, 1], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [0.5, 1, 1]        
        },
    10 : {
        # ball
        "start_index" : 184,
        "len" : 15,
        "color" : [[255, 255, 255], [0, 255, 0], [255, 255, 255]], # this can turn into a 
        "effect" : [3, 3, 3], 
        "dir" : [0, 1, 0], 
        "dim" : [], 
        "count" : 0,
        "bin" : 0,
        "bright" : [0.5, 1, 1]        
    }
} 

effects = {
    0 : colorWipe,
    1 : signalTransmit,
    2 : randoSignal,
    3 : buildUp,
    4 : theaterChase,
    5 : rainbow,
    6 : rainbowCycle,
    7 : theaterChaseRainbow
}

# vary the following two to make the duration of strand styles animation match up 
# as well as change the speed of the light effects 
#style_durations = [90, 90, 90] 
style_durations = [10, 10, 10] 

#style_speeds = [50, 25, 50, 25]
style_speeds = [0, 5, 0]

strand_nums = 0

# Load all .ppm images
ppm_images = load_ppm_images(parent_folder_path)
frame_nums = len(ppm_images)
wait_ms = 20

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
    cur_style = 0
    start_time = time.time()
    last_time = start_time

    while True:
        for name, strand in strands.items():
            effects[strand["effect"][cur_style]](strip, strand, frame_count, cur_style, style_durations)
            frame_count = (frame_count%frame_nums)+1
            time.sleep(style_speeds[cur_style] / 1000.0)
        if (time.time()-last_time) > style_durations[cur_style]:
            print("Changing the style")
            cur_style +=1
            if cur_style >= len(style_durations):
                cur_style = 0
            last_time = time.time()
            for name, strand in strands.items():
                wipeStrand(strand)
        print("Current Style: {}".format(cur_style))
        print("Time Elapsed: {}, Duration of Current Style: {}".format(((time.time()-last_time)), style_durations[cur_style]))



