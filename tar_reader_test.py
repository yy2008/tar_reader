#!/usr/bin/env python

import mock
import tarfile
import unittest

from tar_reader import NotValidArchive as NotValidArchive
from tar_reader import TarReader as Reader


TAR_FILE_NAME = 'tar_file'
MEMBERS = []


class MockTarFile(object):
    def close(self):
        pass

    def getmembers(self):
        return MEMBERS


class TarReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.reader = Reader(TAR_FILE_NAME)
        self.mock_tar_file = MockTarFile()

    def test_peek_with_true_tar_file(self):
        with mock.patch.object(tarfile, 'is_tarfile') as mock_is_tarfile:
            with mock.patch.object(tarfile, 'open') as mock_open:
                with mock.patch.object(MockTarFile,
                                       'getmembers') as mock_getmembers:
                    with mock.patch.object(MockTarFile, 'close') as mock_close:
                        mock_is_tarfile.return_value = True
                        mock_open.return_value = self.mock_tar_file

                        self.reader.peek()

                        mock_is_tarfile.assert_called_once_with(TAR_FILE_NAME)
                        mock_open.assert_called_once_with(TAR_FILE_NAME, "r")
                        mock_getmembers.assert_called_once()
                        mock_close.assert_called_once()

    def test_peek_with_false_tar_file(self):
        with mock.patch.object(tarfile, 'is_tarfile') as mock_is_tarfile:
            mock_is_tarfile.return_value = False
            self.assertRaises(NotValidArchive, self.reader.peek)

    def test_peek_with_invalid_tar_file(self):
        with mock.patch.object(tarfile, 'is_tarfile') as mock_is_tarfile:
            mock_is_tarfile.side_effect = IOError()
            self.assertRaises(NotValidArchive, self.reader.peek)


if __name__ == "__main__":
    unittest.main()
