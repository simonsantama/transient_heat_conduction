"""
Functions to calculate the analytical solutions to the heat diffusion
equation for validation
"""

import numpy as np
from scipy import special


def calc_dirichlet(solution, t):
    """Analytical solution for a dirichlet boundary condition"""
    s = solution["sample"]
    diffusivity = (s.conductivity.iloc[0, 0] / s.density.iloc[0, 0] /
                   s.heat_capacity.iloc[0, 0])
    temperature_initial = solution["problem_description"][
        "temperature_initial"]

    temperature_profile = (s.temperature_surface + (
        temperature_initial - s.temperature_surface) * special.erf(
            s.space_mesh / 2 / np.sqrt(diffusivity * t)))

    return temperature_profile


def calc_neunman(solution, t):
    """Analytical solution for a neunman boundary condition"""
    s = solution["sample"]
    diffusivity = (s.conductivity.iloc[0, 0] / s.density.iloc[0, 0] /
                   s.heat_capacity.iloc[0, 0])
    temperature_initial = solution["problem_description"][
        "temperature_initial"]
    q = solution["problem_description"]["nhf"]

    temperature_profile = (temperature_initial + (2 * q /
                                                  s.conductivity.iloc[0, 0]) *
                           np.sqrt(diffusivity * t / np.pi) * np.exp(
                               - s.space_mesh**2 / (4 * diffusivity * t)) -
                           (q * s.space_mesh / s.conductivity.iloc[0, 0]) *
                           special.erfc(s.space_mesh / 2 / np.sqrt(
                               diffusivity * t)))

    return temperature_profile


def calc_robin(solution, t):
    """Analytical solution for a robin boundary condition"""
    s = solution["sample"]
    diffusivity = (s.conductivity.iloc[0, 0] / s.density.iloc[0, 0] /
                   s.heat_capacity.iloc[0, 0])
    temperature_initial = solution["problem_description"][
        "temperature_initial"]
    h = solution["problem_description"]["h_convective"]

    temperature_profile = 0

    return temperature_profile
    
    
