"""
Main script.
This script is called by other algorithms, wishing to use the heat transfer
solver.

1-D heat transfer solver.
Direct or inverse heat transfer problemns.
Constant or variable properties.
Homogenous solid.

"""
import sys
import time
import numpy as np
import datetime

# import from local project
from classes_and_functions.solid_sample import solid_sample
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

        Function takes as input a single dictionary, formatted in the
        following with the following keys:

            geometry
            --------
            "problem_type": "direct" or "inverse"
            "depth": depth of the sample in m.
            "x_divisions": number of divisions to create spatial mesh

            thermophysical properties
            ------------------------------------
            "properties_type": "constant" or "temperature_dependent". If
            temperature dependence is considered, then the following form is
            assumed: X(T) = Xo(T/300)^exp, where Xo is the value provided and
            exp needs to be additionally specified

            "conductivity": conductivity in W/mK
            "conductivity_exp": exponent for temperature dependence
            "density": density in kg/m3
            "density_exp": exponent for temperature dependence
            "heat_capacity": heat capacity in J/kgK
            "heat_capacity_exp": exponent for temperature dependence

            thermal environment
            -------------------
            "temperature_ambient": ambient temperature in K.
            "temperature_initial": initial temperature in K.
            "boundcond_surface" "dirichlet", "neunman" or "robin"

            if "dirichlet":
                "temperature_surface": constant surface temperature in K.

            elif "neunman":
                "nhf": constant Net Heat Flux in W/m2.

            elif "robin":
                "ihf_type": "constant", "polynomial", "sinusoidal"
                for inverse type problems
                "ihf_coefficients": list of coefficients to reconstruct the
                ihf vs time curve in W/m2.

                "surface_losses_type": "linear", "non-linear"

                    if "linear":
                        "h_total": total (constant) heat transfer coefficient
                    if "non-linear":
                        absorptivity: surface absorptivity (constant)
                        emissivity: surface emissivity (constant)

            "boundcond_back": "insulated" or "conductive_losses":
                "insulated": no additional parameters required.
                "conductive_losses": null contact resistance assumed.
                if "conductive_losses":
                    "conductivity_subs": thermal conductivity of substrate
                    material in W/mK

            pyrolysis:
            ---------
            "material_type": "inert" or "reactive"
            if "reactive":
                accomodates for a single order, first order in fuel
                Arrhenius type reacion.
                "pre-exp_factor": pre-exponential factor in 1/s 10^-6
                "activation_energy": activation energy in kJ/mol
                "heat_reaction": heat of reaction in kJ/kg
                "reaction_order": reaction order.

            miscelaneous:
            ------------
            "material": material (if real). Used for file name.

        If any value is not needed, pass None.


    Returns
    -------
    solution: DICT
        Contains all the description of the problem as well as the full
        temperature profile discretized over the calculated spatial and
        temporal grids.

    """

    time_start = time.time()

    # create solid sample class
    sample = solid_sample(problem_description)

    # validate input from the user
    sample.validate(problem_description)
    
    # calculate additional properties for the sample class
    sample.additional_properties(problem_description)

    # # call the respective algorithm
    # if problem_description["problem_type"] == "direct":
    #     print("Solving a direct heat transfer problem")
    #     result = direct_solver(sample, problem_description)
    # elif problem_description["problem_type"] == "inverse":
    #     print("Solving an inverse problem")
    #     result = 0

    # computing_time = time.time() - time_start
    # print(
    #     f"Time taken for {problem_description['problem_type']}"
    #     f" problem: {np.round(computing_time, 2)} minutes")
    # solution = {"result": result, "sample": sample,
    #             "problem_description": problem_description,
    #             "computing_time": computing_time,
    #             "type": problem_description["problem_type"]}

    # # stored all the results generated as a pickle
    # now = datetime.datetime.today()
    # file_name = (f"{now.year}{now.month}{now.day}_{now.hour}{now.minute}"
    #              f"{now.second}_material-{sample.material}")
    # print(file_name)

    return sample
