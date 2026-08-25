# ==========================================
# Desk Telemetry Agent v0.1
# ==========================================

function Convert-EdidString {
    param(
        [array]$Value
    )

    if ($null -eq $Value) {
        return ""
    }

    return (($Value | Where-Object { $_ -ne 0 }) | ForEach-Object { [char]$_ }) -join ""
}

# ==========================================
# Configuration
# ==========================================

$ApiUrl = "https://sxac70zh3f.execute-api.us-east-1.amazonaws.com/api/v1/telemetry"

$LogFolder = "C:\DeskTelemetry\Logs"
$LogFile   = Join-Path $LogFolder "telemetry.log"

if (!(Test-Path $LogFolder)) {
    New-Item -ItemType Directory -Path $LogFolder -Force | Out-Null
}

# ==========================================
# Main
# ==========================================

try {

    $Hostname = $env:COMPUTERNAME

    # Obtener todos los monitores
    $Monitors = Get-CimInstance `
        -Namespace root\wmi `
        -ClassName WmiMonitorID `
        -ErrorAction Stop

    $MonitorObjects = foreach ($M in $Monitors) {

        $Manufacturer = Convert-EdidString $M.ManufacturerName
        $Model        = Convert-EdidString $M.UserFriendlyName
        $Serial       = Convert-EdidString $M.SerialNumberID

        [PSCustomObject]@{
            Manufacturer = $Manufacturer
            Model        = $Model
            Serial       = $Serial
            MonitorID    = "$Manufacturer-$Model-$Serial"
        }
    }

    # Buscar monitor externo válido
    $SelectedMonitor = $MonitorObjects |
        Where-Object {
            $_.Serial -ne "" -and
            $_.Serial -ne "0"
        } |
        Select-Object -Last 1

    if (-not $SelectedMonitor) {

        Write-Host ""
        Write-Host "No external monitor detected." -ForegroundColor Yellow

        $MonitorID = "NO_MONITOR"
    }
    else {

        $MonitorID = $SelectedMonitor.MonitorID

        Write-Host ""
        Write-Host "Selected Monitor:" -ForegroundColor Yellow
        Write-Host $MonitorID -ForegroundColor Cyan
    }

    $Timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

    $Payload = @{
        hostname      = $Hostname
        monitor_id    = $MonitorID
        timestamp     = $Timestamp
        agent_version = "0.1"
    }

    $Json = $Payload | ConvertTo-Json -Compress

    Write-Host ""
    Write-Host "Sending telemetry..." -ForegroundColor Cyan
    Write-Host $Json

    $Response = Invoke-RestMethod `
        -Uri $ApiUrl `
        -Method POST `
        -Body $Json `
        -ContentType "application/json" `
        -ErrorAction Stop

    Write-Host ""
    Write-Host "Telemetry sent successfully" -ForegroundColor Green
    Write-Host "Desk:   $($Response.desk_code)"
    Write-Host "Status: $($Response.status)"

    Add-Content `
        -Path $LogFile `
        -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | SUCCESS | $Hostname | $MonitorID | $($Response.desk_code) | $($Response.status)"

}
catch {

    $ErrorMessage = $_.Exception.Message

    Write-Host ""
    Write-Host "Telemetry failed" -ForegroundColor Red
    Write-Host $ErrorMessage

    Add-Content `
        -Path $LogFile `
        -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | ERROR | $ErrorMessage"
}