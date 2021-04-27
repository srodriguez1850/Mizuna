import os
from typing import List, Optional, Dict, Any, Tuple
from .utils import call_subprocess


def _git(cmd_tokens: List[str],
         cwd: str) -> Tuple[int, Any, Any]:
    """
    Execute a subprocess call and properly benchmark and log
    Args:
        cmd_tokens: List of command tokens, e.g., ['ls', '-la']
        cwd: Current working directory
    Returns:
        Decoded stdout of called process after completing
    Raises:
        subprocess.CalledProcessError
    """

    env_vars = os.environ
    return call_subprocess(['git'] + cmd_tokens, cwd, check=True, shell=False, env=dict(env_vars), verbose=True)


class GitOverleaf:

    def __init__(self,
                 repo_remote_url: str,
                 repo_local_directory: str,
                 cwd) -> None:
        """Load configuration of bridge or initialize."""

        self.repo_local_directory = repo_local_directory
        self.repo_remote_url = repo_remote_url
        self.cwd = cwd
        # self.config_file = None
        # self.cred_file = None

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

        print('Cloning Overleaf git repo to sync.')
        res_code, stdout, err = _git(['clone', self.repo_remote_url, self.repo_local_directory], self.cwd)

        return res_code, stdout, err

    def add(self, file) -> Tuple[int, Any, Any]:
        """
            Method to add changes to the Overleaf git repository

            Returns:
                the output from git commands
        """
        res_code, stdout, err = _git(['add', file], self.repo_local_directory)

        print(res_code)

        return res_code, stdout, err

    def commit(self) -> Tuple[int, Any, Any]:
        """
        Method to commit changes to the Overleaf git repository

        Returns:
            the output from git commands
        """
        res_code, stdout, err = _git(['commit', '-m', f'Updating linked files from Mizuna.'], self.repo_local_directory)

        print(res_code)

        return res_code, stdout, err

    def pull(self) -> Tuple[int, Any, Any]:
        """Method to pull changes to the Overleaf git repository
        Returns:
            the output from the git command
        """
        res_code, stdout, err = _git(['pull'], self.repo_local_directory)

        # TODO: not a valid .git repo, probably corrupted
        if res_code != 0:
            raise Exception('Not a valid git repo.')

        return res_code, stdout, err

    def push(self) -> Tuple[int, Any, Any]:
        """Method to pull changes to the Overleaf git repository
        Returns:
            the output from the git command
        """
        res_code, stdout, err = _git(['push'], self.repo_local_directory)

        # TODO: not a valid .git repo, probably corrupted
        if res_code != 0:
            raise Exception('Not a valid git repo.')

        return res_code, stdout, err
