# gDrive-auto-sync

Automatically upload data to your Google Drive account at regular intervals.

**Dependencies:**
 - `pip install --upgrade google-api-python-client`

**Usage:**
 - Download your *`client_secrets.json`* file from the Google Developer Console and keep it alongside the script.
 - Add the details regarding the files to be uploaded in the *`file_list.json`* file. For new files, keep the `fileId` empty and `parentId` as the ID of the Drive directory in which the file has to be inserted.
 - Modify *`custom_cmds_pre.sh`* and *`custom_cmds_post.sh`* as per your needs.
 - Make sure that the main script is executable - `chmod +x ./run.sh`.
 - For manually running it, just cd into the directory and execute the main script - `./run.sh`.
 - For scheduling it:
   - Modify the contents of *`crontab.txt`* as per your requirements.
   - Execute `crontab -e` to open the crontab edit buffer.
   - Copy the contents of *`crontab.txt`* in the buffer.

**To-Do:**
 - Add support for uploading contents of a folder recursively without archiving.
 - Add support for uploading a file only if it is has been modified. (By comparing hashes)
