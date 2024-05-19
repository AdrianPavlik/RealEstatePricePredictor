cls

# Get the directory of the script
$ScriptDirectory = $PSScriptRoot

# Set the working directory to the script directory
Set-Location -Path $ScriptDirectory

# Import constants
. .\constants.ps1

# Import helper functions
. .\helpers.ps1

# Create the destination folder if it doesn't exist
Write-Host "[INFO]: Creating folder at $destinationFolder"
try {
    if (-not (Test-Path -Path $destinationFolder -PathType Container)) {
        New-Item -Path $destinationFolder -ItemType Directory
        Write-Host "[INFO]: Folder was created!"
    } else {
        # Remove specific files in the destination folder
        $filesToExclude = @("database.db")
        Remove-Files -Path $destinationFolder -Exclude $filesToExclude
        Write-Host "[INFO]: Existing files related to the script were removed!"
    }
} catch {
    Write-Host "[ERROR]: $_"
    pause
    exit 1
}

function genereate_winsw_configuration_file {
    Write-Host "[INFO]: Generating winsw configuration file"
    # Read the contents of the original configuration file
    $configContent = Get-Content -Path $winswTemplateConfigPath -Raw

    # Replace placeholders with dynamic values
    $configContent = $configContent -replace '{ServiceId}', $serviceName
    $configContent = $configContent -replace '{ServiceName}', $displayName
    $configContent = $configContent -replace '{ServiceDescription}', $description
    $configContent = $configContent -replace '{ExecutablePath}', $executableScriptDestinationFolder

    # Save the modified configuration to a new file
    $configContent | Set-Content -Path $winswConfigPath
    Write-Host "[INFO]: Generating winsw configuration file was successful"
    Write-Host "[INFO]: Copying winsw configuration files to $destinationFolder"
    Copy-Item -Path $winswConfigPath -Destination $destinationFolder -Force
    Remove-Item -Path $winswConfigPath -Force
    Write-Host "[INFO]: Copying winsw configuration files was successful"
}

# Use PyInstaller to convert Python script to exe
Write-Host "[INFO]: Converting python script to executable file"
try {
    genereate_winsw_configuration_file
    pyinstaller --onefile $scriptSourcePath --distpath $destinationFolder --log-level=ERROR
    Remove-Item -Recurse -Force ".\build"
    Remove-Item -Recurse -Force ".\RealityScrapingController.spec"
} catch {
    # Check if pyinstaller was found - due to exporting .exe file of the python script
    Write-Host "[INFO]: Checking if pyinstaller is present."
    try {
        if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Definition)) {
            Write-Host "[ERROR]: Pyinstaller was not located."
            # Check if pip was found
            Write-Host "[INFO]: Checking if pip is present."
            if (-not (Get-Command pip -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Definition)) {
                Write-Host "[ERROR]: Pip was not located. To run this script, you need pip."
                # Check if Python executable was found
                Write-Host "[INFO]: Checking if python is present."
                if (-not (Get-Command python.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Definition)) {
                    throw "[ERROR]: Python executable not found in the system PATH. Please install Python or provide the correct path."
                } else {
                    Write-Host "[INFO]: Python Found!"
                }
            } else {
                Write-Host "[INFO]: Pip Found!"
                # Install pyinstaller
                Write-Host "[INFO]: Installing package pyinstaller"
                pip install pyinstaller -q
                Write-Host "[INFO]: Installing pyinstaller was successful"
            }
        } else {
            Write-Host "[INFO]: Pyinstaller Found!"
        }
    } catch {
        Write-Host "[ERROR]: $_"
        pause
        exit 1
    }
}

# Install the service
Install-ServiceAction

# Start the service
Start-ServiceAction

exit 0
