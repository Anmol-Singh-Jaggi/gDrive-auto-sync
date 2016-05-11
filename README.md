# gDrive-auto-sync

Automatically backup files to your Google Drive account periodically.

**Dependencies:**
 - `pip install google-api-python-client`

**Usage:**
 - Download your *`client_secrets.json`* file from the Google Developer Console and keep it alongside the script.  
   To do this, perform the following steps:
    - Go to [this link](https://console.developers.google.com/project) and make a new project.
    - In the project settings, turn *Drive API* on.
    - In the credentials settings, create an OAuth client ID (choose the application type as *Other*).
    - Click on the *Download JSON* link and save it as *client_secrets.json* in your working directory.
 - Replace the value of the *APPLICATION_NAME* variable in the *`api_boilerplate.py`* file with the name of the project created in the previous step.
 - Add the details regarding the files to be uploaded in the *`file_list.json`* file. For new files, keep the `fileId` empty and `parentId` as the ID of the Drive directory in which the file has to be inserted.  
   The ID of a directory can be found be visiting that directory on Google Drive and looking at the alphanumeric string in the URL.  
   ![Image highlighting the ID of a directory on Google Drive.](gDrive-auto-sync/screenshots/gdrive_directory_id.png?raw=true "Finding Directory ID on Google Drive")
 - Modify *`custom_cmds_pre.sh`* and *`custom_cmds_post.sh`* as per your needs.
 - Make sure that the main script is executable - `chmod +x ./run.sh`.
 - For manually running it, just cd into the directory and execute the main script - `./run.sh`.  
   If you are running it for the first time, you will be asked to authenticate yourself with Google.
 - For scheduling it using [`cron`](https://en.wikipedia.org/wiki/Cron):
   - Modify the contents of *`crontab.txt`* as per your needs.
   - Execute `crontab -e` to open the crontab edit buffer.
   - Copy the contents of *`crontab.txt`* in the buffer and save it.
   - ***TIP:*** In case you need to execute [`notify-send`](http://ss64.com/bash/notify-send.html) from cron, follow the steps given [here](https://anmolsinghjaggi.wordpress.com/2016/05/11/notify-send-in-ubuntu-16-lts/).

**To-Do:**
 - Add support for uploading contents of a folder recursively without archiving.
 - ~~Add support for uploading a file only if it is has been modified. (By comparing hashes)~~
