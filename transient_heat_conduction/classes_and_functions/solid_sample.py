"""
Defines the sample class which is used to validate all the input data provided
and will contain the information required to implement the Crank-Nicolson
scheme.
"""

import numpy as np
import sys


class solid_sample():
    """
    Contains all the geometrical and thermophysical properties of the sample
    as well as the description of the thermal environment. Additionally,
    validates input.
    """

    def __init__(self, problem_description):
        """initiliazes the class"""

        # geometry
        # -------
        self.depth = problem_description["depth"]
        self.space_mesh = np.linspace(0, self.depth, problem_description[
            "x_divisions"])
        self.time_total = problem_description["time_total"]

        # thermophysical properties (at time = 0)
        # ---------------------------------------
        self.base_array = np.zeros_like(self.space_mesh)

        self.conductivity = self.base_array + problem_description[
            "conductivity"]
        self.conductivity_exp = problem_description[
            "conductivity_exp"]
        self.density = self.base_array + problem_description["density"]
        self.density_exp = problem_description["density_exp"]
        self.heat_capacity = self.base_array + problem_description[
            "heat_capacity"]
        self.heat_capacity_exp = problem_description[
            "heat_capacity_exp"]

        # thermal environment
        # -------------------
        self.temperature_ambient = problem_description["temperature_ambient"]
        self.temperature_initial = problem_description["temperature_initial"]

        if problem_description["boundcond_surface"] == "dirichlet":
            self.temperature_surface = problem_description[
                "temperature_surface"]
        elif problem_description["boundcond_surface"] == "neunman":
            self.nhf = problem_description["nhf"]
        elif problem_description["boundcond_surface"] == "robin":

            self.ihf_coeffs = problem_description["ihf_coefficients"]

            if problem_description["surface_losses_type"] == "linear":
                self.h_total = problem_description["h_total"]
            elif problem_description["surface_losses_type"] == "non-linear":
                self.h_conv = problem_description["h_convective"]
                self.absorptivity = problem_description["absorptivity"]
                self.emissivity = problem_description["emissivity"]

        if problem_description["boundcond_back"] == "insulated":
            pass
        elif problem_description["boundcond_back"] == "conductive_losses":
            self.conductivity_subs = problem_description[
                "conductivity_subs"]

        # pyrolysis
        # ---------
        if problem_description["material_type"] == "reactive":
            self.pre_exp_factor = problem_description["pre-exp_factor"]
            self.activation_energy = problem_description["activation_energy"]
            self.heat_reaction = problem_description["heat_reaction"]
            self.reaction_order = problem_description["reaction_order"]

        # miscelaneous
        # ------------
        self.material = problem_description["material"]

    def validate(self, problem_description):
        """
        Validates the input provided by the user
        """
        exit_value = False

        # validate problem type
        if problem_description["problem_type"] not in ["direct", "inverse"]:
            print("Problem type not valid")
            sys.exit(1)

        # validate properties type
        if problem_description["properties_type"] not in [
                "constant", "temperature_dependent"]:
            print("Properties type not valid.")
            sys.exit(1)

        # validate the surface boundary condition type
        if problem_description["boundcond_surface"] not in [
                "dirichlet", "neunman", "robin"]:
            print("Surface boundary condition not valid")
            sys.exit(1)

        # validate type of incident heat flux
        if problem_description["ihf_type"] not in [
                "constant", "polynomial", "sinusoidal", None]:
            print("IHF type nto valid.")
            sys.exit(1)

        # validate surface losses type
        if problem_description["surface_losses_type"] not in ["linear",
                                                              "non-linear"]:
            print("Surface losses type not valid.")
            sys.exit(1)

        # validate back surface boundary condition
        if problem_description["boundcond_back"] not in ["insulated",
                                                         "conductive_losses"]:
            print("Boundary condition of back suface not valid.")
            sys.exit(1)

        # validate all numerical input
        for property_name in ["depth", "x_divisions", "conductivity",
                              "density", "heat_capacity",
                              "temperature_ambient", "temperature_initial"]:
            try:
                float(problem_description[property_name])
            except ValueError:
                print(f"{property_name} not valid.")
                exit_value = True

        # validate numerical exponents if temperature dependent properties
        if (problem_description["properties_type"] ==
                "temperature_dependent"):

            for property_name in ["conductivity_exp", "density_exp",
                                  "heat_capacity_exp"]:
                try:
                    float(problem_description["property_name"])
                except ValueError:
                    print(f"{property_name} not valid.")
                    exit_value = True

        if exit_value:
            sys.exit(1)

    def additional_properties(self, problem_description):
        """
        Calculates additional properties, only called after input validation
        is performed
        """
        self.diffusivity = self.conductivity/self.density/self.heat_capacity
        self.thermal_inertia = (self.conductivity * self.density *
                                self.heat_capacity)
        self.dx = self.space_mesh[1] - self.space_mesh[0]
        self.dt = (1/3)*(self.dx**2/self.diffusivity)
        self.temporal_mesh = np.arange(0, self.time_total, self.dt[0])

        # initialise temperature arrays
        self.temperature_present = self.base_array + self.temperature_initial
        self.temperature_future = self.temperature_present.copy()

        # creat ihf array
        self.base_array_time = np.zeros_like
