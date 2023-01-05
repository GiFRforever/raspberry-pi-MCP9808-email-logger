#!/bin/bash

# Exit immediately if a command returns a non-zero exit code
set -e

# Check if the script is being run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Check if the required packages are already installed
REQUIRED_PACKAGES=`grep -E "^[^#]" requirements.txt`
INSTALLED_PACKAGES=`pip freeze`

# Install any missing packages
for package in $REQUIRED_PACKAGES; do
  if ! echo "$INSTALLED_PACKAGES" | grep -q "$package"; then
    pip install "$package"
  fi
done

# Copy the service file and enable it
cp templogger.service /lib/systemd/system/
chmod 644 /lib/systemd/system/templogger.service
systemctl daemon-reload
systemctl enable templogger.service

# Start the service, unless it's already running
if ! systemctl is-active --quiet templogger.service; then
  systemctl start templogger.service
fi

# Set up the aliases, unless they already exist
if ! grep -q "alias sm=" ~/.bashrc; then
  echo "alias sm='python /home/pi/templogger/sendmail.py'" >> ~/.bashrc
fi

if ! grep -q "alias rt=" ~/.bashrc; then
  echo "alias rt='python /home/pi/templogger/readtemp.py'" >> ~/.bashrc
fi

# Reload the bashrc file to apply the changes
source ~/.bashrc
