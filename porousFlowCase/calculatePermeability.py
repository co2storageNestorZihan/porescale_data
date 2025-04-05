#!/usr/bin/env python3
"""
Calculate permeability from OpenFOAM porous medium flow simulation results
"""
import os
import sys
import numpy as np
try:
    import vtk
    from vtk.util import numpy_support as VN
except ImportError:
    print("Error: VTK Python bindings not found. Please install with: pip install vtk")
    sys.exit(1)

def load_vtk_data(vtk_file):
    """Load the VTK data file"""
    print(f"Loading VTK file: {vtk_file}")
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(vtk_file)
    reader.ReadAllScalarsOn()
    reader.ReadAllVectorsOn()
    reader.Update()
    return reader.GetOutput()

def calculate_permeability(vtk_data, pressure_drop, dx, mu):
    """Calculate permeability using Darcy's law"""
    # Extract cell volumes
    v_cells = VN.vtk_to_numpy(vtk_data.GetCellData().GetArray('V'))
    
    # Extract velocity
    u = VN.vtk_to_numpy(vtk_data.GetCellData().GetArray('U'))
    u_x = u[:, 0]  # x component of velocity
    
    # Calculate volume-weighted average velocity
    total_volume = np.sum(v_cells)
    avg_velocity_x = np.sum(v_cells * u_x) / total_volume
    
    # Calculate permeability using Darcy's law
    # K = μ * (ΔP/Δx)^(-1) * (average velocity)
    pressure_gradient = pressure_drop / dx
    permeability = mu * avg_velocity_x / pressure_gradient
    
    return permeability, avg_velocity_x, total_volume

def main():
    # Find the latest time directory
    time_dirs = [d for d in os.listdir('VTK') if d.startswith('porousFlowCase_')]
    if not time_dirs:
        print("Error: No VTK output files found. Run the simulation first.")
        sys.exit(1)
    
    latest_time = sorted(time_dirs)[-1]
    vtk_file = os.path.join('VTK', f'{latest_time}.vtk')
    
    # Check if the file exists
    if not os.path.exists(vtk_file):
        print(f"Error: VTK file not found: {vtk_file}")
        sys.exit(1)
    
    # Simulation parameters
    pressure_drop = 1.0  # Pa
    rho = 1000.0         # kg/m³
    nu = 1e-6            # m²/s
    mu = rho * nu        # Pa·s
    dx = 80e-6           # m (domain length, 80 pixels scaled to micrometers)
    
    # Load data and calculate permeability
    vtk_data = load_vtk_data(vtk_file)
    perm, avg_vel, vol = calculate_permeability(vtk_data, pressure_drop, dx, mu)
    
    # Print results
    print("\nResults:")
    print(f"Average x-velocity: {avg_vel:.6e} m/s")
    print(f"Total volume: {vol:.6e} m³")
    print(f"Permeability: {perm:.6e} m²")
    print(f"Permeability: {perm*1e12:.6f} darcy")

if __name__ == "__main__":
    main() 