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
    u_y = u[:, 1]  # y component of velocity
    u_z = u[:, 2]  # z component of velocity
    
    # Calculate volume-weighted average velocity
    total_volume = np.sum(v_cells)
    
    # Calculate volume fluxes for each direction
    q_x = v_cells * u_x
    q_y = v_cells * u_y
    
    # Average velocity components
    avg_velocity_x = np.sum(q_x) / total_volume
    avg_velocity_y = np.sum(q_y) / total_volume
    
    # Calculate permeability using Darcy's law
    # K = μ * (ΔP/Δx)^(-1) * (average velocity)
    pressure_gradient = pressure_drop / dx
    permeability_x = mu * avg_velocity_x / pressure_gradient
    
    # Calculate the magnitude for informational purposes
    u_mag = np.sqrt(u_x**2 + u_y**2 + u_z**2)
    avg_velocity_mag = np.sum(v_cells * u_mag) / total_volume
    
    return permeability_x, avg_velocity_x, avg_velocity_y, avg_velocity_mag, total_volume

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
    mu = rho * nu        # Pa·s (0.001 Pa·s for water)
    
    # Domain dimensions in meters after scaling
    dx = 80e-6           # m (domain length, 80 pixels scaled to micrometers)
    
    # Load data and calculate permeability
    vtk_data = load_vtk_data(vtk_file)
    perm_x, avg_vel_x, avg_vel_y, avg_vel_mag, vol = calculate_permeability(vtk_data, pressure_drop, dx, mu)
    
    # Print results
    print("\nResults:")
    print(f"Total volume: {vol:.6e} m³")
    print(f"Average x-velocity: {avg_vel_x:.6e} m/s")
    print(f"Average y-velocity: {avg_vel_y:.6e} m/s")
    print(f"Average velocity magnitude: {avg_vel_mag:.6e} m/s")
    print(f"Pressure gradient: {pressure_drop/dx:.6e} Pa/m")
    print(f"Permeability in x-direction: {perm_x:.6e} m²")
    print(f"Permeability in x-direction: {perm_x*1e12:.6f} darcy (1 darcy = 9.869233e-13 m²)")
    
    # Save results to file
    with open('permeability_results.txt', 'w') as f:
        f.write("Permeability Results\n")
        f.write("===================\n\n")
        f.write(f"Domain length: {dx:.6e} m\n")
        f.write(f"Pressure drop: {pressure_drop:.6f} Pa\n")
        f.write(f"Fluid viscosity: {mu:.6e} Pa·s\n")
        f.write(f"Average x-velocity: {avg_vel_x:.6e} m/s\n")
        f.write(f"Permeability: {perm_x:.6e} m²\n")
        f.write(f"Permeability: {perm_x*1e12:.6f} darcy\n")

if __name__ == "__main__":
    main() 