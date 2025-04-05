#!/bin/sh
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

application=`getApplication`

# Create a.foam file for ParaView
touch a.foam

# Clean previous results
./clean.sh

# Check for STL file and create if needed
if [ -f "constant/triSurface/porous_model.stl" ]; then
    echo "STL file found in constant/triSurface/"
elif [ -f "../foam_mesh/porous_model.stl" ]; then
    mkdir -p constant/triSurface
    cp ../foam_mesh/porous_model.stl constant/triSurface/
    echo "STL file copied from ../foam_mesh/"
else
    # If STL not found, check for image in geometry folder to create it
    if [ -f "geometry/porous_model.png" ]; then
        echo "Need to convert PNG to STL - please run convertSTL.sh first"
        exit 1
    else
        echo "ERROR: No STL file found and no source image found. Cannot proceed."
        exit 1
    fi
fi

echo "Starting mesh generation..."
# Run mesh generation and simulation
runApplication blockMesh
runApplication snappyHexMesh -overwrite
runApplication checkMesh -allTopology -allGeometry

echo "Scaling mesh to micrometers..."
runApplication transformPoints -scale "(1e-6 1e-6 1e-6)"

echo "Running flow simulation..."
runApplication $application

# Post-processing
echo "Post-processing results..."
runApplication postProcess -func writeCellVolumes
runApplication foamToVTK -useTimeName -latestTime -poly

# echo "Running permeability calculation..."
# python3 calculatePermeability.py

echo "Simulation complete. Results are in the latest time directory and VTK folder."
# echo "Check permeability_results.txt for the calculated permeability." 