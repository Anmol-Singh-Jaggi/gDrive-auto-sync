# gDrive-auto-sync

Automatically backup files to your Google Drive account periodically.

**Dependencies:**
 - `pip install --upgrade google-api-python-client`

**Usage:**
 - Download your *`client_secrets.json`* file from the Google Developer Console and keep it alongside the script.  
   To do this, perform the following steps:
    - Go to [this link](https://console.developers.google.com/project) and make a new project.
    - In the project settings, turn *Drive API* on.
    - In the credentials settings, create an OAuth client ID (choose the application type as *Other*).
    - Click on the *Download JSON* link and save it as *client_secrets.json*.
 - Add the details regarding the files to be uploaded in the *`file_list.json`* file. For new files, keep the `fileId` empty and `parentId` as the ID of the Drive directory in which the file has to be inserted.  
   The ID of a directory can be found be visiting that directory on Google Drive and looking at the alphanumeric string in the URL.  
   ![Finding Directory ID on Google Drive](gDrive-auto-sync/screenshots/gdrive_directory_id.png?raw=true "Finding Directory ID on Google Drive")
 - Modify *`custom_cmds_pre.sh`* and *`custom_cmds_post.sh`* as per your needs.
 - Make sure that the main script is executable - `chmod +x ./run.sh`.
 - For manually running it, just cd into the directory and execute the main script - `./run.sh`.
 - For scheduling it:
   - Modify the contents of *`crontab.txt`* as per your requirements.
   - Execute `crontab -e` to open the crontab edit buffer.
   - Copy the contents of *`crontab.txt`* in the buffer.

**To-Do:**
 - Add support for uploading contents of a folder recursively without archiving.
 - ~~Add support for uploading a file only if it is has been modified. (By comparing hashes)~~
