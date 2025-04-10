#!/bin/bash
# Script to clean up simulation results

# Remove time directories but preserve 0 directory
rm -rf [1-9]* [0-9]*.[0-9]*

# Remove mesh
rm -rf constant/polyMesh

# Remove logs and other generated files
rm -rf log.* postProcessing processor* VTK

echo "Cleaned up simulation files." 