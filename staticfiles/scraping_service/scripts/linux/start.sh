#!/bin/bash

exit_with_error() {
    echo $1 >&2
    exit 1
}

if ! command -v virtualenv &> /dev/null; then
    exit_with_error "virtualenv command could not be found"
fi

if [ ! -d "venv" ]; then
    virtualenv -p python3 venv
    source venv/bin/activate
    pip -q install --upgrade -r requirements.txt
else
    source venv/bin/activate
fi

echo "starting controller"
python3 ScrapingController.py


