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
    '''
    Returns True if the file with the given drive-id exists,
    False otherwise.
    '''

    if not fileId:
        return False
    try:
        file_service.get(fileId=fileId, fields="").execute()
        return True
    except:
        return False


def create_file(file_path, file_name=None, parentId=None):
    '''
    Insert the file located at 'file_path' with the drive-name 'file_name'
    into the drive-directory with id 'parentId'.
    '''

    # If the input 'file_name' is None,
    # Use the filesystem name of the file as its drive-name
    if not file_name:
        file_name = os.path.basename(file_path)

    mimetype = None
    if not os.path.splitext(os.path.basename(file_path))[1]:
        # Required for files with names like '.astylerc'
        mimetype = "text/plain"

    media_body = MediaFileUpload(file_path, mimetype=mimetype)
    body = {'name': file_name}
    if parentId:
        body['parents'] = [parentId]

    results = file_service.create(
        body=body, media_body=media_body, fields="id").execute()

    return results


def update_file(file_path, fileId):
    '''
    Updates the file with the drive-id 'fileId'.
    '''

    mimetype = None
    if not os.path.splitext(os.path.basename(file_path))[1]:
        # Required for files with names like '.astylerc'
        mimetype = "text/plain"

    media_body = MediaFileUpload(file_path, mimetype)

    results = file_service.update(
        fileId=fileId, media_body=media_body, fields="id").execute()

    return results


def list_files():
    '''
    List some files in random order.
    Currently not used.
    '''

    results = file_service.list(
        pageSize=10, fields="files(id, name)").execute()

    return results


def update_or_create_file(input_file):
    '''
    Updates the file if it exists already on the drive(based on its id).
    Creates a new one otherwise.
    '''

    file_path = input_file['path']
    fileId = input_file['fileId']
    parentId = input_file['parentId']

    if file_exists(fileId):
        return update_file(file_path, fileId)
    else:
        return create_file(file_path, parentId=parentId)


def is_file_modified(input_file):
    '''
    Returns True if the contents of the input file on local storage
    are different from that on its drive counterpart, False otherwise.
    It does this by comparing their hash values.
    '''

    file_path = input_file['path']
    fileId = input_file['fileId']

    if not file_exists(fileId):
        return True

    local_file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

    remote_file_hash = file_service.get(
        fileId=fileId, fields="md5Checksum").execute()['md5Checksum']

    return local_file_hash != remote_file_hash


def archive_directory(dir_path):
    '''
    Create an archive of the directory's contents.
    Returns the path of the archive created.
    '''

    archive_path = dir_path + ".tar.xz"

    # Remove the previous archive
    if os.path.exists(archive_path):
        os.remove(archive_path)

    subprocess.check_call(["tar", "-caf", archive_path, "-C", dir_path, "."])

    return archive_path


def main():
    file_list_file_path = "file_list.json"

    in_file = open(file_list_file_path)
    file_list = json.load(in_file)
    in_file.close()

    for input_file in file_list:
        print(str(input_file))
        sys.stdout.flush()

        file_path = input_file['path']
        if os.path.isdir(file_path):
            file_path = archive_directory(file_path)

        # Creating a backup object to prevent changing
        # 'dir_path' to 'dir_path.tar.xz' in the output json file
        input_file_new = dict(input_file)
        input_file_new['path'] = file_path

        if is_file_modified(input_file_new):
            results = update_or_create_file(input_file_new)
            input_file['fileId'] = results['id']

        # Delete the archive file
        if os.path.isdir(input_file['path']):
            os.remove(file_path)

    # Write the list to the json file again
    # as it may contain new fileId's for some files
    out_file = open(file_list_file_path, "w")
    json.dump(file_list, out_file, indent=4)
    out_file.close()

    print("Done!!")


if __name__ == '__main__':
    main()
