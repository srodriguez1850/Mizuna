import os
import shutil
from .version import __version__
from .git import Git
import mizuna.utils
from .utils.utils import verbose_print, all_of_type
import warnings


# NOTE: this hook into shutil._samefile will force all files to be considered different, thus overwriting
# networked drives considers two files in the same directory equal, this hook is needed so files can be copied
def samefile_network_hook(*args, **kwargs):
    return False


samefile_original_func = shutil._samefile


class Mizuna:

    def __init__(self,
                 repo_remote_url: str,
                 repo_local_directory: str,
                 networked_drive: bool = False,
                 verbose: bool = False):

        """
        Mizuna constructor.

        Parameters
        ----------
        repo_remote_url: str
            Remote URL of the git repository
        repo_local_directory: str
            Local directory to maintain the git repository
        networked_drive: bool
            True if the local directory is a networked drive
        verbose: bool
            Print verbose output
        """

        mizuna.utils.verbose = verbose
        self.version = __version__

        self.__files_tracked = dict()

        self._repo_remote_url = repo_remote_url
        self._mizuna_sync_dir = '.mizuna'
        self._repo_local_directory = repo_local_directory
        full_local_directory = os.path.join(self._mizuna_sync_dir, self._repo_local_directory)

        verbose_print(f'[mizuna] v{self.version}')
        verbose_print(f'[mizuna] cwd: {os.getcwd()}')

        if networked_drive:
            warnings.warn(f'A bug in Python (see https://bugs.python.org/issue33935) prevents files in networked drives'
                          f'from copying properly.'
                          f'Mizuna will prevent a crucial routine in the copying method from running.'
                          f'This will allow the metadata of same files to be updated and overwritten.', RuntimeWarning)
            shutil._samefile = samefile_network_hook

        if os.path.isdir(self._mizuna_sync_dir):
            verbose_print(f'[mizuna] Sync folder {self._mizuna_sync_dir}/ exists.')
            verbose_print(f'[mizuna] Consider adding {self._mizuna_sync_dir}/ to your .gitignore if using VC.')
        else:
            verbose_print(f'[mizuna] Sync folder {self._mizuna_sync_dir}/ does not exist -- creating.')
            os.mkdir(self._mizuna_sync_dir)

        verbose_print(f'[mizuna] Sync folder (absolute): {os.path.join(os.getcwd(), self._mizuna_sync_dir)}')

        verbose_print(f'[mizuna] Remote URL: {self._repo_remote_url}')
        verbose_print(f'[mizuna] Local directory: {os.path.join(self._mizuna_sync_dir, self._repo_local_directory)}')

        print('[mizuna] Connecting to git...')
        self.__bridge = Git(repo_remote_url, full_local_directory, os.getcwd())

        self.__bridge.pull()

    def __str__(self):

        return_string = f'Repository Remote URL: {self._repo_remote_url}\n' \
                        f'Repository Local Directory: {self._repo_local_directory}'

        return return_string

    @property
    def track_list(self):
        return self.__files_tracked

    @property
    def track_count(self):
        return len(self.__files_tracked)

    @property
    def git(self):
        return self.__bridge

    def track(self,
              *args):

        if len(args) == 0:
            raise Exception('Not enough arguments.')
        if len(args) > 2:
            raise Exception('Too many arguments.')

        files = args[0]
        rename = args[1] if len(args) == 2 else None

        # single file
        if isinstance(files, str) and rename is None:
            self.__track_single(files)

        # single file with rename
        elif isinstance(files, str) and rename is not None:
            self.__track_single(files, rename)

        # list of files or tuples
        elif isinstance(files, list) and rename is None:
            if all_of_type(files, str):
                for f in files:
                    self.__track_single(f)
            elif all_of_type(files, tuple):
                for f in files:
                    self.__track_single(f[0], f[1])
            else:
                raise Exception('Invalid type passed in list.')

        # dictionary
        elif isinstance(files, dict) and rename is None:
            self.__track_multiple_dict(files)

        # invalid type
        else:
            raise Exception('Invalid arguments passed.')

    def __track_single(self,
                       file: str,
                       remote: str = ''):

        if not isinstance(remote, str):
            raise Exception('Remote is not a string.') # TODO: better error message

        if remote == '':
            self.__files_tracked.update({file: file})
        else:
            self.__files_tracked.update({file: remote})

    def __track_multiple_dict(self,
                              files: dict):

        for f, r in files.items():
            self.__track_single(f, r)

    def untrack(self, file):

        self.__files_tracked.pop(file)
        print(f'[mizuna] {file} untracked.')

    def untrack_all(self):

        self.__files_tracked.clear()
        print(f'[mizuna] All files untracked.')

    def sync(self):

        self.__bridge.pull()

        if self.track_count == 0:
            warnings.warn('Mizuna has no files to sync.', RuntimeWarning)
            return

        res1 = None
        for src, rename in self.__files_tracked.items():
            copy_path = os.path.join(self.__bridge.local_directory, rename)
            verbose_print(f'Source: {src} -> Rename: {rename} -- Remote path: {copy_path}')

            if not os.path.exists(os.path.dirname(copy_path)):
                os.makedirs(os.path.dirname(copy_path), exist_ok=True)
            shutil.copy2(src, copy_path)

            res1 = self.__bridge.add(rename)

        res2 = self.__bridge.commit()
        res3 = self.__bridge.push()

        return res1 or res2 or res3
