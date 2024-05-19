#!/bin/bash

source ./constants.sh

exit_with_error() {
    echo "$1" >&2
    exit 1
}

echo "[INFO]: Attempting to stop the $SERVICE_NAME service..."
if ! sudo systemctl stop "$SERVICE_NAME.service"; then
    exit_with_error "$SERVICE_NAME service failed to stop."
fi

if systemctl is-active --quiet "$SERVICE_NAME.service"; then
    exit_with_error "$SERVICE_NAME service failed to stop."
else
    echo "[INFO]: $SERVICE_NAME service stopped successfully."
fi
