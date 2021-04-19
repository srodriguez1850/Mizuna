import unittest
from mizuna import Mizuna

test_repo_url = 'https://git.overleaf.com/6078b25623c7c09fd1d3f4a2'
test_repo_dir = 'Viz2OverleafDummy'

file_single1 = 'file1'
file_list = ['file2', 'file3']
file_single2 = 'file4'


# TODO: initialize with dummy connections
class Initialization(unittest.TestCase):

    def test_version(self):
        from mizuna.version import __version__
        m = Mizuna(test_repo_url, test_repo_dir)
        self.assertEqual(m.version, __version__)

    @staticmethod
    def test_initialization():
        m = Mizuna(test_repo_url, test_repo_dir)

    def test_networked_drive_warning(self):
        m = Mizuna(test_repo_url, test_repo_dir, True)
        self.assertRaises(RuntimeWarning)


class Tracking(unittest.TestCase):
    m = Mizuna(test_repo_url, test_repo_dir)


class Adding(Tracking):

    def setUp(self) -> None:
        self.m.untrack_all()
        self.assertEqual(self.m.files_tracked_count, 0)

    def test_track_one_single(self):
        self.m.track(file_single1)
        self.assertEqual(self.m.files_tracked_count, 1)
        test_set = {file_single1}
        self.assertSetEqual(self.m.track_list(), test_set)

    def test_track_two_singles(self):
        self.m.track(file_single1, file_single2)
        self.assertEqual(self.m.files_tracked_count, 2)
        test_set = {file_single1, file_single2}
        self.assertSetEqual(self.m.track_list(), test_set)

    def test_track_list(self):
        self.m.track(file_list)
        self.assertEqual(self.m.files_tracked_count, len(file_list))
        test_set = set()
        [test_set.add(x) for x in file_list]
        self.assertSetEqual(self.m.track_list(), test_set)

    def test_track_many(self):
        self.m.track(file_single1, file_single2, file_list)
        self.assertEqual(self.m.files_tracked_count, 2 + len(file_list))
        test_set = {file_single1, file_single2}
        [test_set.add(x) for x in file_list]
        self.assertSetEqual(self.m.track_list(), test_set)


class Removing(Tracking):

    test_set = {file_single1, file_list[0], file_list[1], file_single2}

    def setUp(self) -> None:
        self.m.untrack_all()
        self.assertEqual(self.m.files_tracked_count, 0)
        self.m.track(list(self.test_set))
        self.assertEqual(self.m.files_tracked_count, len(self.test_set))

    def test_remove_one(self):
        self.m.untrack(file_single1)
        self.assertEqual(self.m.files_tracked_count, len(self.test_set) - 1)
        test_set_removed = set(self.test_set)
        test_set_removed.remove(file_single1)
        self.assertSetEqual(self.m.track_list(), test_set_removed)

    def test_remove_all(self):
        self.m.untrack_all()
        self.assertEqual(self.m.files_tracked_count, 0)
        self.assertSetEqual(self.m.track_list(), set())


# class Flow(unittest.TestCase):
#     m = Mizuna(test_repo_url, test_repo_dir)
#     files_tracked = ['figures/price_over_year.pdf']
#
#     def test_flow(self):
#         return
#         self.m.track(self.files_tracked[0])
#         self.m.sync()


if __name__ == '__main__':
    unittest.main()
