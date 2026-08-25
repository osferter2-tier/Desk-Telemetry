while($true){

    Clear-Host

    Write-Host ""
    Write-Host "DESK TELEMETRY DASHBOARD" -ForegroundColor Cyan
    Write-Host "$(Get-Date)"
    Write-Host ""

    $data = Invoke-RestMethod `
    -Uri "https://sxac70zh3f.execute-api.us-east-1.amazonaws.com/api/v1/status"

    foreach($desk in $data){

        switch($desk.status){

            "OK" {
                $color = "Green"
            }

            "UNASSIGNED_DEVICE" {
                $color = "Red"
            }

            "NO_REPORT" {
                $color = "Yellow"
            }

            "NO_MONITOR" {
                $color = "Magenta"
            }

            default {
                $color = "White"
            }
        }

        Write-Host (
            "{0,-10} {1,-25} {2,-20} {3,-20}" -f
            $desk.desk_code,
            $desk.employee_name,
            $desk.current_hostname,
            $desk.status
        ) -ForegroundColor $color
    }

    Start-Sleep 15
}