<h1 align="center">py2opsin</h1> 
<h3 align="center">Simple Python interface to <a href="https://github.com/dan2097/opsin">OPSIN: Open Parser for Systematic IUPAC nomenclature</a></h3>

<p align="center">
  <img alt="GitHub Repo Stars" src="https://img.shields.io/github/stars/JacksonBurns/py2opsin?style=social">
  <img alt="Lifetime Downloads" src="https://static.pepy.tech/personalized-badge/py2opsin?period=total&units=none&left_color=grey&right_color=red&left_text=Lifetime%20Downloads">
  <img alt="PyPI - License" src="https://img.shields.io/github/license/JacksonBurns/py2opsin">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/py2opsin">
  <img alt="Run Tests" src="https://github.com/JacksonBurns/py2opsin/actions/workflows/run_tests.yml/badge.svg?branch=main&event=schedule">
</p>

<p align="center">  
  <img alt="py2opsin demo" src="https://github.com/JacksonBurns/py2opsin/blob/main/py2opsin_demo.gif">
</p> 

## Installation
`py2opsin` can be installed with `pip install py2opsin`. It has _zero_ Python dependencies (`OPSIN v2.7.0` is included in the PyPI package) and should work inside any environment running modern Python. Java 8+ is required to run OPSIN.

Try a demo of `py2opsin` live on your browser (no installation required!): [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JacksonBurns/py2opsin/HEAD?labpath=examples%2Fpy2opsin_example.ipynb)

## Usage
Command-line arguments available in `OPSIN` can be passed through to `py2opsin`:

```python
from py2opsin import py2opsin

>> smiles_string = py2opsin(
    chemical_name = "ethane",
    output_format = "SMILES",
)
smiles_str = "CC"

>> py2opsin(
    chemical_name: str or list of strings,
    output_format: str = "SMILES",
    allow_acid = False,
    allow_radicals = True,
    allow_bad_stereo = False,
    wildcard_radicals = False,
    jar_fpath = "/path/to/opsin.jar",
)
```

The result is returned as a Python string, or False if an unexpected error occurs when calling OPSIN. If a list of IUPAC names is provided, a list is returned. It is __highly__ reccomended to use `py2opsin` in this manner if you need to resolve any more than a couple names -- the performance cost of running `OPSIN` from Python one name at a time is significant (~5 seconds/molecule individually, milliseconds otherwise).

Arguments:
 - chemical_name (str): IUPAC name of chemical as a Python string, or a list of strings.
 - output_format (str, optional): One of "SMILES", "CML", "InChI", "StdInChI", or "StdInChIKey". Defaults to "SMILES".
 - allow_acid (bool, optional): Allow interpretation of acids. Defaults to False.
 - allow_radicals (bool, optional): Enable radical interpretation. Defaults to False.
 - allow_bad_stereo (bool, optional): Allow OPSIN to ignore uninterpreatable stereochem. Defaults to False.
 - wildcard_radicals (bool, optional): Output radicals as wildcards. Defaults to False.
 - jar_fpath (str, optional): Filepath to OPSIN jar file. Defaults to "opsin-cli.jar" which is distributed with py2opsin.


## Speedup 50x from `pubchempy`
`py2opsin` runs locally and is smaller in scope in what it provides, which makes it __dramatically__ faster at resolving identifiers. In the code block below, the call to `py2opsin` will execute ~58x faster than an equivalent call to `puchempy`:
```python
import time

from pubchempy import PubChemHTTPError, get_compounds
from py2opsin import py2opsin

compound_list = [
    "dienochlor",
    "kepone",
...
    "ditechnetium decacarbonyl",
]

for compound in compound_list:
    result = get_compounds(compound, "name")

smiles_strings = py2opsin(compound_list)
```


## Examples
 - Jeremy Monat's ([@bertiewooster](https://github.com/bertiewooster)) fantastic [blog post](https://bertiewooster.github.io/2023/03/10/Revisiting-a-Classic-Cheminformatics-Paper-The-Wiener-Index.html) using `py2opsin` to help explore the Wiener Index by enabling translation from IUPAC names into molecules directly from the original paper.

## Online Documentation
[Click here to read the documentation](https://JacksonBurns.github.io/py2opsin/)

## Contributing & Developer Notes
Pull Requests, Bug Reports, and all Contributions are welcome! Please use the appropriate issue or pull request template when making a contribution.

When submitting a PR, please mark your PR with the "PR Ready for Review" label when you are finished making changes so that the GitHub actions bots can work their magic!

### Developer Install

To contribute to the `py2opsin` source code, start by cloning the repository (i.e. `git clone git@github.com:JacksonBurns/py2opsin.git`) and then inside the repository run `pip install -e .[dev]`. This will set you up with all the required dependencies to run `astartes` and conform to our formatting standards (`black` and `isort`), which you can configure to run automatically in vscode [like this](https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00#:~:text=Go%20to%20settings%20in%20your,%E2%80%9D%20and%20select%20%E2%80%9Cblack%E2%80%9D.).

__Note for Windows Powershell or MacOS Catalina or newer__: On these systems the command line will complain about square brackets, so you will need to double quote the `molecules` command (i.e. `pip install -e ".

## License
`OPSIN` and `py2opsin` are both distributed under the MIT license.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
