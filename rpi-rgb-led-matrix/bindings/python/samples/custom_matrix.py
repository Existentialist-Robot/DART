import os
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

# Configuration for the LED matrix
options = RGBMatrixOptions()
options.rows = 64  # Change this to match your matrix's row count
options.cols = 64  # Change this to match your matrix's column count
options.chain_length = 2  # Change if you have daisy-chained matrices
options.parallel = 1  # Change if you use parallel chains of matrices
options.hardware_mapping = 'adafruit-hat-pwm'  # Change to 'adafruit-hat' if using Adafruit's HAT

# Create the matrix object
matrix = RGBMatrix(options=options)


# Specify the path to the parent folder containing the .ppm files
parent_folder_path = "../../../../frames_2"

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

# Load all .ppm images
ppm_images = load_ppm_images(parent_folder_path)

# Process the loaded images
for file_name, img in ppm_images:
    print(f"Processing {file_name}: {img.size[0]}x{img.size[1]}")


for file_name, img in ppm_images:
    print(f"Displaying {file_name} on the LED matrix.")
    
    ### if needing to rotate or resize

    # Rotate
    #img_rotated = img.rotate(90, expand=True)
    print("Size before rotate: {}, {}".format(int(img.width), int(img.height)))

    img_rotated = img.rotate(90, expand=True)
    
    # Resize the image to half its size to fit your matrix size
    print("Current size after rotate: {}, {}".format(int(img_rotated.width), int(img_rotated.height)))
    new_size = (int(img_rotated.width * 0.5), int(img_rotated.height * 0.5))
    img_resized = img_rotated.resize(new_size)
    
    print("Confirmed new size: {}, {}".format(img_resized.width, img_resized.height))
    
    # Display the image on the matrix
    matrix.SetImage(img_resized.convert('RGB'))

    # Example of displaying each image for 5 seconds
    time.sleep(0.05)

# Clear the matrix when done
matrix.Clear()
    # Note: You don't need to open the image again with PIL, as it's already loaded.

# If you are done with processing and want to release memory, explicitly close each image:
for _, img in ppm_images:
    img.close()
