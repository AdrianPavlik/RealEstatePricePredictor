cls

# Get the directory of the script
$ScriptDirectory = $PSScriptRoot

# Set the working directory to the script directory
Set-Location -Path $ScriptDirectory

# Import helper functions
. .\helpers.ps1

Stop-ServiceAction

Start-ServiceAction

exit 0