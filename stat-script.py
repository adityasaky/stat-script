#!/usr/bin/env python

import sys
import os
import json


EXCLUDE_PATHS = ('proc', 'sys', 'usr/local/stat-script', 'usr/bin/stat-script')


def _check_exclude(path):
    for to_be_excluded in EXCLUDE_PATHS:
        # super hacky to handle the leading /, eventually requires PathSpec
        if path[1:].startswith(to_be_excluded):
            return True
    return False


def main():
    file_stat = {}
    path = sys.argv[1]
    out = sys.argv[2]
    print("Running stat-script...")
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, followlinks=False,
                                         topdown=True):
            dirs[:] = [d for d in dirs if not d.startswith(EXCLUDE_PATHS)]
            dirpaths = []
            for dirname in dirs:
                dirpaths.append(os.path.normpath(os.path.join(root, dirname)))
            dirs[:] = []
            for dirpath in dirpaths:
                dirs.append(os.path.basename(dirpath))

            filepaths = []
            for filename in files:
                norm_filepath = os.path.normpath(os.path.join(root, filename))
                if os.path.isfile(norm_filepath):
                    filepaths.append(norm_filepath)

            for filepath in filepaths:
                if not _check_exclude(filepath):
                    file_stat[filepath] = os.stat(filepath).st_atime
    elif os.path.isfile(path):
        absolute_path = os.path.abspath(path)
        if not _check_exclude(absolute_path):
            file_stat[absolute_path] = os.stat(path).st_atime

    with open(out, 'w') as f:
        json.dump(file_stat, f, indent=4)


if __name__ == "__main__":
    main()
