# Get the current username
$currentUsername = $env:USERNAME

# Service Constants
$serviceName = "RealEstateScrapingService"
$scriptName = "ScrapingController.py"
$executableScriptName = "ScrapingController.exe"
$winswName = "WinSW.exe"
$winswTemplateConfigName = "scraping_service_winsw_configuration_template.xml"
$winswConfigName = "scraping_service_winsw_configuration.xml"
$displayName = "Real Estate Predictor - Scraping Service"
$description = "This service ensures that the data are scraped so the prices can be predicted."

# Variables that are glued together
$thisScriptPath = $MyInvocation.MyCommand.Path
$thisScriptParentDirectory = Split-Path $thisScriptPath -Parent
$thisScriptParentParentDirectory = Split-Path $thisScriptParentDirectory -Parent
$sourceScriptDirectory = Split-Path $thisScriptParentParentDirectory -Parent
$helperScriptTemplateDirectoryLocation = "src\utils\helpers\helper_template.py"
$helperScriptDirectoryLocation = "src\utils\helpers\helper.py"
$templatesDirectoryLocation = "src\templates"
$helperScriptTemplateDirectoryPath = Join-Path -Path $sourceScriptDirectory -ChildPath $helperScriptTemplateDirectoryLocation
$helperScriptDirectoryPath = Join-Path -Path $sourceScriptDirectory -ChildPath $helperScriptDirectoryLocation
$scriptSourcePath = Join-Path -Path $sourceScriptDirectory -ChildPath $scriptName
$templatesDirectoryPath = Join-Path -Path $sourceScriptDirectory -ChildPath $templatesDirectoryLocation
$destinationFolder = "C:\Users\$currentUsername\AppData\Roaming\RealEstateWebScraper\ScrapingService"
$winswDestinationFolder = "C:\Users\$currentUsername\AppData\Roaming\RealEstateWebScraper"
$templatesDestinationFolder = "C:\Users\$currentUsername\AppData\Roaming\RealEstateWebScraper\ScrapingService\templates"
$executableScriptDestinationFolder = Join-Path -Path $destinationFolder -ChildPath $executableScriptName

$winswDestinationConfigPath = Join-Path -Path $destinationFolder -ChildPath $winswConfigName
$winswDestinationExePath = Join-Path -Path $winswDestinationFolder -ChildPath $winswName
$winswPath = Join-Path -Path $PSScriptRoot -ChildPath $winswName
$winswTemplateConfigPath = Join-Path -Path $PSScriptRoot -ChildPath $winswTemplateConfigName
$winswConfigPath = Join-Path -Path $PSScriptRoot -ChildPath $winswConfigName

