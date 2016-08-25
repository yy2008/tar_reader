#!/usr/bin/env python

import argparse
import tarfile
import time


class NotValidArchive(Exception):
    pass


class TarReader(object):
    def __init__(self, arch):
        self.arch = arch

    def peek(self):
        try:
            if tarfile.is_tarfile(self.arch):
                #with tarfile.open(self.arch, "r") as files:
                files = tarfile.open(self.arch, "r")
                for f in files.getmembers():
                    print "{} {}".format(time.ctime(f.mtime), f.name)
                files.close()
            else:
                raise NotValidArchive(self.arch + " is not valid archive")
        except IOError:
            raise NotValidArchive(self.arch + " is not valid archive")


def main():
    parser = argparse.ArgumentParser(
        description="Read contents of an archive"
    )
    parser.add_argument(
        "archive_name",
        help="the name of file archive to be inspected"
    )
    args = parser.parse_args()
    reader = TarReader(args.archive_name)
    reader.peek()


if __name__ == "__main__":
    main()
