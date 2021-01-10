"""
Calculates parameters that are used by the numerical solver
"""
import numpy as np


def calc_Fo(sample, t_step):
    """Returns the Fourier number as an array given the density, conductivity
    and heat capacity as DataFrames"""

    sample.fo.iloc[:, t_step] = (sample.conductivity.iloc[:, t_step] *
                                 sample.dt) / (
                                     sample.density.iloc[:, t_step] *
                                     sample.heat_capacity.iloc[:, t_step] *
                                     sample.dx**2)


def calc_Upsilon(problem_description, sample, t_step):
    """Calculates the Upsilon parameter, defined in my thesis Appendix B"""
    base, exp = problem_description["conductivity_coeff"]
    temperature_difference = np.zeros_like(sample.temperatures.iloc[:, t_step])
    temperature_difference[0] = (sample.temperatures.iloc[1, t_step] -
                                 sample.temperatures.iloc[0, t_step])
    for i in sample.temperatures.iloc[:-1, t_step]:
        if i == 0:
            continue
        temperature_difference[i] = (sample.temperatures.iloc[i+1, t_step] -
                                     sample.temperatures.iloc[i-1, t_step])
    temperature_difference[-1] = (sample.temperatures.iloc[-1, t_step] -
                                  sample.temperature.iloc[-2, t_step])
    sample.upsilon.iloc[:, t_step] = (
        exp * base / 300)*(sample.temperatures.iloc[:, t_step]**(exp-1))*(
            sample.dt/sample.density.iloc[:, t_step] /
            sample.heat_capacity.iloc[:, t_step] / sample.dx)*(
                temperature_difference/2/sample.dx)**2


def matrix_A(problem_description, sample, t_step):
    "Defines matrix A. Matrix of coefficient for the temperatures at t=n+1"
    A = np.diagflat(- sample.fo.iloc[:, t_step].values[:-1] / 2, -1) +\
        np.diagflat(1 + sample.fo.iloc[:, t_step].values[:]) +\
        np.diagflat(- sample.fo.iloc[:, t_step].values[1:] / 2, 1)

    # update edge values of A depending on the boundary conditions
    if problem_description["boundcond_surface"] == "dirichlet":
        A[0, 0] = 1
        A[0, 1] = 0
    # elif problem_description["boundcond_surface"] == "neunman":
    #     pass
    # elif problem_description["boundcond_surface"] == "robin":
    #     pass

    if problem_description["boundcond_back"] == "insulated":
        A[-1, -2] = - sample.fo.iloc[-2, t_step]
        A[-1, -1] = 1 + sample.fo.iloc[-1, t_step]
    # elif problem_description["boundcond_back"] == "conductive_losses":
    #     pass

    A = A.astype(float)

    return A


def vector_b(problem_description, sample, t_step):
    """Defines vector b, which is calculated from matrix B of coefficients
    at temperature t=n and accounts for extra terms from the  boundary
    conditions"""
    B = np.diagflat(sample.fo.iloc[:, t_step].values[:-1] / 2, -1) +\
        np.diagflat(1 - sample.fo.iloc[:, t_step].values[:]) +\
        np.diagflat(sample.fo.iloc[:, t_step].values[1:] / 2, 1)

    # calculate g_dot (source term - pyrolysis)
    sample.omega_dots.iloc[:, t_step] = (sample.density.iloc[:, t_step] *
                                         sample.pre_exp_factor *
                                         np.exp(- sample.activation_energy /
                                         sample. R /
                                         sample.temperatures.iloc[:,
                                                                  t_step]))

    sample.g_dots.iloc[:, t_step] = (sample.omega_dots.iloc[:, t_step] *
                                     sample.heat_reaction)

    b = B.dot(sample.temperatures.iloc[:, t_step]) +\
        sample.upsilon.iloc[:, t_step] - (sample.g_dots.iloc[:, t_step] *
                                          sample.dt /
                                          sample.density.iloc[:, t_step] *
                                          sample.heat_capacity.iloc[:,
                                                                    t_step])

    # update edge values of b depending on the boundary conditions
    if problem_description["boundcond_surface"] == "dirichlet":
        b.iloc[0] = problem_description["temperature_surface"]
    elif problem_description["boundcond_surface"] == "neunman":
        pass
    elif problem_description["boundcond_surface"] == "robin":
        pass

    if problem_description["boundcond_back"] == "insulated":
        b.iloc[-1] = (sample.fo.iloc[-2, t_step] *
                      sample.temperatures.iloc[-2, t_step] +
                      (1 - sample.fo.iloc[-1, t_step]) *
                      sample.temperatures.iloc[-1, t_step] +
                      sample.upsilon.iloc[-1, t_step] - (
                          sample.g_dots.iloc[-1, t_step] * sample.dt[-1]) /
                      (sample.density.iloc[-1, t_step] *
                       sample.heat_capacity.iloc[-1, t_step]))
    elif problem_description["boundcond_back"] == "conductive_losses":
        pass

    b = b.astype(float)

    return b


def update_thermal_properties(problem_description, sample, t_step):
    """Updates the thermal properties"""
    for prop, property_name in [(sample.conductivity, "conductivity"),
                                (sample.density, "density"),
                                (sample.heat_capacity, "heat_capacity")]:
        if problem_description["properties_type"] == "constant":
            prop.iloc[:, t_step+1] = prop.iloc[:, t_step]
        elif problem_description["properties_type"
                                 ] == "temperature_dependent":
            base, exponent = problem_description["property_name"]
            prop.iloc[:, t_step+1] = base * (
                sample.temperatures.iloc[:, t_step].values/300)**(exponent)
