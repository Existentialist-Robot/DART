import os
from PIL import Image

# Specify the path to the parent folder containing the .ppm files
parent_folder_path = "../your_parent_folder_path_here"

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
    # Here, you can process each image. For demonstration, let's print its size.
    print(f"Processing {file_name}: {img.size[0]}x{img.size[1]}")

    # Add your code here to work with the image or send it to the RGB LED matrix

    # Note: You don't need to open the image again with PIL, as it's already loaded.

# If you are done with processing and want to release memory, explicitly close each image:
for _, img in ppm_images:
    img.close()