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

        # TODO: allow multiple folders based on config files
        # env_vars = os.environ
        # if 'CI' in env_vars and env_vars['CI']:
        #     print(f'CI detected, skipping bridge initialization.')
        #     self.initialized = False
        #     return
        if not os.path.isdir(self.repo_local_directory):
            res_code, stdout, err = self.clone()
            if res_code == 128:
                print(f'An error occurred while cloning the repository: {err.decode()}')
                self.initialized = False
                return
        else:
            print(f'Found existing repo in sync folder: {self.repo_local_directory}')

        print(f'Bridge initialized, bridge directory: {self.repo_local_directory}')
        self.initialized = True

    def clone(self) -> Tuple[int, Any, Any]:
        if os.path.isdir(self.repo_local_directory):
            raise Exception('Repository already cloned.')

        print('Cloning Overleaf git repo to sync.')
        output = _git(['clone', self.repo_remote_url, self.repo_local_directory], self.cwd)

        return output

    def add(self) -> Tuple[int, Any, Any]:
        """
            Method to add changes to the Overleaf git repository

            Returns:
                the output from git commands
        """
        # TODO: add files depending on tracked files by Mizuna
        output = _git(['add', '-A'], self.repo_local_directory)

        print(output)

        return output

    def commit(self) -> Tuple[int, Any, Any]:
        """
        Method to commit changes to the Overleaf git repository

        Returns:
            the output from git commands
        """
        output = _git(['commit', '-m', f'Updating linked files from Viz2Overleaf.'], self.repo_local_directory)

        print(output)

        return output

    def pull(self) -> Tuple[int, Any, Any]:
        """Method to pull changes to the Overleaf git repository
        Returns:
            the output from the git command
        """
        output = _git(['pull'], self.repo_local_directory)

        # TODO: not a valid .git repo, probably corrupted
        if output == 128:
            print('Not a valid git repo.')

        return output

    def push(self) -> Tuple[int, Any, Any]:
        """Method to pull changes to the Overleaf git repository
        Returns:
            the output from the git command
        """
        output = _git(['push'], self.repo_local_directory)

        # TODO: not a valid .git repo, probably corrupted

        return output
