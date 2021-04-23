import unittest
from unittest.mock import patch
import shutil
import os

from mizuna.mizuna import Mizuna


test_repo_url = 'https://git.overleaf.com/invalidlink'
test_repo_dir = 'DummySync'
sync_dir_name = '.mizuna_sync'

test_dir = 'tests'
file_single1 = 'figures/fig1.pdf'
file_single2 = 'figures/fig2.pdf'


class Utilities:

    @staticmethod
    def delete_sync_directory():
        if os.path.exists(sync_dir_name):
            shutil.rmtree(sync_dir_name)


class Initialization(unittest.TestCase):

    def setUp(self) -> None:
        Utilities.delete_sync_directory()

    def tearDown(self) -> None:
        Utilities.delete_sync_directory()

    @patch('mizuna.gitoverleaf.call_subprocess')
    def test_version(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        from mizuna.version import __version__
        m = Mizuna(test_repo_url, test_repo_dir)
        self.assertEqual(m.version, __version__)

    @patch('mizuna.gitoverleaf.call_subprocess')
    def test_initialization(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        m = Mizuna(test_repo_url, test_repo_dir)
        self.assertTrue(m.initialized)

    @patch('mizuna.gitoverleaf.call_subprocess')
    def test_create_sync_directory(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        m = Mizuna(test_repo_url, test_repo_dir)
        self.assertTrue(os.path.exists(sync_dir_name))

    @patch('mizuna.gitoverleaf.call_subprocess')
    def test_networked_drive_warning(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        with self.assertWarns(RuntimeWarning):
            m = Mizuna(test_repo_url, test_repo_dir, True)


class Adding(unittest.TestCase):

    @patch('mizuna.gitoverleaf.call_subprocess')
    def setUp(self, mock_subprocess) -> None:
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir)
        self.m.untrack_all()
        self.assertEqual(self.m.files_tracked_count, 0)

    def test_track_one_single(self):
        self.m.track(file_single1, file_single1)
        self.assertEqual(self.m.files_tracked_count, 1)
        test_set = {file_single1: file_single1}
        self.assertDictEqual(self.m.track_list(), test_set)

    def test_track_two_singles(self):
        self.m.track(file_single1, file_single1)
        self.m.track(file_single2, file_single2)
        self.assertEqual(self.m.files_tracked_count, 2)
        test_set = {file_single1: file_single1,
                    file_single2: file_single2}
        self.assertDictEqual(self.m.track_list(), test_set)

    def test_track_duplicate(self):
        with self.assertWarns(RuntimeWarning):
            self.m.track(file_single1)
            self.m.track(file_single1)


class Removing(unittest.TestCase):

    test_set = {file_single1: file_single1,
                file_single2: file_single2}

    @patch('mizuna.gitoverleaf.call_subprocess')
    def setUp(self, mock_subprocess) -> None:
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir)
        self.m.untrack_all()
        self.assertEqual(self.m.files_tracked_count, 0)
        self.m.track(self.test_set)
        self.assertEqual(self.m.files_tracked_count, len(self.test_set))

    def test_remove_one(self):
        self.m.untrack(file_single1)
        self.assertEqual(self.m.files_tracked_count, len(self.test_set) - 1)
        test_set_removed = self.test_set
        test_set_removed.pop(file_single1)
        self.assertDictEqual(self.m.track_list(), test_set_removed)

    def test_remove_all(self):
        self.m.untrack_all()
        self.assertEqual(self.m.files_tracked_count, 0)
        self.assertDictEqual(self.m.track_list(), dict())


class Syncing(unittest.TestCase):

    @patch('mizuna.gitoverleaf.call_subprocess')
    def setUp(self, mock_subprocess) -> None:
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir)

    @patch('mizuna.gitoverleaf.call_subprocess')
    def test_sync(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m.track(os.path.join(test_dir, file_single1), file_single1)
        result = self.m.sync()
        self.assertEqual(result[0], 0)

    @patch('mizuna.gitoverleaf.call_subprocess')
    def test_sync_no_files(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        with self.assertRaises(Exception):
            self.m.sync()

    def tearDown(self) -> None:
        Utilities.delete_sync_directory()


if __name__ == '__main__':
    unittest.main()
