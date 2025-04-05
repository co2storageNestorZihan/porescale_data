#!/bin/bash
# Script to run the porous medium flow simulation

# Set case directory
export PORO_FOAM_CASE="$PWD"
cd $PORO_FOAM_CASE

# Create a.foam file for ParaView
touch a.foam

# Clean previous results
rm -rf processor* postProcessing [0-9]* [0-9]*.[0-9]*

# Create background mesh
blockMesh > log.blockMesh

# Create the mesh with snappyHexMesh
snappyHexMesh -overwrite > log.snappyHexMesh

# Check mesh quality
checkMesh -allTopology -allGeometry > log.checkMesh

# Scale mesh to physical units (micrometers)
transformPoints -scale "(1e-6 1e-6 1e-6)" > log.transformPoints

# Run the simulation
simpleFoam > log.simpleFoam

# Post-process: calculate cell volumes for permeability calculation
postProcess -func writeCellVolumes > log.postProcess

# Convert results to VTK format for visualization
foamToVTK -useTimeName -latestTime -poly > log.foamToVTK

echo "Simulation complete. Results are in the latest time directory and VTK folder." 