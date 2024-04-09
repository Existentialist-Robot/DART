#!/usr/bin/env python
import time
from samplebase import SampleBase
from PIL import Image
# import board
# import neopixel


# # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# # NeoPixels must be connected to D10, D12, D18 or D21 to work.
# pixel_pin = board.D10

# # The number of NeoPixels
# num_pixels = 201

# # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
# ORDER = neopixel.RGB

# pixels = neopixel.NeoPixel(
#     pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
# )


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="../../../examples-api-use/runtext.ppm")

    def run(self):
        # neopixel_cycle_count = 0
        frame_count = 0
        

        # let's scroll - or not
        xpos = 0
        while True: 
            frame_count = str(frame_count).zfill(3)
            image_path = "./frames2/{frame_count}.ppm"
            print(image_path)
            
            if not 'image' in self.__dict__:
                self.image = Image.open(self.args.image).convert('RGB')
            self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

            double_buffer = self.matrix.CreateFrameCanvas()
            img_width, img_height = self.image.size

            xpos += 0
            if (xpos > img_width):
                xpos = 0

            double_buffer.SetImage(self.image, -xpos)
            double_buffer.SetImage(self.image, -xpos + img_width)

            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            
            # ### Draw NeoPixels
            # for i in range(num_pixels):
            #     pixel_index = (i * 256 // num_pixels) + neopixel_cycle_count
            #     pixels[i] = wheel(pixel_index & 255)
            # pixels.show()
            
            # if neopixel_cycle_count >= 255:
            #     neopixel_cycle_count = 0
            # else:
            #     neopixel_cycle_count += 1
                
            frame_count = (frame_count+1)%100

            time.sleep(0.01)
            


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()