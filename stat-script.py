#!/usr/bin/env python

import os
import json
import argparse
import subprocess


EXCLUDE_PATHS = ('proc', 'sys', 'usr/local/stat-script', 'usr/bin/stat-script')
DIFF_EXCLUDE_PATHS = ('/build/', '/srcdest/', '/startdir/', '/logdest/')


def _dump_target(target, target_path):
    with open(target_path, 'w') as f:
        json.dump(target, f, indent=4)


def _check_exclude(path):
    for to_be_excluded in EXCLUDE_PATHS:
        # super hacky to handle the leading /, eventually requires PathSpec
        if path[1:].startswith(to_be_excluded):
            return True
    return False


def record(root_path, target_path):
    file_stat = {}

    print('Recording stat...')

    if os.path.isdir(root_path):
        for root, dirs, files in os.walk(root_path, followlinks=False, topdown=True):
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
    elif os.path.isfile(root_path):
        absolute_path = os.path.abspath(root_path)
        if not _check_exclude(absolute_path):
            file_stat[absolute_path] = os.stat(root_path).st_atime

    _dump_target(file_stat, target_path)


def diff(pre_path, post_path, target_path):
    diff_values = {}

    print('Diff-ing pre and post stat values...')

    with open(pre_path) as fp:
        pre_data = json.load(fp)

    with open(post_path) as fp:
        post_data = json.load(fp)

    for path in post_data:
        if path.startswith(DIFF_EXCLUDE_PATHS):
            continue
        if path in pre_data:
            if pre_data[path] < post_data[path]:
                diff_values[path] = (pre_data[path], post_data[path])
        else:
            diff_values[path] = (None, post_data[path])

    _dump_target(diff_values, target_path)


def find_owners(diff_file_path, target_path):
    ownership = {}

    print('Finding owners...')

    with open(diff_file_path) as fp:
        diff_data = json.load(fp)

    for path in diff_data:
        try:
            output = subprocess.check_output(['pacman', '-Qo', path])
            package, version = output.decode('utf-8').split('owned by')[1].strip().split(' ')
            ownership[path] = (package, version)
        except subprocess.CalledProcessError:
            ownership[path] = 'UNKNOWN'

    _dump_target(ownership, target_path)


def main():
    parser = argparse.ArgumentParser(description='Granular stats for better provenance')

    parser.add_argument('-r', '--record', action='store_true', dest='record_flag')
    parser.add_argument('--root', type=str, dest='root_path')


    parser.add_argument('-d', '--diff', action='store_true', dest='diff_flag')
    parser.add_argument('--pre', type=str, dest='pre_path')
    parser.add_argument('--post', type=str, dest='post_path')

    parser.add_argument('-o', '--find-owners', action='store_true', dest='find_owners_flag')
    parser.add_argument('--diff-file', type=str, dest='diff_file_path')

    parser.add_argument('-t', '--target', type=str, dest='target_path')

    args = parser.parse_args()

    if not args.record_flag and not args.diff_flag and not args.find_owners_flag:
        raise RuntimeError('select an operation')

    if args.record_flag:
        record(args.root_path, args.target_path)

    if args.diff_flag:
        diff(args.pre_path, args.post_path, args.target_path)

    if args.find_owners_flag:
        find_owners(args.diff_file_path, args.target_path)


if __name__ == '__main__':
    main()
