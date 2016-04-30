#!/usr/bin/env bash

for i in `seq 1 3`;
do
 notify-send "gDrive auto-backup started!!"
done


# Get the temporary directory's location
temp_dir_path="temp"

# Remove any existing temp directory
printf "Removing temp directory ...\n"
rm -rf "${temp_dir_path}"
printf "Done!\n\n"

# Make a fresh temp directory
mkdir -p "${temp_dir_path}"

source ./custom_cmds_pre.sh


printf "Executing Python script ...\n"

mkdir -p ./logs
chmod +x ./upload.py
./upload.py > ./logs/$(date +%Y-%m-%d_%H-%M-%S.log) 2>&1

printf "Python script execution complete!\n\n"


source ./custom_cmds_post.sh

# Remove the temp directory
printf "Removing temp directory ...\n"
rm -rf "${temp_dir_path}"
printf "Done!\n\n"


for i in `seq 1 3`;
do
 notify-send "gDrive auto-backup finished!!"
done
