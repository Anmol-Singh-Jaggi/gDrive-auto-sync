# Commands to be run before invoking the main script

temp_dir_path="/home/anmol/auto-backup-temp"
mkdir -p "${temp_dir_path}"

directory_snapshot "/media/Data/anmol" "${temp_dir_path}/snapshot" "${temp_dir_path}/snapshot_logs"
comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u) > "${temp_dir_path}/manually_installed_apps.txt"
