cd permeabilityCase

# Generate the basic block mesh
blockMesh

# Convert the voxel data to OpenFOAM mesh
voxelToFoam -dict system/voxelToFoamDict

# Check the mesh quality
checkMesh

# Run the simulation
simpleFoam