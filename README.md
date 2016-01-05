# gDrive-auto-sync

Automatically upload data to your Google Drive account at regular intervals.

**Dependencies:**
 - `pip install --upgrade google-api-python-client`

**Usage:**
 - Download your *`client_secrets.json`* file from the Google Developer Console and keep it alongside the script.
 - Modify the *`file_list.json`* file as per your needs. For new files, keep the `fileId` empty and `parentId` as the ID of the Drive directory in which the file has to be inserted.
 - Modify *`custom_cmds_pre.sh`* and *`custom_cmds_post.sh`* as per your needs.
 - For scheduling it:
   - Execute `crontab -e`.
   - Copy the contents of *`crontab.txt`* in this buffer.
     ( Make sure the script is executable first - `chmod +x run.sh` )
