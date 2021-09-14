import os
from typing import List, Any, Tuple
from .utils.utils import verbose_print, call_subprocess


class Git:

    def __init__(self,
                 repo_remote_url: str,
                 repo_local_directory: str,
                 cwd: str):
        """
        Git constructor.

        Parameters
        ----------
        repo_remote_url: str
            Remote URL of the git repository
        repo_local_directory: str
            Local directory to maintain the git repository
        cwd: str
            Current working directory
        """

        self.__repo_local_directory = repo_local_directory
        self.__repo_remote_url = repo_remote_url
        self.__cwd = cwd

        verbose_print(f'[mizuna] git: {self.__repo_local_directory} -- {self.__repo_remote_url}')
        verbose_print(f'[mizuna] git cwd: {self.__cwd}')

        if not os.path.isdir(self.__repo_local_directory):
            res_code, stdout, err = self.clone()
            if res_code != 0:
                raise Exception(f'An error occurred while cloning the repository: {err.decode()}')
        else:
            verbose_print(f'[mizuna] Found existing repo in sync folder: {self.__repo_local_directory}')

        print(f'[mizuna] Git connection established -- directory: {self.__repo_local_directory}')

    @property
    def local_directory(self):
        return self.__repo_local_directory

    @property
    def remote(self):
        return self.__repo_remote_url

    @staticmethod
    def __git(cmd_tokens: List[str],
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
        return call_subprocess(['git'] + cmd_tokens, cwd, check=True, shell=False, env=dict(env_vars))

    def clone(self) -> Tuple[int, Any, Any]:
        """
        Clone the Overleaf git repository.

        Returns
        -------
        Tuple[int, Any, Any]
            the output from the git command
        """

        verbose_print('[mizuna] Cloning git repository...')
        res_code, stdout, err = self.__git(['clone', self.__repo_remote_url, self.__repo_local_directory], self.__cwd)

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

        res_code, stdout, err = self.__git(['add', file], self.__repo_local_directory)

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

        res_code, stdout, err = self.__git(['commit', '-m', f'Update from Mizuna'], self.__repo_local_directory)

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

        res_code, stdout, err = self.__git(['pull'], self.__repo_local_directory)

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

        res_code, stdout, err = self.__git(['push'], self.__repo_local_directory)

        if res_code != 0:
            raise Exception(err)

        return res_code, stdout, err
