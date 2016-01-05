#!/usr/bin/env bash

for i in `seq 1 3`;
do
 notify-send "gDrive auto-backup started!!"
done

chmod +x ./custom_cmds_pre.sh
./custom_cmds_pre.sh

mkdir -p logs
chmod +x ./upload.py
./upload.py > ./logs/$(date +%Y-%m-%d_%H-%M-%S.log) 2>&1

chmod +x ./custom_cmds_post.sh
./custom_cmds_post.sh

for i in `seq 1 3`;
do
 notify-send "gDrive auto-backup finished!!"
done
