import os
import struct
import numpy as np

def create_blockmesh_dict(binary_file, output_dir='system'):
    """
    Create a blockMeshDict file for OpenFOAM based on dimensions from a binary image file.
    
    Args:
        binary_file (str): Path to the binary file
        output_dir (str): Directory to save the blockMeshDict file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read dimensions from binary file
    with open(binary_file, 'rb') as f:
        width, height = struct.unpack('ii', f.read(8))
        print(f"Image dimensions: {width}x{height}")
    
    # Create blockMeshDict content with actual dimensions
    blockmesh_content = fr"""/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \    /   O peration     | Version:  v2212                                 |
|   \  /    A nd           | Website:  www.openfoam.com                      |
|    \/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Image dimensions: {width}x{height}
scale 1;

// Define the vertices for a 3D mesh based on 2D image
// z-dimension is set to 1 cell thick for 2D simulation
vertices
(
    (0 0 0)       // 0
    ({width} 0 0)      // 1
    ({width} {height} 0)     // 2
    (0 {height} 0)      // 3
    (0 0 1)       // 4
    ({width} 0 1)      // 5
    ({width} {height} 1)     // 6
    (0 {height} 1)      // 7
);

blocks
(
    // Define a single block with the image dimensions
    hex (0 1 2 3 4 5 6 7) ({width} {height} 1) simpleGrading (1 1 1)
);

boundary
(
    inlet
    {{
        type patch;
        faces
        (
            (0 4 7 3)
        );
    }}
    outlet
    {{
        type patch;
        faces
        (
            (1 5 6 2)
        );
    }}
    walls
    {{
        type wall;
        faces
        (
            (0 1 5 4)
            (3 7 6 2)
        );
    }}
    frontAndBack
    {{
        type empty;
        faces
        (
            (0 3 2 1)
            (4 5 6 7)
        );
    }}
);

// ************************************************************************* //"""

    # Write the blockMeshDict file
    output_file = os.path.join(output_dir, 'blockMeshDict')
    with open(output_file, 'w') as f:
        f.write(blockmesh_content)
    
    print(f"Created blockMeshDict file at {output_file}")
    print(f"Mesh dimensions: {width}x{height}x1")

if __name__ == '__main__':
    # You can change this to any of your binary files
    binary_file = './foam_binary/blob_network_0.5.raw'
    create_blockmesh_dict(binary_file) 