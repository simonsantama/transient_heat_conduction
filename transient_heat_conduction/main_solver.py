"""
Main script.
This script is called by other algorithms, wishing to use the heat transfer
solver.

1-D heat transfer solver.
Direct or inverse heat transfer problemns.
Constant or variable properties.
Homogenous solid.

"""
import time
import numpy as np
import datetime

# import from local project
from classes_and_functions.solid_sample import solid_sample
from classes_and_functions.calc_parameters import (calc_Fo, calc_Upsilon,
                                                   matrix_A, vector_b,
                                                   update_thermal_properties)
from direct_solution.direct_solver import direct_solver


def main_solver(problem_description):
    """
    Main function that will implement the heat transfer solver and return
    all the information.

    Parameters
    ----------
    problem_description : DICT
        Contains the description of the heat transfer problem, including
        problem type, properties and boundary conditions.

        Function takes as input as shown below. If any value is not needed,
        pass None.

            "material": material to be tested. used for file name. if unknown
                or non-applicable, pass "material-unknown"
            "problem_type": "direct" or "inverse"

            geometry
            --------
            "depth": depth of the sample in m.
            "x_divisions": number of divisions to create spatial mesh
            "time_total": total time for the analysis in seconds

            thermophysical properties
            -------------------------
            "properties_type": "constant" or "temperature_dependent". If
                temperature dependence is considered, then the following form
                is assumed: X(T) = Xo(T/300)^exp, where Xo is the value
                provided and exp needs to be additionally specified

            "conductivity_coeff": (base, exponent) -> base conductivity and
                exponent for temperature dependence. W/mK
            "density_coeff": (base, exponent) -> base density and exponent for
                temperature dependence. kg/m3
            "heat_capacity_coeff": (base, exponent) -> base heat capacity and
                exponent for temperature dependence. J/kgK

            heat transfer environment
            ------------------------
            "temperature_ambient": ambient temperature in K.
            "temperature_initial": initial temperature in K. Float or array
                whose length equals x_divisions

            "boundcond_surface" "dirichlet", "neunman" or "robin"
            if "dirichlet":
                "temperature_surface": constant surface temperature in K.
            elif "neunman":
                "nhf": constant Net Heat Flux in W/m2.
            elif "robin":
                "ihf_type": "constant", "polynomial", "sinusoidal"
                if "constant":
                    "ihf_coefficients": ihf in W/m2
                elif "polynomial":
                    "ihf_coefficients": list of coefficients to reconstruct the
                    ihf vs time curve in W/m2. From a0x^0 + a1x^1 + .. + anx^n
                elif "sinusoidal":
                    "ihf_coefficients": amplitud, angular frequency and phase
                    angle (A, omega, phi)

                "surface_losses_type": "linear", "non-linear"
                    if "linear":
                        "h_total": total (constant) heat transfer coefficient
                    if "non-linear":
                        "h_convective": convective heat transfer coefficient
                        in W/m2K
                        absorptivity: surface absorptivity (constant)
                        emissivity: surface emissivity (constant)

            "boundcond_back": "insulated" or "conductive_losses":
                if "insulated": no additional parameters required.
                elif "conductive_losses": null contact resistance assumed.
                    "conductivity_subs": thermal conductivity of substrate
                    material in W/mK

            pyrolysis:
            ---------
            "material_type": "inert" or "reactive"
            if "reactive":
                accomodates for a single order, first order in fuel
                Arrhenius type reacion.
                "pre_exp_factor": pre-exponential factor in 1/s 10^-6
                "activation_energy": activation energy in kJ/mol
                "heat_reaction": heat of reaction in kJ/kg
                "reaction_order": reaction order.

            in-depth absorption of radiation:
            ------------
            "in-depth_absorptivity": value in 1/m

    Returns
    -------
    solution: DICT
        Contains the description of the problem as well as the full
        temperature profile discretized over the calculated spatial and
        temporal grids.

    """

    time_start = time.time()

    # create solid sample class
    sample = solid_sample(problem_description)

    # validate input from the user
    sample.validate_input(problem_description)

    # assign properties
    sample.assign_properties(problem_description)

    # call the respective algorithm
    print(f"Solving {problem_description['problem_type']} problem")
    if problem_description["problem_type"] == "direct":
        direct_solver(sample, problem_description, calc_Fo, calc_Upsilon,
                      matrix_A, vector_b, update_thermal_properties)
    elif problem_description["problem_type"] == "inverse":
        pass

    computing_time = time.time() - time_start
    print(f"Time taken for {problem_description['problem_type']}"
          f" problem: {np.round(computing_time/60, 2)} minutes")
    solution = {"sample": sample,
                "problem_description": problem_description,
                "computing_time": computing_time,
                "type": problem_description["problem_type"]}

    # store all the results generated as a pickle
    now = datetime.datetime.today()
    file_name = (f"{now.year}{now.month}{now.day}_{now.hour}{now.minute}"
                 f"{now.second}_material-{sample.material}_"
                 f"ihf-{problem_description['ihf_type']}")
    print(file_name)

    return solution
