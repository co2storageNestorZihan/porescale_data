import os
import numpy as np
from PIL import Image

def png_to_foam_binary(input_dir='./sample_blobs', output_dir='./foam_binary'):
    """
    Convert all PNG files in input directory to OpenFOAM-compatible binary files.
    
    Args:
        input_dir (str): Path to directory containing PNG files
        output_dir (str): Path to save binary files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of PNG files
    png_files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    
    for png_file in png_files:
        # Read PNG file
        img_path = os.path.join(input_dir, png_file)
        img = Image.open(img_path)
        img_array = np.array(img)
        
        # Convert to binary format (OpenFOAM expects row-major order)
        binary_data = img_array.astype(np.float32).tobytes()
        
        # Create output filename
        base_name = os.path.splitext(png_file)[0]
        foam_file = os.path.join(output_dir, f'{base_name}.raw')
        
        # Write binary file
        with open(foam_file, 'wb') as f:
            # Write header with dimensions (OpenFOAM format)
            header = np.array([img_array.shape[1], img_array.shape[0]], dtype=np.int32)
            f.write(header.tobytes())
            f.write(binary_data)
            
        print(f'Converted {png_file} to {foam_file}')

if __name__ == '__main__':
    png_to_foam_binary()