#!/bin/bash
# Script to convert STL to OpenFOAM-compatible format

# Make sure we're in the case directory
cd $(dirname "$0")

# Create triSurface directory if it doesn't exist
mkdir -p constant/triSurface

# Copy the STL file from foam_mesh to a temporary location
cp ../foam_mesh/porous_model.stl constant/triSurface/temp.stl

# Convert to binary format that OpenFOAM can read
surfaceConvert constant/triSurface/temp.stl constant/triSurface/porous_model.stl

# Remove the temporary file
rm constant/triSurface/temp.stl

echo "STL file converted and placed in constant/triSurface/" 