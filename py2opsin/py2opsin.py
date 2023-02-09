from difflib import get_close_matches
import os
import subprocess
import sys
import warnings


def py2opsin(
    chemical_name: str,
    output_format: str = "SMILES",
    allow_acid: bool = False,
    allow_radicals: bool = False,
    allow_bad_stereo: bool = False,
    wildcard_radicals: bool = False,
    jar_fpath: str = "opsin-cli-2.7.0-jar-with-dependencies.jar",
) -> str:
    """Simple passthrough to opsin, returning results as Python strings.

    Args:
        chemical_name (str): IUPAC name of chemical.
        output_format (str, optional): One of "SMILES", "CML", "InChI", "StdInChI", or "StdInChIKey". Defaults to "SMILES".
        allow_acid (bool, optional): Allow interpretation of acids. Defaults to False.
        allow_radicals (bool, optional): Enable radical interpretation. Defaults to False.
        allow_bad_stereo (bool, optional): Allow OPSIN to ignore uninterpreatable stereochem. Defaults to False.
        wildcard_radicals (bool, optional): Output radicals as wildcards. Defaults to False.
        jar_fpath (str, optional): Filepath to OPSIN jar file. Defaults to "opsin-cli-2.7.0-jar-with-dependencies.jar" which is distributed with py2opsin.

    Returns:
        str: Species in requested format, or False if not found or an error occoured.
    """
    # default arguments to start
    arg_list = ["java", "-jar", jar_fpath]

    # format the output argument
    if output_format == "SMILES":
        arg_list.append("-osmi")
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
            ["SMILES", "CML", "InChI", "StdInChI", "StdInChIKey"],
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
        file.write(chemical_name)

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
        stderr=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
    )

    # parse and return the result
    try:
        result.check_returncode()
        return result.stdout.decode(encoding=sys.stdout.encoding).strip("\n")
    except Exception as e:
        warnings.warn("Unexpected error occured! " + e)
        return False
    finally:
        os.remove(temp_f)
