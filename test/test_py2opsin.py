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
            "4-amino-4-phenylbutanoic acid",
        )

        self.chemical_smiles = (
            "CC",
            "O",
            "NC(CCC(=O)O)C1=CC=CC=C1",
        )

        self.chemical_stdinchis = (
            "InChI=1/C2H6/c1-2/h1-2H3",
            "InChI=1/H2O/h1H2",
            "InChI=1/C10H13NO2/c11-9(6-7-10(12)13)8-4-2-1-3-5-8/h1-5,9H,6-7,11H2,(H,12,13)/f/h12H",
        )

        self.chemical_stdinchikeys = (
            "",
            "",
            "",
        )

        self.chemical_inchi_fixedh = (
            "",
            "",
            "",
        )

        self.chemical_extendedsmiles = (
            "CC |$_AV:1;2$|",
            "O |$_AV:O$|" "NC(CCC(=O)O)C1=CC=CC=C1 |$_AV:N;4;3;2;1;O';O;1;2;3;4;5;6$|",
        )

        self.chemical_info = [
            {
                "name": name,
                "smiles": smiles,
                "stdinchi": stdinchi,
                "stdinchikey": stdinchikey,
                "inchi_fixedh": inchi_fixedh,
                "extendedsmiles": extendedsmiles,
            }
            for name, smiles, stdinchi, stdinchikey, inchi_fixedh, extendedsmiles in zip(
                self.chemical_names,
                self.chemical_smiles,
                self.chemical_stdinchis,
                self.chemical_stdinchikeys,
                self.chemical_inchi_fixedh,
                self.chemical_extendedsmiles,
            )
        ]

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

    def test_name_to_extendedsmiles(self):
        """
        Tests converting IUPAC names to Extended SMILES
        """
        # for test_info in self.chemical_info:
        # opsin_smiles = py2opsin(test_info['name'])
        # self.assertEqual(opsin_smiles, test_info['extendedsmiles'])

    def test_name_to_stdinchi(self):
        """ """
        pass

    def test_name_to_stdinchikey(self):
        """ """
        pass

    def test_name_to_inchi_fixedh(self):
        """ """
        pass

    def test_load_txt_file(self):
        """
        Test ability to load in a .txt file with species separated by lines
        """
        filename = os.path.join(os.getcwd(), "data", "example.txt")
        predictions = py2opsin(filename)
        # TODO: finish with actual implementation

    def test_allow_multiple_options(self):
        """
        Test whether py2opsin can handle multiple arguments passed to it
        """
        pass

    def test_output_to_file(self):
        """
        Test whether results can be successfully saved to a file
        """

        pass


if __name__ == "__main__":
    unittest.main()
