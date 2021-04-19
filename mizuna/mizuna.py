import os
import shutil
from mizuna.gitoverleaf import GitOverleaf
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
                 networked_drive: bool = False):

        self._cwd = os.getcwd()

        print(f'Thanks for using Mizuna!')
        print(f'Mizuna will setup a sync folder from your current working directory.')
        print(f'Current working directory: {self._cwd}')

        if networked_drive:
            warnings.warn(f'A bug in Python (see https://bugs.python.org/issue33935) prevents files in networked drives from copying properly.'
                          f'Mizuna will prevent a crucial routine in the copying method from running.'
                          f'This will allow the metadata of same files to be updated and overwritten.', RuntimeWarning)
            shutil._samefile = samefile_network_hook

        self._files_tracked = set()
        self.files_tracked_count = len(self._files_tracked)
        self._mizuna_sync_folder = '.mizuna_sync'

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

        print(f'Opening bridge...')
        full_local_directory = os.path.join(self._mizuna_sync_folder, self._repo_local_directory)
        print(f'Sync local directory: {full_local_directory}')
        self._bridge = GitOverleaf(repo_remote_url, full_local_directory, self._cwd)

        self._initialized = self._bridge.initialized

        if not self._bridge.initialized:
            print(f'Git bridge failed to initialize, sync command will not work.')
        else:
            self._bridge.pull()

    def __str__(self):
        print(f'Initialized: {self._initialized}')
        print(f'Repository Remote URL: {self._repo_remote_url}')
        print(f'Repository Local Directory: {self._repo_local_directory}')

    def track(self,
              *files):

        # TODO: check if file exists before tracking? throw warning if files does not exist

        for file in files:

            if isinstance(file, str):
                self._add_single_track(file)
            elif isinstance(file, list):
                self._add_multi_track(file)

        self.files_tracked_count = len(self._files_tracked)
        print(self._files_tracked)

    def _add_single_track(self, file_path):
        if file_path in self._files_tracked:
            print(f'{file_path} is already being tracked.')
            return
        self._files_tracked.add(file_path)

    def _add_multi_track(self, file_paths):
        for file in file_paths:
            self._add_single_track(file)

    def untrack(self, file_path):
        self._files_tracked.remove(file_path)
        self.files_tracked_count = len(self._files_tracked)
        print(f'{file_path} untracked.')

    def untrack_all(self):
        self._files_tracked.clear()
        self.files_tracked_count = 0
        print(f'All files untracked.')

    def track_list(self):
        return self._files_tracked

    def sync(self):

        if not self._initialized:
            print(f'Trying to sync without a valid Git bridge, files will not be synced with Overleaf.')
            return

        self._bridge.pull()

        if len(self._files_tracked) == 0:
            raise Exception('Trying to call sync with no tracked files.')

        # copy files over sync folder
        for file in self._files_tracked:
            src = file
            dest = os.path.join(self._bridge.repo_local_directory, file)
            print(src, dest)
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(src, dest)



        self._bridge.add()
        self._bridge.commit()
        self._bridge.push()

        #TODO: replacing existing files in remote, what to do?
