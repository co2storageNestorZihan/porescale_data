#%%
import numpy as np
import struct
import os

def create_alpha_field(binary_file, output_dir='0'):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(binary_file, 'rb') as f:
        width, height = struct.unpack('ii', f.read(8))
        data = np.frombuffer(f.read(), dtype=np.float32).reshape(height, width)

    header = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2212                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      binary;
    class       volScalarField;
    object      alpha;
}}

dimensions [0 0 0 0 0 0 0];

internalField   nonuniform List<scalar> 
{data.size}
(
"""

    with open(f'{output_dir}/alpha', 'wb') as f:
        f.write(header.encode('ascii'))
        f.write(b')\n;\n\n// Binary data\n')
        f.write(struct.pack('<Q', data.size))
        data.astype(np.float32).flatten().tofile(f)




def create_block_mesh(width, height, output_dir='system'):
    os.makedirs(output_dir, exist_ok=True)
    
    content = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2212                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}

convertToMeters 1.0;

vertices
(
    (0 0 0)
    ({width} 0 0)
    ({width} {height} 0)
    (0 {height} 0)
    (0 0 0.1)
    ({width} 0 0.1)
    ({width} {height} 0.1)
    (0 {height} 0.1)
);

blocks
(
    hex (0 1 2 3 4 5 6 7) ({width} {height} 1) simpleGrading (1 1 1)
);

edges
(
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
            (1 2 6 5)
        );
    }}
    walls
    {{
        type wall;
        faces
        (
            (0 3 2 1)
            (4 5 6 7)
        );
    }}
);

mergePatchPairs
(
);
"""

    with open(f'{output_dir}/blockMeshDict', 'w') as f:
        f.write(content)




# ... keep existing functions unchanged ...
if __name__ == "__main__":
    # Hardcoded file path
    binary_file = "./foam_binary/blob_network_0.5.raw"
    output_dir = '0'
    system_dir = 'system'

    # Read binary data directly
    with open(binary_file, 'rb') as f:
        width, height = struct.unpack('ii', f.read(8))
        data = np.frombuffer(f.read(), dtype=np.float32).reshape(height, width)
    
    create_alpha_field(binary_file, output_dir)
    create_block_mesh(width, height, system_dir)
# %%
