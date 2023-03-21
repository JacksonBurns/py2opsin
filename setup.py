import codecs
import os.path
import pathlib

from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# The directory containing this file
cwd = pathlib.Path(__file__).parent

# The text of the README file
README = (cwd / "README.md").read_text()

setup(
    name="py2opsin",
    version=get_version("py2opsin/__init__.py"),
    description="Simple Python interface to OPSIN: Open Parser for Systematic IUPAC nomenclature",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JacksonBurns/py2opsin",
    author="Jackson Burns, Jonathan Zheng",
    license="MIT",
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=[],
    extras_require={"dev": ["pubchempy", "black", "pytest", "isort"]},
    packages=find_packages(
        exclude=["test*", "docs*", "examples*"], include=["py2opsin*"]
    ),
    include_package_data=True,
)
