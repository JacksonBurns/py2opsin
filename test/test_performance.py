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
        # list of 10 carbon molecules taken from wikipedia
        # https://en.wikipedia.org/wiki/List_of_compounds_with_carbon_number_10
        self.compound_list = [
            "dienochlor",
            "kepone",
            "perfluoronaphthalene",
            "perfluoroadamantanone",
            "perfluorodecalin",
            "perfluorodecyl iodide",
            "oxychlordane",
            "heptachlor",
            "heptachlor epoxide",
            "copper phenylethynylacetylenide",
            "ethyl perfluorooctanonate",
            "dichloro naphthalene",
            "quinomethionate",
            "flavianic acid",
            "alloxazine",
            "phenylmaleic anhydride",
            "chloro quinaldol",
            "anagrelide",
            "tridiphane",
            "dihydroheptachlor",
            "kynurenic acid",
            "thiabendazole",
            "azulene",
            "naphthalene",
            "pyrazon",
            "drazoxolon",
            "tetrachloro tetrahydro naphthalene",
            "1,4-benzenediacetonitrile",
            "phenylsuccinonitrile",
            "picrolonic acid",
            "phenylpropynoic acid methyl ester",
            "monophenyl succinic anhydride",
            "cis piperonylacrylic acid",
            "scopoletin",
            "chloro mercuri ferrocene",
            "acetylmandelic chloride",
            "captafol",
            "captafol",
            "tetrachlorvinphos",
            "isocyanobutanemolybdenum pentacarbonyl",
            "naphthylamine",
            "vinylphenylacetonitrile",
            "probenazole",
            "isocyanobutanetungsten pentacarbonyl",
            "bullvalene",
            "diisopropenyldiacetylene",
            "niobocene dichloride",
            "titanocene dichloride",
            "cobaltocene",
            "ferrocenium hexafluorophosphate",
            "ferrocene",
            "mercurocene",
            "magnesocene",
            "sulfadiazine",
            "nickelocene",
            "bullvalone",
            "cyclopropyl phenyl ketone",
            "cinnamyl formate",
            "methylbenzylglyoxal",
            "phenacylacetate",
            "benzylmalonic acid",
            "dimethyl phthalate",
            "piperonyl acetate",
            "pyrocatechol diacetate",
            "osmocene",
            "plumbocene",
            "stannocene",
            "vanadocene",
            "brallobarbital",
            "clofibric acid",
            "acetamiprid",
            "fluoridamid",
            "ethanol dmpfps",
            "iodobenzene diacetate",
            "benzenebutanenitrile",
            "cyclopropiophenone oxime",
            "ethyl oxanilate",
            "sulfasomizole",
            "nifuratel",
            "disodium inosinate",
            "cyclopropylphenylmethane",
            "tetralin",
            "beclamide",
            "carbanolate",
            "chlorpropham",
            "tranid",
            "norfenfluramine",
            "biacetyl phenylhydrazone",
            "cotinine",
            "allobarbital",
            "bentazone",
            "orotidine",
            "thiacetazone",
            "inosine",
            "anethole",
            "cinnamyl methyl ether",
            "cyclopropyl phenylmethanol",
            "isopropyl phenyl ketone",
            "eugenol",
            "acetonylguaiacol",
            "anisyl acetate",
            "ethyl anisate",
            "cantharidin",
            "diallyl maleate",
            "methyl everninate",
            "tetramethyltetrathiafulvalene",
            "tetramethyltetraselenafulvalene",
            "chlordimeform",
            "metoxuron",
            "procyazine",
            "chlorothymol",
            "tolylfluanid",
            "isobutyranilide",
            "butyl nicotinate",
            "homarylamine",
            "tenamfetamine",
            "guanosine",
            "deoxyadenosine",
            "adenosine",
            "deoxyguanosine",
            "cymene",
            "diethyl benzene",
            "tetrahydrotriquinacene",
            "clotermine",
            "zytron",
            "molybdenyl acetylacetonate",
            "nicotine",
            "nicotine",
            "nikethamide",
            "methallatal",
            "sultiame",
            "thymidine",
            "morinamide",
            "proxyphylline",
            "diprophylline",
            "nickel acetylacetonate",
            "benzenebutanol",
            "butoxybenzene",
            "carvone",
            "carvone",
            "chrysantenone",
            "durenol",
            "eucarvone",
            "isopiperitenone",
            "menthofuran",
            "myrtenal",
            "perillaldehyde",
            "pinocarvone",
            "piperitenone",
            "prehnitenol",
            "verbenone",
            "carvone oxide",
            "durohydroquinone",
            "elsholtzia ketone",
            "nepetalactone",
            "perilla ketone",
            "ethyl vanillylether",
            "ethylsyringol",
            "mephenesin",
            "adipic acid divinyl ester",
            "diallyl succinate",
            "butylthiobenzene",
            "isobutyl phenyl sulfide",
            "vinyldimethylphenylsilane",
            "benzenebutanamine",
            "geranonitrile",
            "methamphetamine",
            "phenpromethamine",
            "ephedrine",
            "hordenine",
            "perillartine",
            "etilefrine",
            "hydroxyephedrine",
            "modaline",
            "fenformin",
            "fonofos",
            "fenthion",
            "diethyl phenyl phosphate",
            "diethylphenylphosphine",
            "adamantane",
            "alpha cis ocimene",
            "alpha myrcene",
            "beta phellandrene",
            "beta terpinene",
            "bornylene",
            "camphene",
            "cis ocimene",
            "cyclodecyne",
            "isolimonene",
            "limonene",
            "perhydrotriquinacene",
            "protoadamantane",
            "santolina triene",
            "trans ocimene",
            "pipobroman",
            "decanedioyl dichloride",
            "triallate",
            "aminoparathion",
            "famophos",
            "decanedinitrile",
            "hexyl pyrazine",
            "hystrine",
            "smipine",
            "butabarbital",
            "butethal",
            "biotin",
            "EDDS",
            "adenosine triphosphate",
            "dipentaerythritol hexanitrate",
            "cimetidine",
            "artemiseole",
            "artemisia ketone",
            "camphor",
            "caranone",
            "carvotanaceton",
            "citral",
            "dihydrocarvone",
            "dihydrocarvone",
            "epicamphor",
            "hotrienol",
            "ipsdienol",
            "isocyclocitral",
            "isopinocamphone",
            "isopulegone",
            "lyratol",
            "myrtanal",
            "neroloxide",
            "phellandral",
            "pinocarveol",
            "piperitone",
            "pulegone",
            "pulegone",
            "thujol",
            "thujone",
            "ethoxydimethyl phenylsilane",
            "butyl sorbate",
            "diosphenol",
            "iridomyrmecin",
            "lilac aldehyde a",
            "lilac aldehyde b",
            "limonene dioxide",
            "massoialactone",
            "nerolic acid",
            "piperitone oxide",
            "pinonic acid",
            "triethylsuccinic anhydride",
            "diethyl isopropylidenemalonate",
            "triethyl methanetricarboxylate",
            "thiocamphor",
            "bornyl chloride",
            "octyl trichloroacetate",
            "cyclohexanebutyronitrile",
            "ecgonine methyl ester",
            "etrimfos",
            "pentaglycine",
            "cyclodecene",
            "ethylidenecyclooctane",
            "methylenecyclononane",
            "methylhydrindan",
            "thujane",
            "ipazine",
            "octyl dichloroacetate",
            "artemisia alcohol",
            "borneol",
            "camphene hydrate",
            "carvomenthone",
            "cis rose oxide",
            "cyclodecanone",
            "eucalyptol",
            "fenchyl alcohol",
            "fragranol",
            "grandisol",
            "ipsenol",
            "isogeraniol",
            "isomenthone",
            "isomenthone",
            "isopulegol",
            "menthone",
            "neodihydrocarveol",
            "piperitol",
            "sabinene hydrate",
            "santolina alcohol",
            "terpineol",
            "yomogi alcohol",
            "allyl heptanoate",
            "citronellic acid",
            "cyclohexanecarboxylic acid isopropyl ester",
            "cyclooctanol acetate",
            "decalinhydroperoxide",
            "sobrerol",
            "tagetonol",
            "valeric anhydride",
            "decanedioic acid",
            "diethyl propylmalonate",
            "hexanedioic acid monoethyl ester",
            "succinic acid diisopropyl ester",
            "triethylbutanedioic acid",
            "octyl bromoacetate",
            "phosphamidon",
            "decanoyl chloride",
            "octyl chloroacetate",
            "decanenitrile",
            "lupinine",
            "diethylaminoethyl methacrylate",
            "nonyl isothiocyanate",
            "leucylglycylglycine",
            "secbumeton",
            "terbutryn",
            "malathion",
            "malaoxon",
            "cyclodecane",
            "diethylcyclohexane",
            "diisoamylene",
            "nickel diethyldithiocarbamate",
            "mebutamate",
            "disulfiram",
            "carvomenthol",
            "cyclodecanol",
            "decanal",
            "dihydromyrcenol",
            "dihydroterpineol",
            "isocarvomenthol",
            "isomenthol",
            "menthol",
            "neocarvomenthol",
            "neoisocarvomenthol",
            "neoisomenthol",
            "rhodinol",
            "cyclopentadienyl pentamethyl disiloxane",
            "decanoic acid",
            "hydroxycitronellal",
            "neodecanoic acid",
            "terpinol",
            "isooctyl mercaptoacetate",
            "octyl thioglycolate",
            "diallyldiethoxysilane",
            "peroxydecanoic acid",
            "promoxolane",
            "pempidine",
            "perhydrophentermine",
            "propylhexedrine",
            "decanamide",
            "diethylcarbamazine",
            "decane",
            "diethyl cyclohexylaminophosphonate",
            "dipiperazinylethane",
            "butyl hexyl ether",
            "decanol",
            "heptyl propyl ether",
            "methyl nonyl ether",
            "tetrahydrolavandulol",
            "triisopropylmethanol",
            "tripropyl orthoformate",
            "pentyl sulfite",
            "diethylhexylamine",
            "diethylaminoacetaldehyde diethyl acetal",
            "hypusine",
            "butyloxytriethylsilane",
            "tripropyloxymethylsilane",
            "uranium pentaethylate",
            "spermine",
            "decamethylcyclopentasiloxane",
            "manganese technetium decacarbonyl",
            "dimanganese decacarbonyl",
            "hexacyanobutadiene radical",
            "dirhenium decacarbonyl",
            "ditechnetium decacarbonyl",
        ]

    def test_performance(self):
        """
        Test performance relative to pubchempy
        """
        # typical workflow of looking up names, saving in a list
        smiles_strings = []
        pubchempy_start = time.time()
        for compound in self.compound_list:
            try:
                result = get_compounds(compound, "name")
            except PubChemHTTPError:
                smiles_strings.append(None)
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
            "py2opsin should be faster than pubchempy",
        )
        self.assertTrue(
            pubchempy_exe / py2opsin_exe > 50,
            "speedup should be at least 50x relative to pubchempy",
        )


if __name__ == "__main__":
    unittest.main()
