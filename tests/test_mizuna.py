import unittest
from unittest.mock import patch
import shutil
import os

from mizuna.mizuna import Mizuna


test_repo_url = 'https://git.overleaf.com/unittesturl'
test_repo_dir = 'UnitTestDir'
sync_dir_name = '.mizuna'

test_dir = 'tests'
file_single1 = 'figures/fig1.txt'
file_single2 = 'figures/fig2.txt'


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

    @patch('mizuna.git.call_subprocess')
    def test_version(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        from mizuna.version import __version__
        m = Mizuna(test_repo_url, test_repo_dir)
        self.assertEqual(m.version, __version__)

    @patch('mizuna.git.call_subprocess')
    def test_initialization(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        m = Mizuna(test_repo_url, test_repo_dir)

    @patch('mizuna.git.call_subprocess')
    def test_clone_fail(self, mock_subprocess):
        mock_subprocess.return_value = (128, 'fail', 'fail')
        with self.assertRaises(Exception):
            m = Mizuna(test_repo_url, test_repo_dir)

    @patch('mizuna.git.call_subprocess')
    def test_create_sync_directory(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        m = Mizuna(test_repo_url, test_repo_dir)
        self.assertTrue(os.path.exists(sync_dir_name))

    @patch('mizuna.git.call_subprocess')
    def test_networked_drive_warning(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        with self.assertWarns(RuntimeWarning):
            m = Mizuna(test_repo_url, test_repo_dir, True)

    @patch('mizuna.git.call_subprocess')
    def test_print(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        m = Mizuna(test_repo_url, test_repo_dir)
        print(m)


class Adding(unittest.TestCase):

    @patch('mizuna.git.call_subprocess')
    def setUp(self, mock_subprocess) -> None:
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir)
        self.m.untrack_all()
        self.assertEqual(self.m._files_tracked_count, 0)

    def test_track_single(self):
        self.m.track(os.path.join(test_dir, file_single1), file_single1)
        self.assertEqual(self.m._files_tracked_count, 1)
        test_set = {os.path.join(test_dir, file_single1): file_single1}
        self.assertDictEqual(self.m.file_track_list(), test_set)

    def test_track_dict(self):
        self.m.track(os.path.join(test_dir, file_single1), file_single1)
        self.m.track(os.path.join(test_dir, file_single2), file_single2)
        self.assertEqual(self.m._files_tracked_count, 2)

        test_set = {os.path.join(test_dir, file_single1): file_single1,
                    os.path.join(test_dir, file_single2): file_single2}
        self.assertDictEqual(self.m.file_track_list(), test_set)

    def test_track_duplicate(self):
        with self.assertWarns(RuntimeWarning):
            self.m.track(os.path.join(test_dir, file_single1))
            self.m.track(os.path.join(test_dir, file_single1))

    def test_bad_track_local_single(self):
        with self.assertRaises(Exception):
            self.m.track(1234)

        self.assertEqual(self.m._files_tracked_count, 0)
        self.assertDictEqual(self.m.file_track_list(), dict())

    def test_bad_track_remote_single(self):
        with self.assertRaises(Exception):
            self.m.track(os.path.join(test_dir, file_single1), 1234)

        self.assertEqual(self.m._files_tracked_count, 0)
        self.assertDictEqual(self.m.file_track_list(), dict())

    def test_bad_track_dict(self):
        test_set = {file_single1: 1234,
                    file_single2: file_single2}
        with self.assertRaises(Exception):
            self.m.track(test_set)

        test_set = {file_single1: file_single1,
                    1234: file_single2}
        with self.assertRaises(Exception):
            self.m.track(test_set)

        self.assertEqual(self.m._files_tracked_count, 0)
        self.assertDictEqual(self.m.file_track_list(), dict())


class Removing(unittest.TestCase):

    test_set = {os.path.join(test_dir, file_single1): file_single1,
                os.path.join(test_dir, file_single1): file_single2}

    @patch('mizuna.git.call_subprocess')
    def setUp(self, mock_subprocess) -> None:
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir)
        self.m.untrack_all()
        self.assertEqual(self.m._files_tracked_count, 0)
        self.m.track(self.test_set)
        self.assertEqual(self.m._files_tracked_count, len(self.test_set))

    def test_remove_one(self):
        self.m.untrack(os.path.join(test_dir, file_single1))
        self.assertEqual(self.m._files_tracked_count, len(self.test_set) - 1)
        test_set_removed = self.test_set
        test_set_removed.pop(os.path.join(test_dir, file_single1))
        self.assertDictEqual(self.m.file_track_list(), test_set_removed)

    def test_remove_all(self):
        self.m.untrack_all()
        self.assertEqual(self.m._files_tracked_count, 0)
        self.assertDictEqual(self.m.file_track_list(), dict())


class Syncing(unittest.TestCase):

    @patch('mizuna.git.call_subprocess')
    def setUp(self, mock_subprocess) -> None:
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir)

    @patch('mizuna.git.call_subprocess')
    def test_sync(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m.track(os.path.join(test_dir, file_single1), file_single1)
        result, stdout, err = self.m.sync()
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(os.path.join(sync_dir_name, test_repo_dir, file_single1)))

    @patch('mizuna.git.call_subprocess')
    def test_sync_different_names(self, mock_subprocess):
        test_set = {os.path.join(test_dir, file_single1): file_single1,
                    os.path.join(test_dir, file_single2): ''}

        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m.track(test_set)
        result, stdout, err = self.m.sync()
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(os.path.join(sync_dir_name, test_repo_dir, file_single1)))
        self.assertTrue(os.path.exists(os.path.join(sync_dir_name, test_repo_dir, 'tests', file_single2)))

    @patch('mizuna.git.call_subprocess')
    def test_sync_no_files(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        with self.assertWarns(RuntimeWarning):
            self.m.sync()

    def tearDown(self) -> None:
        Utilities.delete_sync_directory()
