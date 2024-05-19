cls

# Get the directory of the script
$ScriptDirectory = $PSScriptRoot

# Set the working directory to the script directory
Set-Location -Path $ScriptDirectory

# Import constants
. .\constants.ps1

# Import helper functions
. .\helpers.ps1

Uninstall-ServiceAction

$filesToExclude = @("database.db", "predaj_model.pkl", "prenajom_model.pkl")
Remove-Files -Path $destinationFolder -Exclude $filesToExclude

exit 0
