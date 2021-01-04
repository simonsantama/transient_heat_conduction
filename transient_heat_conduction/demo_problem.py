"""
Demo problem.
"""

from main_solver import main_solver

# define the problem parameters
problem_description = {

    # miscelaneous
    # ------------
    "material": "pmma",
    "problem_type": "direct",  # "direct or inverse

    # geometry
    # --------
    "depth": 0.025,  # depth of the sample in meters
    "x_divisions": 101,  # number of divisions to create the spatial mesh
    "time_total": 60,  # total time in seconds

    # thermophysical properties
    # -------------------------
    "properties_type": "constant",  # constant or temperature dependent
    "conductivity_coeff": (0.2, None),  # conductivity in W/mK and exponent
    "density_coeff": (1196, None),  # density in kg/m2 and exponent
    "heat_capacity_coeff": (1549, None),  # heat capacity in J/kgK and exponent

    # heat transfer environment
    # -------------------------
    "temperature_ambient": 288,  # ambient temperature
    "temperature_initial": 288,  # initial temperature
    "boundcond_surface": "robin",  # "dirichlet", "neunamn" or "robin"
    "temperature_surface": None,  # surface temperature in K if dirichlet
    "nhf": None,  # Net Heat Flux in W/m2 if neunman
    "ihf_type": "constant",  # "constant", "polynomial", "sinusoidal" if robin
    "ihf_coefficients": 40000,  # W/m2
    "surface_losses_type": "non-linear",  # "linear" or "non-linear"
    "h_total": None,
    "h_convective": 12,
    "absorptivity": 0.9,
    "emissivity": 0.9,

    "boundcond_back": "insulated",  # insulated or conductive_losses
    "conductivity_subs": None,  # conductivity of substrate material in W/mK

    # pyrolysis
    # ---------
    "material_type": "inert",  # "inert" or "reactive"
    "pre_exp_factor": None,
    "activation_energy": None,
    "heat_reaction": None,
    "reaction_order": None,

    # in-depth absorption of radiation
    # --------------------------------
    "in-depth_absorptivity": 0,
    }

# call the main solver algorithm
solution = main_solver(problem_description)
