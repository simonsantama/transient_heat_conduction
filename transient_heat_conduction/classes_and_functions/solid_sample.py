"""
Defines the sample class which is used to validate all the input data provided
and will contain the information required to implement the Crank-Nicolson
scheme.
"""

import numpy as np
import sys
import pandas as pd


class solid_sample():
    """
    Contains all the geometrical and thermophysical properties of the sample
    as well as the description of the thermal environment. Additionally,
    validates input.
    """

    def __init__(self, problem_description):
        """initiliazes the class"""
        self.material = problem_description["material"]

    def validate_input(self, problem_description):
        """validates the input provided by the user"""

        # validate material name
        if problem_description["material"] is None:
            print("Error, material not valid")
            sys.exit(1)
        # validate problem type
        if problem_description["problem_type"] not in ["direct", "inverse"]:
            print("Error, problem type not valid")
            sys.exit(1)
        # validate properties type
        if problem_description["properties_type"] not in [
                "constant", "temperature_dependent"]:
            print("Error, properties type not valid")
            sys.exit(1)

        # validate numerical input
        exit_value = False
        for property_name in ["depth", "x_divisions", "time_total",
                              "temperature_ambient", "temperature_initial",
                              ]:
            # don't check temperature initial as a float if it is an array
            if (property_name == "temperature_initial") and (
                    isinstance(problem_description[property_name],
                               np.ndarray)):
                continue
            try:
                float(problem_description[property_name])
            except (ValueError, TypeError):
                print(f"Error, {property_name} not valid")
                exit_value = True
        if exit_value:
            sys.exit(1)

        # validate numerical input for thermal properties
        for property_name in ["conductivity_coeff", "density_coeff",
                              "heat_capacity_coeff"]:
            # validate the base value
            try:
                float(problem_description[property_name][0])
            except (ValueError, TypeError):
                print(f"Error, base {property_name.split('_')[0]} not valid")
                exit_value = True
            # validate the exponent
            if problem_description["properties_type"] == "constant":
                if problem_description[property_name][1] is not None:
                    print("Error, exponent for constant "
                          f"{property_name.split('_')[0]} not valid")
                    exit_value = True
            elif problem_description[
                    "properties_type"] == "temperature_dependent":
                try:
                    float(problem_description[property_name][1])
                except (ValueError, TypeError):
                    print("Error, exponent for temperature dependent "
                          f"{property_name.split('_')[0]} not valid")
                    exit_value = True
            if exit_value:
                sys.exit(1)

        # validate initial temperature if array
        if isinstance(problem_description["temperature_initial"], np.ndarray):
            if not problem_description["x_divisions"] == len(
                    problem_description["temperature_initial"]):
                print("Error, size of the initial temperature array not valid")
                sys.exit(1)

        # validate the surface boundary condition
        if problem_description["boundcond_surface"] not in [
                "dirichlet", "neunman", "robin"]:
            print("Error, surface boundary condition not valid")
            sys.exit(1)
        exit_value = False
        # dirichlet
        if problem_description["boundcond_surface"] == "dirichlet":
            try:
                float(problem_description["temperature_surface"])
            except (ValueError, TypeError):
                print("Error, surface temperature for dirichlet boundary "
                      "condition not valid")
                exit_value = True
        # neunman
        elif problem_description["boundcond_surface"] == "neunman":
            try:
                float(problem_description["nhf"])
            except (ValueError, TypeError):
                print("Error, net heat flux for neunman boundary condition"
                      " not valid")
                exit_value = True
        # robin
        elif problem_description["boundcond_surface"] == "robin":
            if problem_description["ihf_type"] not in ["constant",
                                                       "polynomial",
                                                       "sinusoidal"]:
                print("Error, ihf type not valid")
                sys.exit(1)
            # constant ihf
            elif problem_description["ihf_type"] == "constant":
                try:
                    float(problem_description["ihf_coefficients"])
                except (ValueError, TypeError):
                    print("Error, ihf coefficients not valid for constant ihf")
                    exit_value = True
            # polynomial ihf
            elif problem_description["ihf_type"] == "polynomial":
                try:
                    np.array(problem_description["ihf_coefficients"],
                             dtype=float)
                except (ValueError, TypeError):
                    print("Error, ihf coefficients not valid for polynomial"
                          " ihf")
                    exit_value = True
            # sinusoidal ihf
            elif problem_description["ihf_type"] == "sinusoidal":
                if len(problem_description["ihf_coefficients"]) != 3:
                    print("Error, ihf coefficients not valid for sinusoidal"
                          " ihf")
                    sys.exit(1)
                try:
                    np.array(problem_description["ihf_coefficients"],
                             dtype=float)
                except (ValueError, TypeError):
                    print("Error, ihf coefficients not valid for sinusoidal"
                          " ihf")
                    exit_value = True

            # surface heat losses
            if problem_description[
                    "surface_losses_type"] not in ["linear", "non-linear"]:
                print("Error, surface losses not valid")
                sys.exit(1)
            # linear surface losses
            elif problem_description["surface_losses_type"] == "linear":
                try:
                    float(problem_description["h_total"])
                except (ValueError, TypeError):
                    print("Error, total heat transfer coefficient not valid")
                    exit_value = True
            # non-linear surface losses
            elif problem_description["surface_losses_type"] == "non-linear":
                for property_name in ["h_convective", "absorptivity",
                                      "emissivity"]:
                    try:
                        float(problem_description[property_name])
                    except (ValueError, TypeError):
                        print(f"Error, {property_name} not valid")
                        exit_value = True

        # back face boundary condition
        if problem_description["boundcond_back"] not in ["insulated",
                                                         "conductive_losses"]:
            print("Error, back face boundary condition not valid")
            sys.exit(1)
        elif problem_description["boundcond_back"] == "conductive_losses":
            try:
                float(problem_description["conductivity_subs"])
            except (ValueError, TypeError):
                print("Error, conductivity of substrate material not valid")
                exit_value = True
        if exit_value:
            sys.exit(1)

        # pyrolysis
        exit_value = False
        if problem_description["material_type"] not in ["inert", "reactive"]:
            print("Error, material type not valid")
            sys.exit(1)
        elif problem_description["material_type"] == "reactive":
            for property_name in ["pre_exp_factor", "activation_energy",
                                  "heat_reaction", "reaction_order"]:
                try:
                    float(problem_description[property_name])
                except (ValueError, TypeError):
                    print(f"Error, {property_name} not valid")
                    exit_value = True
            if exit_value:
                sys.exit(1)

        # in-depth absorption
        try:
            float(problem_description["in-depth_absorptivity"])
        except (ValueError, TypeError):
            print("Error, in-depth absorptivity not valid")
            exit_value = True
        if exit_value:
            sys.exit(1)

    def assign_properties(self, problem_description):
        """Assigns properties given by the user to the sample class and
        calculates additional parameters"""

        # geometry
        # -------
        self.depth = problem_description["depth"]
        self.x_divisions = problem_description["x_divisions"]
        self.space_mesh = np.linspace(0, self.depth, self.x_divisions)
        self.time_total = problem_description["time_total"]

        # termophysical properties
        # -------------------------
        base_array_space = np.zeros_like(self.space_mesh)
        conductivity_0 = base_array_space + problem_description[
            "conductivity_coeff"][0]
        density_0 = base_array_space + problem_description[
            "density_coeff"][0]
        heat_capacity_0 = base_array_space + problem_description[
            "heat_capacity_coeff"][0]

        diffusivity_0 = conductivity_0/density_0/heat_capacity_0
        self.dx = self.space_mesh[1] - self.space_mesh[0]
        self.dt = (1/6)*(self.dx**2/diffusivity_0)
        self.temporal_mesh = np.arange(0, self.time_total, self.dt[0])

        # values are stored in DataFrames where columns names are time stamps
        self.conductivity = pd.DataFrame(columns=self.temporal_mesh)
        self.density = self.conductivity.copy(deep=True)
        self.heat_capacity = self.conductivity.copy(deep=True)
        self.fo = self.conductivity.copy(deep=True)
        self.upsilon = self.conductivity.copy(deep=True)
        self.temperatures = self.conductivity.copy(deep=True)
        if not isinstance(problem_description[
                "temperature_initial"], np.ndarray):
            temperature_initial_0 = base_array_space + problem_description[
                "temperature_initial"]
        else:
            temperature_initial_0 = problem_description["temperature_initial"]
        for property_name, data in [(self.conductivity, conductivity_0),
                                    (self.density, density_0),
                                    (self.heat_capacity, heat_capacity_0),
                                    (self.temperatures,
                                     temperature_initial_0)]:
            property_name.iloc[:, 0] = data

        # heat transfer environment
        # -------------------------
        self.temperature_ambient = problem_description["temperature_ambient"]

        # surface boundary condition
        if problem_description["boundcond_surface"] == "dirichlet":
            self.temperature_surface = problem_description[
                "temperature_surface"]
        elif problem_description["boundcond_surface"] == "neunman":
            self.nhf = problem_description["nhf"]
        elif problem_description["boundcond_surface"] == "robin":

            # incident heat flux
            self.ihf_coeffs = problem_description["ihf_coefficients"]
            if problem_description["ihf_type"] == "constant":
                self.ihf = np.zeros_like(
                    self.temporal_mesh) + self.ihf_coeffs
            elif problem_description["ihf_type"] == "polynomial":
                ihf_terms = []
                for exp, coeff in enumerate(self.ihf_coeffs):
                    ihf_terms.append(coeff * self.temporal_mesh**exp)
                    self.ihf = sum(ihf_terms)
            elif problem_description["ihf_type"] == "sinusoidal":
                self.ihf = self.ihf_coeffs[0] * np.sin(
                    self.ihf_coeffs[1]*self.temporal_mesh + self.ihf_coeffs[2])

            # surface heat losses
            if problem_description["surface_losses_type"] == "linear":
                self.h_total = problem_description["h_total"]
            elif problem_description["surface_losses_type"] == "non-linear":
                self.h_conv = problem_description["h_convective"]
                self.absorptivity = problem_description["absorptivity"]
                self.emissivity = problem_description["emissivity"]
                self.stefan_boltz = 5.67e-8

        # back face boundary condition
        if problem_description["boundcond_back"] == "conductive_losses":
            self.conductivity_subs = problem_description[
                "conductivity_subs"]

        # pyrolysis
        # ---------
        self.pre_exp_factor = 0
        self.activation_energy = 0
        self.heat_reaction = 0
        self.reaction_order = 0
        for prop, property_name in [
                (self.pre_exp_factor, "pre_exp_factor"),
                (self.activation_energy, "activation_energy"),
                (self.heat_reaction, "heat_reaction"),
                (self.reaction_order, "reaction_order")]:
            if problem_description[property_name] is None:
                prop = 0
            else:
                prop = problem_description[property_name]
        self.omega_dots = self.conductivity.copy(deep=True)
        self.g_dots = self.conductivity.copy(deep=True)
        self.R = 8.314

        # in-depth absorption
        # -------------------
        self.indepth_absorptivity = problem_description[
            "in-depth_absorptivity"]
