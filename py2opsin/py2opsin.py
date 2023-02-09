import subprocess


def py2opsin(jar_fpath: str = "opsin-cli-2.7.0-jar-with-dependencies.jar"):
    result = subprocess.run(
        [
            "java",
            "-jar",
            jar_fpath,
            "-h",
        ],
        stderr=subprocess.DEVNULL,
    )
    result.check_returncode()
    print(result)
