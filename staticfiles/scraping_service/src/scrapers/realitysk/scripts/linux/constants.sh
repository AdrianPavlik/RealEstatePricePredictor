#!/bin/bash

# Get the current username
export CURRENT_USERNAME=$(whoami)

# Service Constants
export SERVICE_NAME="RealitySKRealEstateScrapingService"
export SCRIPT_NAME="RealityScrapingController.py"
export DISPLAY_NAME="Real Estate Predictor - RealitySK Scraping Service"
export DESCRIPTION="This service ensures that the data are scraped from RealitySK so the prices can be predicted."

# Variables that are glued together
export THIS_SCRIPT_PATH="$(readlink -f "$0")"
export THIS_SCRIPT_LINUX_DIRECTORY=$(dirname "$THIS_SCRIPT_PATH")
export THIS_SCRIPT_SCRIPTS_PARENT_DIRECTORY=$(dirname "$THIS_SCRIPT_LINUX_DIRECTORY")
export THIS_SCRIPT_REALITYSK_PARENT_DIRECTORY=$(dirname "$THIS_SCRIPT_SCRIPTS_PARENT_DIRECTORY")
export THIS_SCRIPT_SCRAPERS_PARENT_DIRECTORY=$(dirname "$THIS_SCRIPT_REALITYSK_PARENT_DIRECTORY")
export THIS_SCRIPT_SRC_PARENT_DIRECTORY=$(dirname "$THIS_SCRIPT_SCRAPERS_PARENT_DIRECTORY")
export THIS_SCRIPT_MAIN_PARENT_DIRECTORY=$(dirname "$THIS_SCRIPT_SRC_PARENT_DIRECTORY")
export SCRIPT_SOURCE_PATH="$THIS_SCRIPT_REALITYSK_PARENT_DIRECTORY/$SCRIPT_NAME"
export DESTINATION_FOLDER="RealEstateWebScraper/RealitySKScrapingService"
