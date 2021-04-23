from typing import List, Optional, Dict, Tuple, Any
import subprocess
# import getpass


def call_subprocess(cmd_tokens: List[str],
                    cwd: str,
                    check: bool = True,
                    shell: bool = False,
                    env: Optional[Dict[str, str]] = None,
                    verbose: bool = False) -> Tuple[int, Any, Any]:
    """Execute a subprocess call and properly benchmark and log
    Args:
        cmd_tokens: List of command tokens, e.g., ['ls', '-la']
        cwd: Current working directory
        check: Raise exception if command fails
        shell: Run as shell command (not recommended)
        env: environment variables to pass to the subprocess
    Returns:
        Decoded stdout of called process after completing
    Raises:
        subprocess.CalledProcessError
    """
    try:
        r = subprocess.run(cmd_tokens, cwd=cwd, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           check=check, shell=shell, env=env)
        return r.returncode, r.stdout, r.stderr
    except subprocess.CalledProcessError as err:
        # raise ValueError(f"An error occurred in a subprocess call:\ncmd: {' '.join(cmd_tokens)}\n"
        #                  f"code: {err.returncode}\n"
        #                  f"output: {err.stdout} \nerror: {err.stderr}")
        if verbose:
            print(f"An error occurred in a subprocess call:\ncmd: {' '.join(cmd_tokens)}\n"
                  f"code: {err.returncode}\n"
                  f"output: {err.stdout} \nerror: {err.stderr}")
        return err.returncode, err.stdout, err.stderr


# def confirmation_prompt(prompt: str = 'Confirm ([y]/n)? ',
#                         yes_responses: List[str] = ['y', 'yes'],
#                         no_responses: List[str] = ['n', 'no']) -> bool:
#
#     user_response = input(prompt)
#
#     if len(user_response) == 0:
#         return True
#     elif user_response.lower() in yes_responses:
#         return True
#     elif user_response.lower() in no_responses:
#         return False
#     else:
#         print(f'Unrecognized confirmation: {user_response}')
#         return False


# def get_credentials() -> Tuple[str, str]:
#
#     email = getpass.getpass('Overleaf email: ')
#     password = getpass.getpass('Overleaf password: ')
#
#     return email, password
