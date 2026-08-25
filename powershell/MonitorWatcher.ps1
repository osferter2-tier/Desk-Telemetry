Write-Host "Desk Telemetry Monitor Watcher Started..." -ForegroundColor Green

$Global:LastMonitorCount = (Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorID).Count

Register-WmiEvent `
    -Class Win32_DeviceChangeEvent `
    -SourceIdentifier MonitorChange `
    -Action {

        Start-Sleep -Seconds 2

        $CurrentMonitorCount = (Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorID).Count

        if ($CurrentMonitorCount -ne $Global:LastMonitorCount) {

            $Global:LastMonitorCount = $CurrentMonitorCount

            Write-Host "$(Get-Date) - Monitor change detected" -ForegroundColor Yellow

            powershell.exe `
                -ExecutionPolicy Bypass `
                -File ""C:\DeskTelemetry\Send-Telemetry.ps1""
        }
    }

while ($true) {
    Wait-Event | Out-Null
}