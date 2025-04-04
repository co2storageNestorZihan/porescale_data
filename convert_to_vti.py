#%%
import os
import numpy as np
from PIL import Image
import porespy as ps
import matplotlib.pyplot as plt

# Create foam_mesh directory if it doesn't exist
os.makedirs('foam_mesh', exist_ok=True)

# Load the binary image
img_path = 'sample_blobs/blob_network_0.5.png'
img = Image.open(img_path).convert("L")
print(f"Original image dimensions: {img.size}")

#%%
# Convert the image to a numpy array
arr = np.asarray(img, dtype=int)
print(f"Array shape: {arr.shape}")

# Make 3D by stacking along axis=2 (as per reference)
arr_stacked = np.stack((arr, arr), axis=2)
print(f"3D array shape: {arr_stacked.shape}")

# Save as VTI file for ParaView visualization
vti_filename = os.path.join('foam_mesh', 'porous_medium')
ps.io.to_vtk(arr_stacked, vti_filename)
print(f"Saved VTI file to: {vti_filename}")

# Optionally visualize a slice of the 3D array
plt.figure(figsize=(8, 8))
plt.imshow(arr, cmap='gray')
plt.title('Binary Image')
plt.axis('off')
plt.savefig(os.path.join('foam_mesh', 'binary_image.png'))
print(f"Saved visualization to: {os.path.join('foam_mesh', 'binary_image.png')}")

print("Conversion complete. You can now visualize the VTI file in ParaView.") 