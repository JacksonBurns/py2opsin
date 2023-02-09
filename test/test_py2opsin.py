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
            "methane",
            "water",
        )

    def test_name_to_smiles(self):
        """ """
        print(py2opsin("ethane"))


if __name__ == "__main__":
    unittest.main()
