#!/bin/bash

source ./constants.sh

exit_with_error() {
    echo "$1" >&2
    exit 1
}

echo "[INFO]: Restarting the $SERVICE_NAME service..."
if ! sudo systemctl restart "$SERVICE_NAME.service"; then
    exit_with_error "Failed to restart $SERVICE_NAME service."
fi

if ! systemctl is-active --quiet "$SERVICE_NAME.service"; then
    exit_with_error "$SERVICE_NAME service is not active after restart."
else
    echo "[INFO]: $SERVICE_NAME service restarted successfully."
fi
