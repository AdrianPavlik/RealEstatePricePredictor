#!/bin/bash

# Get the current username
export CURRENT_USERNAME=$(whoami)

# Service Constants
export SERVICE_NAME="RealEstateScrapingService"
export SCRIPT_NAME="ScrapingController.py"
export DISPLAY_NAME="Real Estate Predictor - Scraping Service"
export DESCRIPTION="This service ensures that the data are scraped so the prices can be predicted."

# Variables that are glued together
export THIS_SCRIPT_PATH="$(readlink -f "$0")"
export THIS_SCRIPT_PARENT_DIRECTORY=$(dirname "$THIS_SCRIPT_PATH")
export THIS_SCRIPT_PARENT_PARENT_DIRECTORY=$(dirname "$THIS_SCRIPT_PARENT_DIRECTORY")
export SOURCE_SCRIPT_DIRECTORY=$(dirname "$THIS_SCRIPT_PARENT_PARENT_DIRECTORY")
export HELPER_SCRIPT_TEMPLATE_DIRECTORY_LOCATION="src/utils/helpers/helper_template.py"
export HELPER_SCRIPT_DIRECTORY_LOCATION="src/utils/helpers/helper.py"
export TEMPLATES_DIRECTORY_LOCATION="src/templates"
export HELPER_SCRIPT_TEMPLATE_DIRECTORY_PATH="$SOURCE_SCRIPT_DIRECTORY/$HELPER_SCRIPT_TEMPLATE_DIRECTORY_LOCATION"
export HELPER_SCRIPT_DIRECTORY_PATH="$SOURCE_SCRIPT_DIRECTORY/$HELPER_SCRIPT_DIRECTORY_LOCATION"
export SCRIPT_SOURCE_PATH="$SOURCE_SCRIPT_DIRECTORY/$SCRIPT_NAME"
export TEMPLATES_DIRECTORY_PATH="$SOURCE_SCRIPT_DIRECTORY/$TEMPLATES_DIRECTORY_LOCATION"
export DESTINATION_FOLDER="RealEstateWebScraper/ScrapingService"
export TEMPLATES_DESTINATION_FOLDER="/home/$CURRENT_USERNAME/.config/RealEstateWebScraper/ScrapingService/templates"
