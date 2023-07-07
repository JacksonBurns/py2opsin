import os
import sys
import time
import unittest

from pubchempy import PubChemHTTPError, get_compounds

from py2opsin import py2opsin


class Test_py2opsin_performance(unittest.TestCase):
    """
    Test the performance of py2opsin.
    """

    @classmethod
    def setUpClass(self):
        self.jar_path = os.path.join(
            os.getcwd(),
            "opsin-cli-2.7.0-jar-with-dependencies.jar",
        )
        # list of molecules taken from IUPAC Dissociation Constants dataset
        # https://zenodo.org/record/7236453
        self.compound_list = [
            'pyridine, 2-amino-',
            'pyridine, 3-iodo-',
            'pyridine, 3-methyl-',
            '1,4-Thiazine, tetrahydro-',
            'pyridine, 2-(2-aminoethyl)-',
            'aniline, 2,5-dichloro-',
            'aniline, N-n-propyl-',
            'benzylamine, N-ethyl-',
            'aniline, 4-methoxy-',
            'piperidine, 3-methyl-',
            'pyrazole, 3,5-dimethyl-',
            'quinoline, 8-amino-6-methoxy-',
            'pyridine, 4-phenyl-',
            'quinoline, 3-nitro-',
            'pyridine, 4-chloro-',
            'pyridine, 2-benzyl-',
            'Quinoline',
            'Pyridine 1-oxide',
            'aniline, 4-bromo-N,N-dimethyl-',
            'indole, 1,2-dimethyl-',
            'aniline, N-hydroxy-',
            'benzimidazole, 2-isopropyl-',
            'quinoline, 8-nitro-',
            'quinoline, 2,4,8-trimethyl-',
            'pyrimidine, 2-methoxy-',
            'quinoline, 6-bromo-',
            'aniline, 2,4-dinitro-',
            'aziridine, 2-ethyl-',
            'octane, 1,8-diamino-',
            '1,2,4-Thiadiazole, 5-amino-3-phenyl-',
            'pyrrole, 2-methyl-',
            'quinoline, 7-bromo-',
            'pyridine, 2-methoxy-',
            'quinoline, 4-methoxy-',
            'quinoline, 4-methyl-',
            'pyridine, 3,5-dimethyl-',
            'quinoline, 6-nitro-',
            'pyrrole, 2,4-dimethyl-',
            'aniline, 4-chloro-2-nitro-',
            'pyridine, 3-amino-',
            'quinoline, 3-chloro-',
            'quinoline, 5-nitro-',
            'quinoline, 7-bromo-4-chloro-',
            'quinoline, 2-amino-',
            'quinoline, 2-methyl-',
            '1,4-Thiazine',
            'isoquinoline, 5-amino-',
            'aniline, N-phenyl-',
            'pyrazine, 2,5-dimethyl-',
            'pyridine, 4-(5-phenyl-2-oxazolyl)-',
            'pyridine, 3-cyano-',
            'pyridine, 2-phenyl-',
            'pyridine, 4-methoxy-',
            'Pyrimidine',
            'quinoline, 6-chloro-',
            'pyrimidine, 2,5-diamino-',
            'pyridine, 2,4,6-trimethyl-',
            'pyrimidine, 4,6-dimethyl-',
            'pyridine, 4-iodo-',
            'quinoline, 7-chloro-',
            'aniline, 5-chloro-2-nitro-',
            'Quinuclidine',
            'aniline, 2,6-dichloro-4-nitro-',
            'isoquinoline, 3-amino-',
            'imidazole, 2-ethyl-',
            'quinoline, 2-bromo-',
            'quinoline, 2,8-dimethyl-',
            'azobenzene, 4-nitro-',
            'quinoline, 6-amino-',
            'pyridine, 4-bromo-',
            'pyridine, 2-pentyl-',
            'pyrimidine, 2-amino-4,6-dimethyl-',
            'piperazine, 1-methyl-4-nitroso-',
            'pyridine, 2-hexyl-',
            'isoquinoline, 4-bromo-',
            'pyridine, 2,3-dimethyl-',
            'Morpholine',
            'quinoline, 5-fluoro-',
            'aniline, 3-bromo-',
            'pyrimidine, 2,4,6-triamino-',
            'piperidine, 2,2,6,6-tetramethyl-',
            'pyridine, 2-bromo-',
            'pyrazine, tetramethyl-',
            'isoquinoline, 5-nitro-',
            '2-Pyrroline, 1,2-dimethyl-',
            'Pyridazine',
            'aniline, 2-bromo-4,6-dinitro-',
            'piperazine, 1-acetyl-',
            'quinoline, 7-nitro-',
            'pyrazole, 1,3-dimethyl-',
            'pyridine, 3-bromo-',
            'pyridine, 4-methyl-',
            'pyridine, 3-phenyl-',
            'pyridazine, 4-methyl-',
            'aniline, 2-iodo-',
            'pyrazine, trimethyl-',
            'pyrrolidine, 1-methyl-',
            'anthracene, 1-amino-',
            'azetidine, N-methyl-',
            'aniline, 2,4,6-trinitro-',
        ]

    @unittest.skipIf(os.path.exists(".no_perf_test"), "file .no_perf_test was found")
    def test_performance(self):
        """
        Test performance relative to pubchempy
        """
        # typical workflow of looking up names, saving in a list
        smiles_strings = []
        pubchempy_start = time.time()
        for compound in self.compound_list:
            # HTTP errors can happen
            for attempt in range(3):
                try:
                    result = get_compounds(compound, "name")
                    break
                except PubChemHTTPError:
                    pass
            # could possibly never get server access
            if attempt == 2:
                smiles_strings.append(None)
                continue
            try:
                smiles_strings.append(result[0].isomeric_smiles)
            except IndexError:
                smiles_strings.append(None)
        pubchempy_exe = time.time() - pubchempy_start

        smiles_strings = []
        py2opsin_start = time.time()
        smiles_strings = py2opsin(self.compound_list)
        py2opsin_exe = time.time() - py2opsin_start
        self.assertTrue(
            pubchempy_exe > py2opsin_exe,
            "py2opsin should be faster than pubchempy (py2opsin took {:.2f} seconds, pubchempy took {:.2f} seconds)".format(
                py2opsin_exe,
                pubchempy_exe,
            ),
        )


if __name__ == "__main__":
    unittest.main()
