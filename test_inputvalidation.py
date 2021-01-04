import unittest
from transient_heat_conduction.main_solver import main_solver
import numpy as np


class TestInputValidation(unittest.TestCase):

    # create problem description dictionary
    list_keys = ["depth", "x_divisions", "time_total", "temperature_ambient",
                 "temperature_initial"]
    problem_description_test = {key: 10 for key in list_keys}
    problem_description_test.update({entry[0]: entry[1] for entry in [
        ("material", "pmma"), ("problem_type", "direct"),
        ("properties_type", "constant"), ("boundcond_surface", "robin"),
        ("surface_losses_type", "non-linear"), ("absorptivity", 0.9),
        ("emissivity", 0.9), ("h_convective", 10),
        ("boundcond_back", "insulated"), ("ihf_type", "constant"),
        ("conductivity_subs", 0), ("material_type", "inert"),
        ("pre_exp_factor", 1), ("activation_energy", 1),
        ("heat_reaction", 1), ("reaction_order", 1)]})
    for property_name in ["conductivity_coeff", "density_coeff",
                          "heat_capacity_coeff"]:
        problem_description_test[property_name] = [1, None]

    def test_a_materialname(self):
        """Tests that the material name is not None"""
        self.problem_description_test["material"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)
        self.problem_description_test["material"] = 0

    def test_b_problemtype(self):
        """Tests that incorrect problem types are not allowed"""
        self.problem_description_test["problem_type"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)
        self.problem_description_test["problem_type"] = "direct"

    def test_c_numericinput(self):
        """Tests that numeric input is demanded from the user in those fields
        that require it"""
        for property_name in self.list_keys:
            self.problem_description_test[property_name] = None
            with self.assertRaises(SystemExit) as cm:
                main_solver(self.problem_description_test)
            self.assertEqual(cm.exception.code, 1)
            self.problem_description_test[property_name] = 10

    def test_d_propertiestype(self):
        """Tests that incorrect properties type are not allowed"""
        self.problem_description_test["properties_type"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)
        self.problem_description_test["properties_type"] = "constant"

    def test_e_thermalproperties_constant(self):
        """Test that input to the thermo-physical properties is correct, for
        constant and temperature dependent properties properties"""
        for property_name in ["conductivity_coeff", "density_coeff",
                              "heat_capacity_coeff"]:

            # test base value needs to be correct
            self.problem_description_test[property_name][0] = None
            with self.assertRaises(SystemExit) as cm:
                main_solver(self.problem_description_test)
            self.assertEqual(cm.exception.code, 1)
            self.problem_description_test[property_name][0] = 1

            # test that the exponent is None if properties are constant
            self.problem_description_test[property_name][1] = 1
            with self.assertRaises(SystemExit) as cm:
                main_solver(self.problem_description_test)
            self.assertEqual(cm.exception.code, 1)
            self.problem_description_test[property_name][1] = None

    def test_f_thermalproperties_dependent(self):
        """Tests that exponent if a float if the properties depend on
        temperature"""
        self.problem_description_test["properties_type"
                                      ] = "temperature_dependent"
        for property_name in ["conductivity_coeff", "density_coeff",
                              "heat_capacity_coeff"]:
            self.problem_description_test[property_name][1] = None
            with self.assertRaises(SystemExit) as cm:
                main_solver(self.problem_description_test)
            self.assertEqual(cm.exception.code, 1)
            self.problem_description_test[property_name][1] = 1
        self.problem_description_test["properties_type"] = "constant"
        for property_name in ["conductivity_coeff", "density_coeff",
                              "heat_capacity_coeff"]:
            self.problem_description_test[property_name] = [1, None]

    def test_g_temperatureinitial(self):
        """Tests that an array of the adequate shape is given if the initial
        temperature is an array and not a float"""
        self.problem_description_test["temperature_initial"] = np.linspace(
            0, 10, self.problem_description_test["x_divisions"] - 1)
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)
        self.problem_description_test["temperature_initial"] = 10

    def test_h_boundcondsurface(self):
        """Tests that the correct boundary surface condition is passed by the
        user"""
        self.problem_description_test["boundcond_surface"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)
        self.problem_description_test["boundcond_surface"] = "robin"

    def test_i_boundcond_dirichlet(self):
        """Test that the correct parameters are provided for dirichlet boundary
        condition"""
        self.problem_description_test["boundcond_surface"] = "dirichlet"
        self.problem_description_test["temperature_surface"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)

    def test_j_boundcond_neunman(self):
        """Tests that the correct parameters are provided for neunman boundary
        condition"""
        self.problem_description_test["boundcond_surface"] = "neunman"
        self.problem_description_test["nhf"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)
        self.problem_description_test["boundcond_surface"] = "robin"

    def test_k_boundcond_robin(self):
        """Tests that a robin boundary condition is correctly defined"""
        self.problem_description_test["ihf_type"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)

        # constant heat flux
        self.problem_description_test["ihf_type"] = "constant"
        self.problem_description_test["ihf_coefficients"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)

        # polynomial heat flux
        for ihf_type in ["polynomial", "sinusoidal"]:
            self.problem_description_test["ihf_type"] = ihf_type
            self.problem_description_test["ihf_coefficients"] = ["value", 2, 3]
            with self.assertRaises(SystemExit) as cm:
                main_solver(self.problem_description_test)
            self.assertEqual(cm.exception.code, 1)
        self.problem_description_test["ihf_type"] = "constant"
        self.problem_description_test["ihf_coefficients"] = 10

    def test_l_surfacelosses(self):
        """Tests that surface losses is correctly defined and parameters are
        adequately passed"""
        self.problem_description_test["surface_losses_type"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)

        # linear surface losses
        self.problem_description_test[
            "surface_losses_type"] = "linear"
        self.problem_description_test["h_total"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)

        # non-linear surface losses
        self.problem_description_test[
            "surface_losses_type"] = "non-linear"
        for property_name in ["h_convective", "absorptivity", "emissivity"]:
            self.problem_description_test[property_name] = None
            with self.assertRaises(SystemExit) as cm:
                main_solver(self.problem_description_test)
            self.assertEqual(cm.exception.code, 1)
            self.problem_description_test[property_name] = 10

    def test_m_backboundcond(self):
        """Tests that the back face boundary condition is correctly defined
        and adequate parameters are passed"""
        self.problem_description_test["boundcond_back"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)

        self.problem_description_test["boundcond_back"] = "conductive_losses"
        self.problem_description_test["conductivity_subs"] = None,
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)
        self.problem_description_test["boundcond_back"] = "insulated"

    def test_n_pyrolysis(self):
        """Tests that if the solid is considered as reactive, the parameters
        are correctly defined"""
        self.problem_description_test["material_type"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)

        self.problem_description_test["material_type"] = "reactive"
        for property_name in ["pre_exp_factor", "activation_energy",
                              "heat_reaction", "reaction_order"]:
            self.problem_description_test[property_name] = None
            with self.assertRaises(SystemExit) as cm:
                main_solver(self.problem_description_test)
            self.assertEqual(cm.exception.code, 1)
            self.problem_description_test[property_name] = 1

    def test_o_indepth_absorp(self):
        """Tests the indepth absorptivity value needs to be a float"""
        self.problem_description_test["in-depth_absorptivity"] = None
        with self.assertRaises(SystemExit) as cm:
            main_solver(self.problem_description_test)
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
