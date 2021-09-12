import os
from getpass import getpass
from typing import List, Any, Tuple
from .utils import call_subprocess


def _git(cmd_tokens: List[str],
         cwd: str) -> Tuple[int, Any, Any]:
    """
    Execute a git subprocess call.

    Parameters
    ----------
    cmd_tokens: list
        List of command tokens, e.g., ['ls', '-la']
    cwd: str
        Current working directory

    Returns
    -------
    Tuple
        Decoded stdout of called process after completing

    Raises
    ------
    subprocess.CalledProcessError
        If there is an error in the subprocess
    """

    env_vars = os.environ
    return call_subprocess(['git'] + cmd_tokens, cwd, check=True, shell=False, env=dict(env_vars), verbose=True)


class Git:

    def __init__(self,
                 repo_remote_url: str,
                 repo_local_directory: str,
                 cwd: str):
        """
        Load and configure bridge to a git repository.

        Parameters
        ----------
        repo_remote_url: str
            Remote URL of the git repository
        repo_local_directory: str
            Local directory to maintain the git repository
        cwd: str
            Current working directory
        """

        self.repo_local_directory = repo_local_directory
        self.repo_remote_url = repo_remote_url
        self.cwd = cwd

        print(f'Git bridge: {self.repo_local_directory} -- {self.repo_remote_url}')
        print(f'Git bridge cwd: {self.cwd}')

        if not os.path.isdir(self.repo_local_directory):
            res_code, stdout, err = self.clone()
            if res_code != 0:
                raise Exception(f'An error occurred while cloning the repository: {err.decode()}')
        else:
            print(f'Found existing repo in sync folder: {self.repo_local_directory}')

        print(f'Bridge initialized, bridge directory: {self.repo_local_directory}')

    def clone(self) -> Tuple[int, Any, Any]:
        """
        Clone the Overleaf git repository.

        Returns
        -------
        Tuple[int, Any, Any]
            the output from the git command
        """

        print('Cloning Overleaf git repo to sync.')
        res_code, stdout, err = _git(['clone', self.repo_remote_url, self.repo_local_directory], self.cwd)

        if res_code != 0:
            raise Exception(err)

        return res_code, stdout, err

    def add(self,
            file: str) -> Tuple[int, Any, Any]:
        """
        Add changes to the git repository.

        Parameters
        ----------
        file: str
            File to add to the staging

        Returns
        -------
        Tuple[int, Any, Any]
            the output from the git command
        """

        res_code, stdout, err = _git(['add', file], self.repo_local_directory)

        if res_code != 0:
            raise Exception(err)

        return res_code, stdout, err

    def commit(self) -> Tuple[int, Any, Any]:
        """
        Commit changes to the git repository.

        Returns
        -------
        Tuple[int, Any, Any]
            the output from the git command
        """

        res_code, stdout, err = _git(['commit', '-m', f'Update from Mizuna'], self.repo_local_directory)

        if res_code != 0:
            raise Exception(err)

        return res_code, stdout, err

    def pull(self) -> Tuple[int, Any, Any]:
        """
        Pull changes from the git repository.

        Returns
        -------
        Tuple[int, Any, Any]
            the output from the git command
        """

        res_code, stdout, err = _git(['pull'], self.repo_local_directory)

        if res_code != 0:
            raise Exception(err)

        return res_code, stdout, err

    def push(self) -> Tuple[int, Any, Any]:
        """
        Push changes to the git repository.

        Returns
        -------
        Tuple[int, Any, Any]
            the output from the git command
        """

        res_code, stdout, err = _git(['push'], self.repo_local_directory)

        if res_code != 0:
            raise Exception(err)

        return res_code, stdout, err
