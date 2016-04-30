# Commands to be run after invoking the main script

mv /home/anmol/.config.google-chrome /home/anmol/.config/google-chrome

# Remove the temp directory
printf "Removing temp directory ...\n"
rm -rf "${temp_dir_path}"
printf "Done!\n\n"
