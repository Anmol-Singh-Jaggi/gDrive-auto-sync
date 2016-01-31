#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import json
import subprocess
import hashlib

from apiclient.http import MediaFileUpload
from api_boilerplate import file_service


def file_exists(fileId):
    """
    Checks whether a file exists on the Drive or not.
    :param fileId: The ID of the file to check.
    :type fileId: str
    :returns: bool
    """
    if not fileId:
        return False
    try:
        # Get the file metadata for trashed field 
        # if true, then it doesn't exist in drive
        file_metadata = file_service.get(fileId=fileId, fields="trashed").execute()
        if (file_metadata['trashed']) == True:
            return False
        else:
            return True
    except Exception:
        return False


def create_file(file_path, parentId=None):
    """
    Creates a new file on the Drive.
    :param file_path: The path of the source file on local storage.
    :type file_path: str
    :param parentId: The ID of the directory in which the file has to be
    created. If it is None, the file will be created in the root directory.
    :type parentId: str or None
    :returns: A dictionary containing the ID of the file created.
    """
    media_body = MediaFileUpload(
        file_path, mimetype="application/octet-stream")

    body = {'name': os.path.basename(file_path)}
    if parentId:
        body['parents'] = [parentId]

    results = file_service.create(
        body=body, media_body=media_body, fields="id").execute()

    return results


def update_file(file_path, fileId):
    """
    Modifies an already existing file on the Drive.
    :param file_path: The path of the source file on local storage.
    :type file_path: str
    :param fileId: The ID of the file to be modified.
    :type fileId: str
    :returns: A dictionary containing the ID of the file modified.
    """
    media_body = MediaFileUpload(
        file_path, mimetype="application/octet-stream")

    results = file_service.update(
        fileId=fileId, media_body=media_body, fields="id").execute()

    return results


def list_files():
    """
    List some of the files on the Drive.
    :returns: A dictionary containing the list of file-details.
    """
    results = file_service.list(
        pageSize=10, fields="files(id, name)").execute()

    return results


def update_or_create_file(input_file):
    """
    Updates the file if it exists already on the Drive, else creates a new one.
    :param input_file: A dictionary containing the details about the file.
    The required details are 'path', 'fileId' and 'parentId'.
    :type input_file: dict
    :returns: A dictionary containing the details about the file.
    """
    file_path = input_file['path']
    fileId = input_file['fileId']
    parentId = input_file['parentId']

    if file_exists(fileId):
        return update_file(file_path, fileId)
    else:
        return create_file(file_path, parentId)


def is_file_modified(input_file):
    """
    Checks whether a file on the Drive is different from its local counterpart.
    It does this by comparing their hash values.
    :param input_file: A dictionary containing the details about the file.
    The required details(keys) are 'path' and 'fileId'.
    :type input_file: dict
    :returns: bool
    """
    file_path = input_file['path']
    fileId = input_file['fileId']

    # If the file does not exist on the Drive,
    # then return true.
    if not file_exists(fileId):
        return True

    remote_file_hash = file_service.get(
        fileId=fileId, fields="md5Checksum").execute()['md5Checksum']

    local_file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

    return local_file_hash != remote_file_hash


def archive_directory(dir_path):
    """
    Creates an archive of the directory's contents.
    :param dir_path: The path of the directory on local storage.
    :type dir_path: str
    :returns: str -- The path of the archive created.
    """
    archive_path = dir_path + ".tar.xz"

    # Remove the previous archive if it exists
    if os.path.exists(archive_path):
        os.remove(archive_path)

    subprocess.check_call(["tar", "-caf", archive_path, "-C", dir_path, "."])

    return archive_path


def main():
    file_list_file_path = "file_list.json"

    with open(file_list_file_path) as in_file:
        file_list = json.load(in_file)

    for input_file in file_list:
        print(str(input_file))
        sys.stdout.flush()

        file_path = input_file['path']
        if os.path.isdir(file_path):
            # If it is a directory, its archive will be uploaded.
            file_path = archive_directory(file_path)

        # Creating a backup object to prevent changing
        # 'dir_path' to 'dir_path.tar.xz' in the output json file.
        input_file_new = dict(input_file)
        input_file_new['path'] = file_path

        if is_file_modified(input_file_new):
            results = update_or_create_file(input_file_new)
            input_file['fileId'] = results['id']

        # Delete the archive file.
        if os.path.isdir(input_file['path']):
            os.remove(file_path)

    # Write the list to the json file again
    # as it may contain new fileId's for some files.
    with open(file_list_file_path, "w") as out_file:
        json.dump(file_list, out_file, indent=4, sort_keys=True)

    print("Done!!")


if __name__ == '__main__':
    main()
