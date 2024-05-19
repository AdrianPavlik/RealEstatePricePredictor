# Get the current username
$currentUsername = $env:USERNAME

# Service Constants
$masterServiceName = "RealEstateScrapingService"
$serviceName = "RealityScrapingService"
$scriptName = "RealityScrapingController.py"
$executableScriptName = "RealityScrapingController.exe"
$winswName = "WinSW.exe"
$winswTemplateConfigName = "reality_scraping_service_winsw_configuration_template.xml"
$winswConfigName = "reality_scraping_service_winsw_configuration.xml"
$displayName = "Real Estate Predictor - Reality.sk Scraping Service"
$description = "This service ensures that the data from reality.sk are scraped."

# Variables that are glued together
$thisScriptPath = $MyInvocation.MyCommand.Path
$thisScriptParentDirectory = Split-Path $thisScriptPath -Parent
$thisScriptParentParentDirectory = Split-Path $thisScriptParentDirectory -Parent
$sourceScriptDirectory = Split-Path $thisScriptParentParentDirectory -Parent
$scriptSourcePath = Join-Path -Path $sourceScriptDirectory -ChildPath $scriptName
$destinationFolder = "C:\Users\$currentUsername\AppData\Roaming\RealEstateWebScraper\RealityScrapingService"
$winswDestinationFolder = "C:\Users\$currentUsername\AppData\Roaming\RealEstateWebScraper"
$executableScriptDestinationFolder = Join-Path -Path $destinationFolder -ChildPath $executableScriptName

$winswDestinationConfigPath = Join-Path -Path $destinationFolder -ChildPath $winswConfigName
$winswDestinationExePath = Join-Path -Path $winswDestinationFolder -ChildPath $winswName
$winswPath = Join-Path -Path $PSScriptRoot -ChildPath $winswName
$winswTemplateConfigPath = Join-Path -Path $PSScriptRoot -ChildPath $winswTemplateConfigName
$winswConfigPath = Join-Path -Path $PSScriptRoot -ChildPath $winswConfigName

