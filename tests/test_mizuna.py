import unittest
from unittest.mock import patch
import shutil
import os

from mizuna.mizuna import Mizuna


test_repo_url = 'https://git.overleaf.com/unittesturl'
test_repo_dir = 'UnitTestDir'
sync_dir_name = '.mizuna'

test_dir = 'tests'
file1 = 'figures/fig1.txt'
file2 = 'figures/fig2.txt'
file3 = 'figures/fig3.txt'


class Utilities:

    @staticmethod
    def delete_sync_directory():
        if os.path.exists(sync_dir_name):
            shutil.rmtree(sync_dir_name)


class Initialization(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
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
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir, verbose=True)
        self.m.untrack_all()
        self.assertEqual(self.m.track_count, 0)

    def test_track_bad_empty(self):
        with self.assertRaises(Exception):
            self.m.track()

    def test_track_bad_empty_list(self):
        with self.assertRaises(Exception):
            self.m.track([])

    def test_track_single(self):
        self.m.track(file1)
        self.assertEqual(self.m.track_count, 1)
        test_set = {file1: file1}
        self.assertDictEqual(self.m.track_list, test_set)

    def test_track_single_rename(self):
        self.m.track(file1, 'renamed.txt')
        self.assertEqual(self.m.track_count, 1)
        test_set = {file1: 'renamed.txt'}
        self.assertDictEqual(self.m.track_list, test_set)

    def test_track_list_files(self):
        self.m.track([file1, file2, file3])
        self.assertEqual(self.m.track_count, 3)
        test_set = {file1: file1,
                    file2: file2,
                    file3: file3}
        self.assertDictEqual(self.m.track_list, test_set)

    def test_track_list_tuples(self):
        self.m.track([(file1, 'renamed1.txt'), (file2, 'renamed2.txt'), (file3, 'renamed3.txt')])
        self.assertEqual(self.m.track_count, 3)
        test_set = {file1: 'renamed1.txt',
                    file2: 'renamed2.txt',
                    file3: 'renamed3.txt'}
        self.assertDictEqual(self.m.track_list, test_set)

    def test_track_list(self):
        self.m.track([file1, file2, file3])
        self.assertEqual(self.m.track_count, 3)
        test_set = {file1: file1,
                    file2: file2,
                    file3: file3}
        self.assertDictEqual(self.m.track_list, test_set)

    def test_track_dict(self):
        test_set = {file1: 'renamed1.txt',
                    file2: 'renamed2.txt',
                    file3: 'renamed3.txt'}
        self.m.track(test_set)
        self.assertEqual(self.m.track_count, 3)
        self.assertDictEqual(self.m.track_list, test_set)

    def test_track_bad_file_type(self):
        with self.assertRaises(Exception):
            self.m.track(1234)

    def test_track_bad_remote_type(self):
        with self.assertRaises(Exception):
            self.m.track(file1, 1234)

    def test_track_bad_list_type(self):
        with self.assertRaises(Exception):
            self.m.track([1234, 1234])

    def test_track_too_many_argument_types(self):
        with self.assertRaises(Exception):
            self.m.track((file1, file1), 1234, 'renamed.txt')


class Removing(unittest.TestCase):

    test_set = {file1: file1,
                file2: file2}

    @patch('mizuna.git.call_subprocess')
    def setUp(self, mock_subprocess) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir)
        self.m.untrack_all()
        self.assertEqual(self.m.track_count, 0)
        self.m.track(self.test_set)
        self.assertEqual(self.m.track_count, len(self.test_set))

    def test_remove_one(self):
        self.m.untrack(file1)
        self.assertEqual(self.m.track_count, len(self.test_set) - 1)
        test_set_removed = self.test_set
        test_set_removed.pop(file1)
        self.assertDictEqual(self.m.track_list, test_set_removed)

    def test_remove_all(self):
        self.m.untrack_all()
        self.assertEqual(self.m.track_count, 0)
        self.assertDictEqual(self.m.track_list, dict())

    def test_remove_bad_key(self):
        with self.assertRaises(Exception):
            self.m.untrack('badkey.txt')


class Syncing(unittest.TestCase):

    @patch('mizuna.git.call_subprocess')
    def setUp(self, mock_subprocess) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m = Mizuna(test_repo_url, test_repo_dir, verbose=True)

    @patch('mizuna.git.call_subprocess')
    def test_sync(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        self.m.track(file1)
        result, stdout, err = self.m.sync()
        self.assertEqual(result, 0)
        path = os.path.join(sync_dir_name, test_repo_dir, file1)
        self.assertTrue(os.path.exists(path))

    @patch('mizuna.git.call_subprocess')
    def test_sync_no_files(self, mock_subprocess):
        mock_subprocess.return_value = (0, 'mock', 'mock')
        with self.assertWarns(RuntimeWarning):
            self.m.sync()

    @patch('mizuna.git.call_subprocess')
    def test_bad_git_response(self, mock_subprocess):
        mock_subprocess.return_value = (1, 'mock', 'mock')
        self.m.track(file1)
        with self.assertRaises(Exception):
            self.m.git.commit()
        with self.assertRaises(Exception):
            self.m.git.add()
        with self.assertRaises(Exception):
            self.m.git.push()
        with self.assertRaises(Exception):
            self.m.git.pull()

    def tearDown(self) -> None:
        Utilities.delete_sync_directory()
