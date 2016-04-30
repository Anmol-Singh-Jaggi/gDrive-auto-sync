#!/usr/bin/env python
from __future__ import print_function

import os
import tempfile


def get_temp_dir_path():
    return os.path.join(tempfile.gettempdir(), 'gDrive_auto_backup_temp')


def main():
    print(get_temp_dir_path())

if __name__ == '__main__':
    main()
