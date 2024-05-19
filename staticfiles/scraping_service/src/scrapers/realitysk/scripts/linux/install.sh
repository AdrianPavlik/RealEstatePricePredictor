#!/bin/bash

source constants.sh

if [ $EUID -ne 0 ]; then
  sudo $0 "$@"
  exit
fi

exit_with_error() {
    echo "$1" >&2
    exit 1
}

if ! command -v virtualenv &> /dev/null; then
    echo "Installing virtualenv..." >&2
    apt install --yes python3-virtualenv || exit_with_error "Failed to install python3-virtualenv"
fi

USER_HOME="/home/scraping-control"
USER_NAME="scraping-control"

if getent passwd $USER_NAME &>/dev/null; then
    echo "$USER_NAME user account already exists" >&2
else
    echo "Creating $USER_NAME user account" >&2
    useradd -s /usr/sbin/nologin --create-home $USER_NAME || exit_with_error "Failed to create $USER_NAME user account"
    echo "User account $USER_NAME created successfully" >&2
fi

USER_HOME=$(eval echo ~$USER_NAME)
APP_DIR="$USER_HOME/$DESTINATION_FOLDER"

mkdir -p $APP_DIR || exit_with_error "Failed to create directory at $APP_DIR"

cp "$SCRIPT_SOURCE_PATH" "$APP_DIR/$SCRIPT_NAME" || exit_with_error "Failed to copy $SCRIPT_NAME to $APP_DIR"
cp "$THIS_SCRIPT_REALITYSK_PARENT_DIRECTORY/scraper.py" "$APP_DIR/scraper.py" || exit_with_error "Failed to copy $SCRIPT_NAME to $APP_DIR"
cp -R "$THIS_SCRIPT_MAIN_PARENT_DIRECTORY/src" "$APP_DIR/src" || exit_with_error "Failed to copy src folder to $APP_DIR"
cp "$THIS_SCRIPT_MAIN_PARENT_DIRECTORY/requirements.txt" "$APP_DIR/requirements.txt" || exit_with_error "Failed to copy requirements.txt to $APP_DIR"
cp "$THIS_SCRIPT_LINUX_DIRECTORY/uninstall.sh" "$APP_DIR/uninstall.sh" || exit_with_error "Failed to copy uninstall.sh to $APP_DIR"
cp "$THIS_SCRIPT_LINUX_DIRECTORY/start.sh" "$APP_DIR/start.sh" || exit_with_error "Failed to copy start.sh to $APP_DIR"
cp "$THIS_SCRIPT_LINUX_DIRECTORY/restart.sh" "$APP_DIR/restart.sh" || exit_with_error "Failed to copy restart.sh to $APP_DIR"
cp "$THIS_SCRIPT_LINUX_DIRECTORY/stop.sh" "$APP_DIR/stop.sh" || exit_with_error "Failed to copy stop.sh to $APP_DIR"

chmod +x "$APP_DIR/"*.sh

chown -R $USER_NAME:$USER_NAME $USER_HOME

cp "$THIS_SCRIPT_LINUX_DIRECTORY/$SERVICE_NAME.service" "/etc/systemd/system/$SERVICE_NAME.service" || exit_with_error "Failed to copy systemd service file"
systemctl daemon-reload || exit_with_error "Failed daemon-reload"
sudo systemctl start $SERVICE_NAME || exit_with_error "Failed to start the service"
sudo systemctl enable $SERVICE_NAME || exit_with_error "Failed to enable the service"

echo "Installation and service setup done. $SERVICE_NAME is running!" >&2
