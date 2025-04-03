# read raw image from foam binary folder
#%%
import os
import numpy as np
from PIL import Image

# Load and process the binary image
img = Image.open('sample_blobs/blob_network_0.5.png')
print(f"Original image dimensions: {img.size}")

# Convert to binary array (0 for solid/black, 1 for void/white)
img_array = np.array(img.convert('L'))
binary_array = (img_array > 128).astype(np.uint8)  # Threshold at 128 (mid-gray)

# Save as raw binary format for OpenFOAM
binary_array_3d = np.stack([binary_array] * 1)  # Make it 3D with 1 layer
binary_array_3d.tofile('foam_mesh/porous_medium.raw')

# Save dimensions to a separate file
with open('foam_mesh/porous_medium_dims.txt', 'w') as f:
    f.write(f"{img.size[0]} {img.size[1]} 1")  # Width, Height, Depth

print("Binary data prepared for OpenFOAM meshing")

# %%
