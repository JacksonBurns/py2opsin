import os
import subprocess
import sys
import warnings
from difflib import get_close_matches
from typing import Union
from subprocess import CalledProcessError

try:
    from importlib.resources import files

    pkg_fopen = lambda fname: files("py2opsin") / fname
except ImportError:
    from pkg_resources import resource_filename

    pkg_fopen = lambda fname: resource_filename(__name__, fname)

# check if java is installed
try:
    result = subprocess.run(
        ["java", "-version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
except Exception as e:
    warnings.warn(
        "Java may not be installed/accessible (java -version raised exception). "
        "Java 8 or newer is required to use py2opsin. Original Error:\n" + repr(e),
        category=RuntimeWarning,
    )


def py2opsin(
    chemical_name: Union[str, list],
    output_format: str = "SMILES",
    allow_acid: bool = False,
    allow_radicals: bool = False,
    allow_bad_stereo: bool = False,
    wildcard_radicals: bool = False,
    jar_fpath: str = "default",
) -> str:
    """Simple passthrough to opsin, returning results as Python strings.

    Args:
        chemical_name (str, list): IUPAC name of chemical as string, or list of strings.
        output_format (str, optional): One of "SMILES", "ExtendedSMILES", "CML", "InChI", "StdInChI", or "StdInChIKey".
                                        Defaults to "SMILES".
        allow_acid (bool, optional): Allow interpretation of acids. Defaults to False.
        allow_radicals (bool, optional): Enable radical interpretation. Defaults to False.
        allow_bad_stereo (bool, optional): Allow OPSIN to ignore uninterpreatable stereochem. Defaults to False.
        wildcard_radicals (bool, optional): Output radicals as wildcards. Defaults to False.
        jar_fpath (str, optional): Filepath to OPSIN jar file. Defaults to "default", which causes py2opsin to use its included jar.

    Returns:
        str: Species in requested format, or False if not found or an error ocurred. List of strings if input is list.
    """
    # path to OPSIN jar
    if jar_fpath == "default":
        jar_fpath = pkg_fopen("opsin-cli-2.7.0-jar-with-dependencies.jar")

    # default arguments to start
    arg_list = ["java", "-jar", jar_fpath]

    # format the output argument
    if output_format == "SMILES":
        arg_list.append("-osmi")
    elif output_format == "ExtendedSMILES":
        arg_list.append("-oextendedsmiles")
    elif output_format == "CML":
        arg_list.append("-ocml")
    elif output_format == "InChI":
        arg_list.append("-oinchi")
    elif output_format == "StdInChI":
        arg_list.append("-ostdinchi")
    elif output_format == "StdInChIKey":
        arg_list.append("-ostdinchikey")
    else:
        possiblity = get_close_matches(
            output_format,
            [
                "SMILES",
                "CML",
                "InChI",
                "StdInChI",
                "StdInChIKey",
                "ExtendedSMILES",
            ],
            n=1,
        )
        addendum = (
            " Did you mean '{:s}'?".format(possiblity[0])
            if possiblity
            else " Try help(py2opsin)."
        )
        raise RuntimeError(
            "Output format {:s} is invalid.".format(output_format) + addendum
        )

    # write the input to a text file
    temp_f = "py2opsin_temp_input.txt"
    with open(temp_f, "w") as file:
        if type(chemical_name) is str:
            file.write(chemical_name)
        else:
            file.writelines("\n".join(chemical_name) + "\n")

    # add the temporary file to the args
    arg_list.append(temp_f)

    # grab the optional boolean flags
    if allow_acid:
        arg_list.append("-a")
    if allow_radicals:
        arg_list.append("-r")
    if allow_bad_stereo:
        arg_list.append("-s")
    if wildcard_radicals:
        arg_list.append("-w")

    # do the call
    result = subprocess.run(
        arg_list,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    # warn user if any of the inputs could not be parsed
    if result.stderr:
        err_str = result.stderr.decode(encoding=sys.stderr.encoding)
        warnings.warn(
            "OPSIN raised the following error(s) while parsing:"
            "\n > " + err_str.replace("\n", "\n > ", err_str.count("\n") - 1),
            RuntimeWarning,
        )

    # parse and return the result
    try:
        result.check_returncode()
        if type(chemical_name) is str:
            return (
                result.stdout.decode(encoding=sys.stdout.encoding)
                .replace("\n", "")
                .replace("\r", "")
            )
        else:
            return (
                result.stdout.decode(encoding=sys.stdout.encoding)
                .replace("\r", "")
                .split("\n")[0:-1]  # ignore newline at file end
            )

    except Exception as e:
        warnings.warn("Unexpected error ocurred! " + e)
        return False
    finally:
        os.remove(temp_f)
