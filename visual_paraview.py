
# This script does not run Paraview automatically.
# It outlines the manual steps needed in the Paraview GUI based on the tutorial:
# https://lruepke.github.io/HTF_lecture/summer2022/lectures/L03/FirstCase.html#making-the-mesh

# Steps:
# 1. Run `read_img.py` to generate `foam_mesh/porous_medium.vti`.
#
# 2. Open the Paraview application.
#
# 3. Load the .vti file:
#    - Go to File -> Open...
#    - Navigate to the `foam_mesh` directory and select `porous_medium.vti`.
#    - Click "Apply" in the Properties panel.
#
# 4. Apply the Clip filter to extract the pore space (value = 1):
#    - Select `porous_medium.vti` in the Pipeline Browser.
#    - Go to Filters -> Common -> Clip (or use the Clip button).
#    - In the Properties panel:
#        - Set "Clip Type" to "Scalar".
#        - Set "Scalars" to "Scalars_".
#        - Set "Value" to 0.5 (to separate values 0 and 1).
#        - Check "Inside Out" if you want to keep the region where Scalar > 0.5 (the pores, assuming 1=pore).
#          (The tutorial image shows pores as white (1) and solids as black (0), so keeping > 0.5 should be correct).
#        - Click "Apply".
#
# 5. Apply the Triangulate filter to the clipped surface:
#    - Select the "Clip1" object in the Pipeline Browser.
#    - Go to Filters -> Common -> Triangulate (or search for "Triangulate").
#    - Click "Apply".
#
# 6. Save the triangulated surface as an STL file:
#    - Select the "Triangulate1" object in the Pipeline Browser.
#    - Go to File -> Save Data...
#    - Choose a location and filename. The tutorial suggests placing it in the OpenFOAM case directory:
#      `case_perm_1/constant/triSurface/porous_medium.stl` (You'll need to create this directory structure).
#    - Ensure the file type is ".stl".
#    - Click "OK".

# After these steps, you will have the `porous_medium.stl` file required for `snappyHexMesh`.