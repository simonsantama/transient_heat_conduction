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
    "time_total": 600,  # total time in seconds

    # thermophysical properties
    # -------------------------
    "properties_type": "constant",  # "constant" or "temperature_dependent"
    "conductivity_coeff": (0.2, None),  # conductivity in W/mK and exponent
    "density_coeff": (1196, None),  # density in kg/m2 and exponent
    "heat_capacity_coeff": (1549, None),  # heat capacity in J/kgK and exponent

    # heat transfer environment
    # -------------------------
    "temperature_ambient": 288,  # ambient temperature
    "temperature_initial": 288,  # initial temperature
    "boundcond_surface": "dirichlet",  # "dirichlet", "neunamn" or "robin"
    "temperature_surface": 800,  # surface temperature in K if dirichlet
    "nhf": None,  # Net Heat Flux in W/m2 if neunman
    "ihf_type": "constant",  # "constant", "polynomial", "sinusoidal"
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

    # extra (checking validation)
    # --------------------------
    "validation_case": True
    }

# call the main solver algorithm
solution = main_solver(problem_description)


# ------
# plot temperatures if validation with analytical solutions is desired
# ------
if problem_description["validation_case"]:

    # import extra libraries
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import os
    import numpy as np
    from validation_plots_analyticalsols.calc_analytical import (
        calc_dirichlet, calc_neunman, calc_robin)

    # create figure and format
    cmap = cm.get_cmap('cividis', 10)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlabel("Depht [m]", fontsize=16)
    ax.set_ylabel("Tempeature [K]", fontsize=16)
    ax.set_xlim([0, problem_description["depth"]])
    ax.set_ylim([0, 1000])
    ax.grid(True, linestyle="--", linewidth=0.75, color="gainsboro")
    ax.tick_params(axis='both', which='major', labelsize=13)
    ax.tick_params(axis='both', which='minor', labelsize=11)
    ax.set_title(f"{problem_description['boundcond_surface']} boundary"
                 f"condition.")
    if problem_description['boundcond_surface'] == "dirichlet":
        text = ("$T_{surf}$"
                f" = {problem_description['temperature_surface']} K")
    elif problem_description["boundcond_surface"] == "neunmnan":
        text = ('NHF = {problem_description["nhf"]} kW/m2')
    ax.text(0.02, 500, text, fontsize=15)

    # plot analytical and numerical solutions at 8 different times
    for i, step in enumerate(np.linspace(
            1, solution["sample"].temperatures.columns.shape[0]-1, 8)):
        t = solution["sample"].temperatures.columns[int(step)]

        # plot numerical
        ax.scatter(solution["sample"].space_mesh,
                   solution["sample"].temperatures.loc[:, t],
                   s=40, color=cmap(i/10), alpha=0.6,
                   label=f'{np.round(t,1)} seconds')

        # plot analytical
        if problem_description["boundcond_surface"] == "dirichlet":
            analytical = calc_dirichlet(solution, t)
        elif problem_description["boundcond_surface"] == "neunman":
            analytical = calc_neunman(solution, t)
        elif problem_description["boundcond_surface"] == "robin":
            analytical = calc_robin(solution, t)
        ax.plot(solution["sample"].space_mesh,
                analytical,
                color=cmap(i/10), linestyle="-",
                linewidth=1.5)
    ax.legend(loc='upper center', ncol=2, fontsize=13)

    figure_name = (f"validation_{problem_description['material']}_"
                   f"bouncond-{problem_description['boundcond_surface']}_"
                   f"boundcondback-insulated.png")
    plt.savefig(os.path.join('validation_plots_analyticalsols', figure_name))
