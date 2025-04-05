#!/bin/sh
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

application=`getApplication`

# Create a.foam file for ParaView
touch a.foam

# Clean previous results
./clean.sh

# Make sure the STL file is in the right format
if [ -f "../foam_mesh/porous_model.stl" ]; then
    mkdir -p constant/triSurface
    cp ../foam_mesh/porous_model.stl constant/triSurface/input.stl
    surfaceConvert constant/triSurface/input.stl constant/triSurface/porous_model.stl
    rm constant/triSurface/input.stl
    echo "STL file converted successfully"
else
    echo "WARNING: STL file not found in ../foam_mesh/"
fi

# Run mesh generation and simulation
runApplication blockMesh
runApplication snappyHexMesh -overwrite
runApplication checkMesh -allTopology -allGeometry

runApplication transformPoints -scale "(1e-6 1e-6 1e-6)"

runApplication $application

# Post-processing
runApplication postProcess -func writeCellVolumes
runApplication foamToVTK -useTimeName -latestTime -poly

echo "Simulation complete. Results are in the latest time directory and VTK folder." 