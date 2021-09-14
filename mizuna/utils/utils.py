from typing import List, Optional, Dict, Tuple, Any
import subprocess
import warnings

verbose = True


def call_subprocess(cmd_tokens: List[str],
                    cwd: str,
                    check: bool = True,
                    shell: bool = False,
                    env: Optional[Dict[str, str]] = None) -> Tuple[int, Any, Any]:
    """
    Executes a subprocess call.

    Parameters
    ----------
    cmd_tokens: list
        List of command tokens, e.g., ['ls', '-la']
    cwd: str
        Current working directory
    check: bool, optional
        Raise exception if command fails
    shell: bool, optional
        Run as shell command (not recommended)
    env: dict, optional
        Environment variables to pass to the subprocess

    Returns
    -------
    Tuple[int, Any, Any]
        Decoded stdout of called process after completing

    Raises
    ------
    subprocess.CalledProcessError
        If an error occurs in the subprocess
    """

    try:
        r = subprocess.run(cmd_tokens, cwd=cwd, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           check=check, shell=shell, env=env)
        return r.returncode, r.stdout, r.stderr
    except subprocess.CalledProcessError as err:
        warnings.warn(f"An error occurred in a subprocess call:\ncmd: {' '.join(cmd_tokens)}\n"
                      f"code: {err.returncode}\n"
                      f"output: {err.stdout} \nerror: {err.stderr}")
        return err.returncode, err.stdout, err.stderr


def verbose_print(t):
    if verbose:
        print(t)


def all_of_type(elements, type_check):
    if len(elements) == 0:
        raise Exception('List empty.')

    return all([isinstance(x, type_check) for x in elements])
