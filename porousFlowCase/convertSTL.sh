#!/bin/bash
# Script to convert STL to OpenFOAM-compatible format

# Make sure we're in the case directory
cd $(dirname "$0")

# Create triSurface directory if it doesn't exist
mkdir -p constant/triSurface

# Check if a VTI file exists in the geometry folder
if [ -f "geometry/porous_model.vti" ]; then
    echo "Found VTI file in geometry folder."
    echo "Converting VTI to STL using ParaView is required (not automated)."
    echo "Please use ParaView to convert geometry/porous_model.vti to constant/triSurface/porous_model.stl"
    exit 1
else
    echo "ERROR: VTI file geometry/porous_model.vti not found."
    echo "Please create it first using the PNG to VTI conversion process."
    exit 1
fi

# Note: The actual VTI to STL conversion requires ParaView and cannot be easily 
# automated in a simple bash script. Please use the ParaView GUI or Python script. 