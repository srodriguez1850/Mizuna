import os
import pprint
import shutil
from .version import __version__
from .git import Git
import warnings


# TODO: we should NOT be overwriting the samefile hook, but it'll work with GDrive for the meantime
# all files will be considered different
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
        Initialization method for Mizuna.

        Parameters
        ----------
        repo_remote_url: str
            Remote URL of the git repository
        repo_local_directory: str
            Local directory to maintain the git repository
        networked_drive: bool
            True if the local directory is a networked drive
        """

        self._cwd = os.getcwd()
        self.version = __version__

        print(f'Mizuna v{self.version}')
        print(f'Mizuna will setup a sync folder from your current working directory.')
        print(f'Current working directory: {self._cwd}')

        if networked_drive:
            warnings.warn(f'A bug in Python (see https://bugs.python.org/issue33935) prevents files in networked drives'
                          f'from copying properly.'
                          f'Mizuna will prevent a crucial routine in the copying method from running.'
                          f'This will allow the metadata of same files to be updated and overwritten.', RuntimeWarning)
            shutil._samefile = samefile_network_hook

        self._files_tracked = dict()
        self._files_tracked_count = 0
        self._mizuna_sync_folder = '.mizuna'

        if os.path.isdir(self._mizuna_sync_folder):
            print(f'Sync folder {self._mizuna_sync_folder} exists.')
        else:
            os.mkdir(self._mizuna_sync_folder)
            print(f'Sync folder {self._mizuna_sync_folder} does not exist -- creating.')

        print(f'Sync folder (relative): {self._mizuna_sync_folder}')
        print(f'Sync folder (absolute): {os.path.join(self._cwd, self._mizuna_sync_folder)}')

        self._repo_remote_url = repo_remote_url
        self._repo_local_directory = repo_local_directory

        print(f'Remote URL: {self._repo_remote_url}')
        print(f'Local directory: {self._repo_local_directory}')

        print('Connecting to git...')
        full_local_directory = os.path.join(self._mizuna_sync_folder, self._repo_local_directory)
        print(f'Sync local directory: {full_local_directory}')
        self._bridge = Git(repo_remote_url, full_local_directory, self._cwd)

        self._bridge.pull()

    def __str__(self):

        return_string = f'Repository Remote URL: {self._repo_remote_url}\n' \
                        f'Repository Local Directory: {self._repo_local_directory}'

        return return_string

    def track(self,
              file,
              remote_file: str = ''):

        # TODO: check if file exists before tracking? throw warning if files does not exist

        if isinstance(file, str):
            if isinstance(remote_file, str):
                self._add_single_track(file, remote_file)
            else:
                raise Exception('File remote location should be a string.')
        elif isinstance(file, dict):
            if remote_file != '':
                warnings.warn(f'Passing a dictionary of files, ignoring remote_file parameter.')
            self._add_multi_track(file)
        elif isinstance(file, list):
            if remote_file != '':
                warnings.warn(f'Passing a list of files, ignoring remote_file parameter.')
            for f in file:
                self._add_single_track(f, '')
        else:
            raise Exception('File location should be a string.')

        self._files_tracked_count = len(self._files_tracked)
        pprint.pprint(self._files_tracked)

    def _add_single_track(self,
                          file_path: str,
                          remote_path: str):

        if not os.path.exists(file_path):
            raise Exception(f'{file_path} does not exist')

        if file_path in self._files_tracked:
            warnings.warn(f'{file_path} is already being tracked, updating remote to: {remote_path}', RuntimeWarning)

        self._files_tracked[file_path] = remote_path

    def _add_multi_track(self,
                         files: dict):

        for k, v in files.items():
            if not isinstance(k, str):
                raise Exception(f'File location should be a string: {k}')
            if not isinstance(v, str):
                raise Exception(f'File remote location should be a string: {v}')

            try:
                self._add_single_track(k, v)
            except Exception as e:
                print(e)

    def untrack(self, file):
        self._files_tracked.pop(file)
        self._files_tracked_count = len(self._files_tracked)
        print(f'{file} untracked.')

    def untrack_all(self):
        self._files_tracked.clear()
        self._files_tracked_count = 0
        print(f'All files untracked.')

    def file_track_list(self):
        return self._files_tracked

    def sync(self):
        self._bridge.pull()

        if len(self._files_tracked) == 0:
            warnings.warn('Trying to call sync with no tracked files.', RuntimeWarning)
            return

        # copy files over sync folder
        # TODO: cleanup, remember the git add files should be relative to the local git repo
        for src, dst in self._files_tracked.items():
            if dst == '':
                dst = src
                dstn = os.path.join(self._bridge.repo_local_directory, src)
            else:
                dstn = os.path.join(self._bridge.repo_local_directory, dst)
            print(src, dstn)

            if not os.path.exists(os.path.dirname(dstn)):
                os.makedirs(os.path.dirname(dstn), exist_ok=True)
            shutil.copy2(src, dstn)

            res1 = self._bridge.add(dst)

        res2 = self._bridge.commit()
        res3 = self._bridge.push()

        return res1 or res2 or res3
