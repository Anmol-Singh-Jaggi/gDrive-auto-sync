# Commands to be run before invoking the main script

temp_dir_path="/home/anmol/.auto-backup-temp"
mkdir -p "${temp_dir_path}"

# Execute directory snapshot
directory_snapshot "/media/Data/anmol" "${temp_dir_path}/snapshot" "${temp_dir_path}/snapshot_logs"

# List the manually installed applications
comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u) > "${temp_dir_path}/manually_installed_apps.txt"

# List the PPA's installed
grep -RoPish "ppa.launchpad.net/[^/]+/[^/ ]+" /etc/apt | sort -u | sed -r 's/\.[^/]+\//:/' > "${temp_dir_path}/installed_ppa_list.txt"

# Move Google Chrome's config out due to its large size
mv /home/anmol/.config/google-chrome /home/anmol/.config.google-chrome

# Archive all the .rc files in the home directory
# Activate the 'dotglob' option so that the wildcard '*' includes hidden files as well
shopt -s dotglob
cd /home/anmol && tar -caf "${temp_dir_path}/rc.tar.xz" *rc
shopt -u dotglob
