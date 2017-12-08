import subprocess


def which(exe):
    """
    Finds the path for an executable file, if it exists
    :param exe: executable to look for
    :return: executable path
    """
    return subprocess.check_output(['which', exe]).rstrip()