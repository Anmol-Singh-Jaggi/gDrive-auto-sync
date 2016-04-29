# Commands to be run before invoking the main script

home="/home/anmol"
temp_dir_path="${home}/.auto-backup-temp"
mkdir -p "${temp_dir_path}"

# Execute directory snapshot
directory_snapshot "/media/Data/anmol" "${temp_dir_path}/snapshot" "${temp_dir_path}/snapshot_logs"

# List the manually installed applications
comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u) > "${temp_dir_path}/manually_installed_apps.txt"

# List the PPA's installed
grep -RoPish "ppa.launchpad.net/[^/]+/[^/ ]+" /etc/apt | sort -u | sed -r 's/\.[^/]+\//:/' > "${temp_dir_path}/installed_ppa_list.txt"

# Move Google Chrome's config out due to its large size
mv "${home}/.config/google-chrome" "${home}/.config.google-chrome"

# Archive all the .rc files in the home directory
rc_path="${temp_dir_path}/rc"
mkdir rc_path
# Activate the 'dotglob' option so that the wildcard '*' includes hidden files as well
shopt -s dotglob
cp "${home}"/*rc "${rc_path}"
shopt -u dotglob
