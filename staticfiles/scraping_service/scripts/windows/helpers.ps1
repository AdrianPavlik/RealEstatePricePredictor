# Import constants
. .\constants.ps1

<#
.SYNOPSIS
   Checks if service exists.
#>
function Exists-ServiceAction {
    # Check if the service is actually deleted
    $serviceExists = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    return [bool]($serviceExists)
}

<#
.SYNOPSIS
   Installs a service using winsw.exe.
.DESCRIPTION
   This function installs a service using the specified winsw.exe file.
#>
function Install-ServiceAction {
    try {
        & $winswDestinationExePath install $winswDestinationConfigPath

        # Check if the service is actually installed
        if (-not (Exists-ServiceAction)) {
            throw "Service $serviceName could not be installed."
            $filesToExclude = @("database.db", "predaj_model.pkl", "prenajom_model.pkl")
            Remove-Files -Path $destinationFolder -Exclude $filesToExclude
            exit 1
        }

        Write-Host "[INFO]: Service $serviceName installed."
    } catch {
        Write-Host "[ERROR]: $_"
        $filesToExclude = @("database.db", "predaj_model.pkl", "prenajom_model.pkl")
        Remove-Files -Path $destinationFolder -Exclude $filesToExclude
        pause
        exit 1
    }
}

<#
.SYNOPSIS
   Starts a service using winsw.exe.
.DESCRIPTION
   This function starts a service using the specified winsw.exe file and configuration.
#>
function Start-ServiceAction {
    try {
        if (-not (Exists-ServiceAction)) {
            throw "Service $serviceName does not exist. Service cannot be started."
            exit 1
        }

        & $winswDestinationExePath start $winswDestinationConfigPath

        # Check if the service is actually running
        $serviceStatus = (Get-Service -Name $serviceName).Status
        if ($serviceStatus -ne 'Running') {
            throw "Service $serviceName could not be started. $serviceStatus"
            exit 1
        }

        Write-Host "[INFO]: Service $serviceName started."
    } catch {
        Write-Host "[ERROR]: $_"
        pause
        exit 1
    }
}

<#
.SYNOPSIS
   Stops a service using winsw.exe.
.DESCRIPTION
   This function stops a service using the specified winsw.exe file and configuration.
#>
function Stop-ServiceAction {
    try {
        if (-not (Exists-ServiceAction)) {
            "Service $serviceName does not exist. Service will not be stopped. Skipping."
        } else {
            & $winswDestinationExePath stop $winswDestinationConfigPath
            $serviceStatus = (Get-Service -Name $serviceName).Status
            if ($serviceStatus -ne 'Stopped') {
                throw "Service $serviceName could not be stopped. $serviceStatus"
                exit 1
            }
            Write-Host "[INFO]: Service $serviceName stopped."
        }
    } catch {
        Write-Host "[ERROR]: $_"
        pause
        exit 1
    }
}

<#
.SYNOPSIS
   Restarts a service using winsw.exe.
.DESCRIPTION
   This function restarts a service using the specified winsw.exe file and configuration.
#>
function Restart-ServiceAction {
    try {
        if (-not (Exists-ServiceAction)) {
            throw "Service $serviceName does not exist. Service cannot be restarted."
            exit 1
        }

        & $winswDestinationExePath restart $winswDestinationConfigPath

        # Check if the service is actually running
        $serviceStatus = (Get-Service -Name $serviceName).Status
        if ($serviceStatus -ne 'Running') {
            throw "Service $serviceName could not be restarted. $serviceStatus"
            exit 1
        }

        Write-Host "[INFO]: Service $serviceName restarted."
    } catch {
        Write-Host "[ERROR]: $_"
        pause
        exit 1
    }
}

<#
.SYNOPSIS
   Uninstalls a service using winsw.exe.
.DESCRIPTION
   This function deletes a service using the specified winsw.exe file.
#>
function Uninstall-ServiceAction {
    try {
        if (-not (Exists-ServiceAction)) {
            throw Write-Host "[ERROR]: Service $serviceName does not exist. Cannot uninstall the service."
            exit 1
        } else {
            Stop-ServiceAction
        }

        & sc.exe delete $serviceName
        $filesToExclude = @("database.db", "predaj_model.pkl", "prenajom_model.pkl")
        Remove-Files -Path $destinationFolder -Exclude $filesToExclude

        # Check if the service is actually deleted
        if (Exists-ServiceAction) {
            throw "Service $serviceName could not be deleted."
            exit 1
        }

        Write-Host "[INFO]: Service $serviceName deleted."
    } catch {
        Write-Host "[ERROR]: $_"
        pause
        exit 1
    }
}

<#
.SYNOPSIS
   Gets a status using winsw.exe.
.DESCRIPTION
   This function get a service status using the specified winsw.exe file and configuration.
#>
function GetStatus-ServiceAction {
    try {
        if (-not (Exists-ServiceAction)) {
            throw "Service $serviceName does not exist. Cannot get status from service."
            exit 1
        }

        $winswOutput = & $winswDestinationExePath status $winswDestinationConfigPath

        $serviceStatus = (Get-Service -Name $serviceName).Status
        $statusObject = [PSCustomObject]@{
            ServiceName    = $serviceName
            WinswOutput    = $winswOutput
            ServiceStatus  = $serviceStatus
        }

        return $statusObject
    } catch {
        Write-Host "[ERROR]: $_"
        pause
        exit 1
    }
}

<#
.SYNOPSIS
   Refreshes the service properties without reinstallation using winsw.exe.
.DESCRIPTION
   Refreshes the service properties without reinstallation.
#>
function Refresh-ServiceAction {
    try {
        if (-not (Exists-ServiceAction)) {
            throw "Service $serviceName does not exist."
            exit 1
        }

        & $winswDestinationExePath refresh $winswDestinationConfigPath

        Write-Host "[INFO]: Service $serviceName refreshed."
    } catch {
        Write-Host "[ERROR]: $_"
        pause
        exit 1
    }
}


# Function to remove all files from a directory except those listed in Exclude parameter
function Remove-Files {
    param (
        [string]$Path,
        [string[]]$Exclude = @()
    )

    # Get a list of files in the directory
    $allFiles = Get-ChildItem -Path $Path -File

    # Filter files to keep, excluding those specified in the Exclude parameter
    $filesToKeep = $allFiles | Where-Object { $_.Name -notin $Exclude }

    # Remove each file that is not in the Exclude list
    foreach ($fileToKeep in $filesToKeep) {
        $filePath = Join-Path -Path $Path -ChildPath $fileToKeep.Name
        Remove-Item -Path $filePath -Force
    }
}

