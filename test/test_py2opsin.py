import os
import sys
import unittest

from py2opsin import py2opsin


class Test_py2opsin(unittest.TestCase):
    """
    Test the various functionalities of py2opsin.
    """

    @classmethod
    def setUpClass(self):
        self.jar_path = os.path.join(
            os.getcwd(),
            "opsin-cli-2.7.0-jar-with-dependencies.jar",
        )

        self.chemical_names = (
            "ethane",
            "water",
            "phenylalanine",
            "(2S)-2-azaniumyl-3-phenylpropanoate",
        )

        self.chemical_smiles = (
            "CC",
            "O",
            "N[C@@H](CC1=CC=CC=C1)C(=O)O",
            "[NH3+][C@H](C(=O)[O-])CC1=CC=CC=C1",
        )

        self.chemical_stdinchis = (
            "InChI=1S/C2H6/c1-2/h1-2H3",
            "InChI=1S/H2O/h1H2",
            "InChI=1S/C9H11NO2/c10-8(9(11)12)6-7-4-2-1-3-5-7/h1-5,8H,6,10H2,(H,11,12)/t8-/m0/s1",
            "InChI=1S/C9H11NO2/c10-8(9(11)12)6-7-4-2-1-3-5-7/h1-5,8H,6,10H2,(H,11,12)/t8-/m0/s1",
        )

        self.chemical_stdinchikeys = (
            "OTMSDBZUPAUEDD-UHFFFAOYSA-N",
            "XLYOFNOQVPJJNP-UHFFFAOYSA-N",
            "COLNVLDHVKWLRT-QMMMGPOBSA-N",
            "COLNVLDHVKWLRT-QMMMGPOBSA-N",
        )

        self.chemical_inchi_fixedH = (
            "InChI=1/C2H6/c1-2/h1-2H3",
            "InChI=1/H2O/h1H2",
            "InChI=1/C9H11NO2/c10-8(9(11)12)6-7-4-2-1-3-5-7/h1-5,8H,6,10H2,(H,11,12)/t8-/m0/s1/f/h11H",
            "InChI=1/C9H11NO2/c10-8(9(11)12)6-7-4-2-1-3-5-7/h1-5,8H,6,10H2,(H,11,12)/t8-/m0/s1/f/h10H",
        )

        self.chemical_extendedsmiles = (
            "CC |$_AV:1;2$|",
            "O |$_AV:O$|",
            "N[C@@H](CC1=CC=CC=C1)C(=O)O |$_AV:N;alpha;beta;1;2;3;4;5;6;;O';O$|",
            "[NH3+][C@H](C(=O)[O-])CC1=CC=CC=C1 |$_AV:1;2;1;O';O;3;1;2;3;4;5;6$|",
        )

        self.chemical_info = [
            {
                "name": name,
                "smiles": smiles,
                "stdinchi": stdinchi,
                "stdinchikey": stdinchikey,
                "inchi_fixedH": inchi_fixedH,
                "extendedsmiles": extendedsmiles,
            }
            for name, smiles, stdinchi, stdinchikey, inchi_fixedH, extendedsmiles in zip(
                self.chemical_names,
                self.chemical_smiles,
                self.chemical_stdinchis,
                self.chemical_stdinchikeys,
                self.chemical_inchi_fixedH,
                self.chemical_extendedsmiles,
            )
        ]

    def test_helpful_warning(self):
        """Raise warnings when input cannot be parsed."""
        with self.assertWarns(RuntimeWarning):
            py2opsin(["Methane is an IUPAC Name", "I Have to Fly Planes"])

    def test_invalid_output_spec(self):
        """Invalid output specification should raise a runtime error."""
        with self.assertRaises(RuntimeError):
            py2opsin("ethane", "notvalid")

    def test_invalid_output_helpful_error(self):
        """Typo in the output specification should be greeted with helpful error."""
        with self.assertRaises(RuntimeError) as helpful_error:
            py2opsin("ethane", "SMOLES")
        self.assertEqual(
            str(helpful_error.exception),
            "Output format SMOLES is invalid. Did you mean 'SMILES'?",
        )

    def test_name_to_smiles(self):
        """
        Tests converting IUPAC names to SMILES strings
        """
        for test_info in self.chemical_info:
            opsin_smiles = py2opsin(test_info["name"])
            self.assertEqual(opsin_smiles, test_info["smiles"])

        test_list_smiles = py2opsin(self.chemical_names)
        self.assertEqual(test_list_smiles, list(self.chemical_smiles))

    def test_name_to_extendedsmiles(self):
        """
        Tests converting IUPAC names to Extended SMILES
        """
        for test_info in self.chemical_info:
            opsin_smiles = py2opsin(test_info["name"], output_format="ExtendedSMILES")
            self.assertEqual(opsin_smiles, test_info["extendedsmiles"])

        test_list_extendedsmi = py2opsin(
            self.chemical_names, output_format="ExtendedSMILES"
        )
        self.assertEqual(test_list_extendedsmi, list(self.chemical_extendedsmiles))

    def test_name_to_stdinchi(self):
        """
        Tests converting IUPAC names to standard InChI
        """
        for test_info in self.chemical_info:
            opsin_smiles = py2opsin(test_info["name"], output_format="StdInChI")
            self.assertEqual(opsin_smiles, test_info["stdinchi"])

        test_list_stdinchis = py2opsin(self.chemical_names, output_format="StdInChI")
        self.assertEqual(test_list_stdinchis, list(self.chemical_stdinchis))

    def test_name_to_stdinchikey(self):
        """
        Tests converting IUPAC names to standard InChI keys
        """
        for test_info in self.chemical_info:
            opsin_smiles = py2opsin(test_info["name"], output_format="StdInChIKey")
            self.assertEqual(opsin_smiles, test_info["stdinchikey"])

        test_list_stdinchikeys = py2opsin(
            self.chemical_names, output_format="StdInChIKey"
        )
        self.assertEqual(test_list_stdinchikeys, list(self.chemical_stdinchikeys))

    def test_name_to_inchi_fixedh(self):
        """
        Tests converting IUPAC names to standard InChI with fixed H
        """
        for test_info in self.chemical_info:
            opsin_inchi = py2opsin(test_info["name"], output_format="InChI")
            self.assertEqual(opsin_inchi, test_info["inchi_fixedH"])

        test_list_inchi = py2opsin(self.chemical_names, output_format="InChI")
        self.assertEqual(test_list_inchi, list(self.chemical_inchi_fixedH))

    def test_name_to_cml(self):
        """
        Tests converting IUPAC names to CML format
        """
        opsin_cml = py2opsin("ethane", output_format="CML")
        data_path = os.path.join(os.getcwd(), "test", "data", "cml_test.cml")
        with open(data_path, encoding="unicode_escape") as f:
            test_cml = f.readlines()[0]

        self.assertEqual(opsin_cml, test_cml)

    def test_allow_multiple_options(self):
        """
        Test whether py2opsin can handle multiple arguments passed to it
        """
        test_inchi = py2opsin(
            chemical_name="ethane",
            output_format="InChI",
            allow_acid=True,
            allow_radicals=True,
            allow_bad_stereo=True,
            wildcard_radicals=True,
        )

        self.assertEqual(test_inchi, "InChI=1/C2H6/c1-2/h1-2H3")

    def test_list_with_errors(self):
        """
        Test whether OPSIN will return a list if there is at least one failed translation
        """
        list_with_errors = ["methane", "ethane", "blah", "water"]
        correct_list = ["C", "CC", "", "O"]
        with self.assertWarns(RuntimeWarning):
            smiles_list = py2opsin(list_with_errors)
        self.assertEqual(smiles_list, correct_list)


if __name__ == "__main__":
    unittest.main()
