# Porous Medium Flow Simulation Case

This OpenFOAM case simulates single-phase flow through a porous medium to determine permeability.

## Case Overview

- **Geometry**: Binary image of porous medium (white = pores, black = solids)
- **Fluid**: Water (density = 1000 kg/m³, kinematic viscosity = 1e-06 m²/s)
- **Flow**: Steady-state, incompressible flow (simpleFoam)
- **Boundary Conditions**: Pressure drop of 1 Pa across the domain
- **Post-processing**: Calculate permeability using Darcy's law

## How to Run

1. Ensure the STL file (`porous_model.stl`) is in the `constant/triSurface` directory
2. Make the scripts executable: `chmod +x run.sh clean.sh`
3. Run the simulation: `./run.sh`
4. View results in ParaView using the generated VTK files

## Post-processing for Permeability

To calculate permeability, use Darcy's law:

```
K = μ * (ΔP/Δx)^(-1) * (1/V) * ∫ U dV
```

where:
- K is permeability [m²]
- μ is dynamic viscosity [kg/(m*s)]
- ΔP is pressure drop [Pa]
- Δx is domain length [m]
- V is total volume [m³]
- U is velocity [m/s]

A Python script for permeability calculation might be needed to post-process the results.

## Cleaning Up

To clean all simulation results and start fresh:

```
./clean.sh 