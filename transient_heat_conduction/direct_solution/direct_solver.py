"""
Direct heat transfer problem.
Obtain the temperature profile given the boundary conditions, the material
properties, the thermal environment and the initial condition.
"""
import numpy as np


def direct_solver(sample, problem_description, calc_Fo, calc_Upsilon,
                  matrix_A, vector_b, update_thermal_properties):
    """
    Solves the direct heat transfer problem, determinig the temperature
    profile from the sample and environment conditions.

    Parameters
    ----------
    sample : CLASS
        Class that contains all the information regarding the geometry and
        boundary conditions.

    problem_description: DICT
        Contains all the information used to create the sample class but
        additionally, information regarding the problem type (such as,
        temperature dependence of properties).

    calc_Fo: function
        Function that calculates the Fourier number

    calc_Upsilon: function
        Function that calculates the Upsilon parameter, defined in Appendix B.

    Returns
    -------
    None

    """
    # progress indicators
    progress_indicators = [25, 50, 75]

    # step forward over the temporal domain
    for t_step, t in enumerate(sample.temporal_mesh[:-1]):

        # print progress indicators
        for percentage in progress_indicators:
            if t > (sample.time_total*percentage/100):
                print(f" ... progress {percentage}%")
                progress_indicators.remove(percentage)
                break

        # calculate Fo and Upsilon (for this time step)
        calc_Fo(sample, t_step)
        if problem_description["properties_type"] == "constant":
            sample.upsilon.iloc[:, t_step] = np.zeros_like(
                sample.fo.iloc[:, t_step].values)
        elif problem_description[
                "properties_type"] == "temperature_dependent":
            calc_Upsilon(problem_description, sample, t_step)

        # define  matrix A
        A = matrix_A(problem_description, sample, t_step)

        # define vector b
        b = vector_b(problem_description, sample, t_step)

        # calculate temperatures for the next time step
        sample.temperatures.iloc[:, t_step + 1] = np.linalg.solve(A, b)

        # update thermal properties (to be used on the next time step)
        update_thermal_properties(problem_description, sample, t_step)

    return None
