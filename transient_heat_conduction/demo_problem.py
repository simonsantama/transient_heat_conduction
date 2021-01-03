"""
Demo problem.
"""

from main_solver import main_solver

# define the problem parameters
problem_description = {

    # geometry
    "problem_type": "direct",  # "direct or inverse
    "depth": 0.025,  # depth of the sample in meters
    "x_divisions": 101,  # number of divisions to create the spatial mesh
    "time_total": 60,  # total time in seconds

    # thermophysical properties
    "properties_type": "constant",  # constant or temperature dependent
    "conductivity": 0.2,  # thermal conductivity in W/mk
    "conductivity_exp": None,  # exponent for temperature dependence
    "density": 1196,  # density in kg/m3
    "density_exp": None,
    "heat_capacity": 1549,  # heat capacity in J/kgK
    "heat_capacity_exp": None,

    # thermal environment
    "temperature_ambient": 288,  # ambient temperature
    "temperature_initial": 288,  # initial temperature
    "boundcond_surface": "robin",  # "dirichlet", "neunamn" or "robin"
    "temperature_surface": None,  # surface temperature in K if dirichlet
    "nhf": None,  # Net Heat Flux in W/m2 if neunman
    "ihf_type": "constant",  # "constant", "polynomial", "sinusoidal" if robin
    "ihf_coefficients": [40000],
    "surface_losses_type": "non-linear",
    "h_total": None,
    "h_convective": 12,
    "absorptivity": 0.9,
    "emissivity": 0.9,

    "boundcond_back": "insulated",  # "insulated" or "conductive_losses"
    "conductivity_subs": None,

    # pyrolysis
    "material_type": "inert",  # "inert" or "reactive"
    "pre-exp_factor": None,
    "activation_energy": None,
    "heat_reaction": None,
    "reaction_order": None,

    # miscelaneous
    "material": "pmma"
    }

# call the main solver algorithm
solution = main_solver(problem_description)

# plot the data
