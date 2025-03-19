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
\*---------------------------------------------------------------------------*/
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