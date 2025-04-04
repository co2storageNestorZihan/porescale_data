#!/usr/bin/env python3
# VTI to STL conversion script using ParaView
import os
from paraview.simple import *

def write_stl(vti_path, stl_path):
    """Convert VTI file to STL using ParaView
    
    Args:
        vti_path: path to the input VTI file (without extension)
        stl_path: path to the output STL file
    """
    # 1. Load VTI file
    data = OpenDataFile(f'{vti_path}.vti')
    
    # 2. Clip at threshold value (255 for pores, 0 for solid)
    # Using 127.5 as the threshold as in the reference code
    clip1 = Clip(data, ClipType='Scalar', Scalars=['CELLS', 'im'], Value=127.5, Invert=1)
    
    # 3. Extract surface of the remaining part
    extractSurface1 = ExtractSurface(clip1)
    
    # 4. Triangulate for STL export
    triangulate1 = Triangulate(extractSurface1)
    
    # 5. Save as STL file
    SaveData(stl_path, proxy=triangulate1)
    
    print(f"Successfully converted {vti_path}.vti to {stl_path}")

if __name__ == "__main__":
    # Define file paths
    foam_mesh_dir = "foam_mesh"
    vti_file = os.path.join(foam_mesh_dir, "porous_medium")  # input VTI file without extension
    stl_file = os.path.join(foam_mesh_dir, "porous_model.stl")  # output STL file
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(stl_file), exist_ok=True)
    
    # Call the conversion function
    write_stl(vti_file, stl_file)
