#!/bin/bash

source ./constants.sh

exit_with_error() {
    echo "$1" >&2
    exit 1
}

SERVICE_FILE="/lib/systemd/system/$SERVICE_NAME.service"

echo "[INFO]: Stopping the $SERVICE_NAME service..."
if ! sudo systemctl stop "$SERVICE_NAME.service"; then
    exit_with_error "Failed to stop $SERVICE_NAME service."
fi

echo "[INFO]: Disabling the $SERVICE_NAME service..."
if ! sudo systemctl disable "$SERVICE_NAME.service"; then
    exit_with_error "Failed to disable $SERVICE_NAME service."
fi

if [ -f "$SERVICE_FILE" ]; then
    echo "[INFO]: Removing the systemd service file..."
    if ! sudo rm "$SERVICE_FILE"; then
        exit_with_error "Failed to remove systemd service file."
    fi

    if ! sudo systemctl daemon-reload; then
        exit_with_error "Failed to reload systemd."
    else
        echo "[INFO]: Systemd reloaded."
    fi
else
    echo "[WARNING]: Service file not found, maybe it was already removed?"
fi

echo "[INFO]: Cleaning up installation files and directories..."
if ! sudo rm -rf "$DESTINATION_FOLDER"; then
    exit_with_error "Failed to remove installation files and directories."
fi

if getent passwd $CURRENT_USERNAME &>/dev/null; then
    echo "[INFO]: Removing user account $CURRENT_USERNAME..."
    if ! sudo userdel -r $CURRENT_USERNAME; then
        exit_with_error "Failed to remove user account $CURRENT_USERNAME."
    fi
fi

if getent passwd scraping-control &>/dev/null; then
    echo "[INFO]: Removing user account scraping-control..."
    if ! sudo userdel -r scraping-control; then
        exit_with_error "Failed to remove user account scraping-control."
    fi
fi

echo "[INFO]: Uninstallation complete. The $SERVICE_NAME has been removed from the system."
s