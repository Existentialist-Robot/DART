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
options.hardware_mapping = 'adafruit-hat'  # Change to 'adafruit-hat' if using Adafruit's HAT

# Create the matrix object
matrix = RGBMatrix(options=options)

compress = 2 # 2 will cut dims in half, 4 cuts dim by 4
rotate = 90 # how much to rotate

# Specify the path to the parent folder containing the .ppm files
parent_folder_path = "../../../../Assets/frames_3/128pframes"

# Function to load all .ppm images into memory
def load_file_names(folder_path):
	file_paths = []
	for root, dirs, files in os.walk(folder_path):
		for file in sorted(files):
			if file.endswith(".ppm"):
				file_path = os.path.join(root, file)
				print(file_path)
				file_paths.append(file_path)
	return file_paths

# Load all .ppm images
file_paths = load_file_names(parent_folder_path)
num_images = len(file_paths)
print(num_images)

# Process the loaded images
# for file_name in file_paths:
    # print(f"Processing {file_name}: {img.size[0]}x{img.size[1]}")

while True:
	for file in file_paths:
		img = Image.open(file)
		# print(f"Displaying {file} on the LED matrix.")
		
		print(f"Processing {file}: {img.size[0]}x{img.size[1]}")

		
		# Squish image if needed
		if compress != 0:
			new_size = (img.width // compress, img.height // compress)
			img_resized = img.resize(new_size)
			print("Confirmed new size: {}".format(new_size))
		
		# Rotate image if needed
		if rotate != 0:
			if compress != 0:
				img_rotated = img_resized.rotate(rotate, expand=True)
			else:
				img_rotated = img.rotate(rotate, expand=True)
			print("mode: {}".format(img_rotated.mode))
			
		if compress != 0 and rotate == 0:
			matrix.SetImage(img_resized.convert('RGB'))
		elif compress != 0 and rotate != 0 or compress != 0 and rotate != 0:
			matrix.SetImage(img_rotated.convert('RGB'))
		else:
			matrix.SetImage(img.convert('RGB'))

		# Example of displaying each image for x seconds
		time.sleep(0.02)
		
		img.close()


# Clear the matrix when done
matrix.Clear()


