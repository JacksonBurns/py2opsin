<h1 align="center">py2opsin</h1> 
<h3 align="center">Simple Python interface to OPSIN: Open Parser for Systematic IUPAC nomenclature</h3>

<p align="center">  
  <img alt="py2opsinlogo" src="https://github.com/JacksonBurns/py2opsin/blob/main/py2opsin_logo.png">
</p> 
<p align="center">
  <img alt="GitHub Repo Stars" src="https://img.shields.io/github/stars/JacksonBurns/py2opsin?style=social">
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/py2opsin">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/py2opsin">
  <img alt="PyPI - License" src="https://img.shields.io/github/license/JacksonBurns/py2opsin">
</p>

## Online Documentation
[Click here to read the documentation](https://JacksonBurns.github.io/py2opsin/)

## Installation
`py2opsin` can be installed with `pip install py2opsin`. It has _zero_ dependencies and should work inside any environment running modern Python.

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

The result is returned as a Python string, or False if an unexpected error occurs when calling OPSIN. If a list of IUPAC names is provided, a list if returned.

Arguments:
    chemical_name (str): IUPAC name of chemical as a Python string, or a list of strings.
    output_format (str, optional): One of "SMILES", "CML", "InChI", "StdInChI", or "StdInChIKey". Defaults to "SMILES".
    allow_acid (bool, optional): Allow interpretation of acids. Defaults to False.
    allow_radicals (bool, optional): Enable radical interpretation. Defaults to False.
    allow_bad_stereo (bool, optional): Allow OPSIN to ignore uninterpreatable stereochem. Defaults to False.
    wildcard_radicals (bool, optional): Output radicals as wildcards. Defaults to False.
    jar_fpath (str, optional): Filepath to OPSIN jar file. Defaults to "opsin-cli.jar" which is distributed with py2opsin.

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