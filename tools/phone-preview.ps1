param([ValidateSet('Start', 'Status', 'Stop')][string]$Action = 'Start')
$ErrorActionPreference = 'Stop'
$appRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$previewData = Join-Path $appRoot 'data\phone-preview'
$statePath = Join-Path $previewData 'process.json'
$previewPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$state = if (Test-Path -LiteralPath $statePath) { Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json } else { $null }
$running = if ($state) { Get-CimInstance Win32_Process -Filter "ProcessId=$([int]$state.pid)" } else { $null }
if ($running -and (-not $running.CommandLine.Contains($previewData) -or -not $running.CommandLine.Contains('server.py'))) {
    throw 'The saved process ID belongs to another program. No process was changed.'
}
if ($Action -eq 'Stop') {
    if ($running) { Stop-Process -Id $running.ProcessId }
    if (Test-Path -LiteralPath $statePath) { Remove-Item -LiteralPath $statePath }
    Write-Output 'Phone preview stopped. The laptop app and phone browser progress were kept.'
    exit
}
if ($Action -eq 'Status' -or $running) {
    if ($running) {
        $health = Invoke-RestMethod -Uri ($state.url + '/api/health') -TimeoutSec 5
        if ($health.app -ne 'stepstone') { throw 'The preview did not return Stepstone health.' }
        Write-Output "Phone preview: $($state.url) (process $($state.pid))"
    } else { Write-Output 'Phone preview is not running.' }
    exit
}
if (-not (Test-Path -LiteralPath $previewPython)) { throw 'The Python runtime was not found. The laptop app was not changed.' }
$network = Get-NetIPConfiguration | Where-Object { $_.InterfaceAlias -eq 'Wi-Fi' -and $_.IPv4DefaultGateway -and $_.IPv4Address } | Select-Object -First 1
if (-not $network) { throw 'Connect this laptop to Wi-Fi before starting the phone preview.' }
$address = [string]$network.IPv4Address[0].IPAddress
if ($address -notmatch '^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)') { throw 'This preview requires a private Wi-Fi address.' }
$port = 8091
$url = "http://${address}:$port"
if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) { throw "Port $port is already in use. No process was changed." }
New-Item -ItemType Directory -Path $previewData -Force | Out-Null
$previewArguments = @('-B', ('"' + (Join-Path $appRoot 'server.py') + '"'), '--host', $address, '--port', $port, '--allow-host', "${address}:$port", '--data', ('"' + $previewData + '"'))
$process = Start-Process -FilePath $previewPython -ArgumentList $previewArguments -WorkingDirectory $appRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $previewData 'server.log') -RedirectStandardError (Join-Path $previewData 'server-error.log')
try {
    $ready = $false
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        if ($process.HasExited) { throw 'The preview exited. Check data/phone-preview/server-error.log.' }
        try {
            $health = Invoke-RestMethod -Uri ($url + '/api/health') -TimeoutSec 1
            if ($health.app -eq 'stepstone') { $ready = $true; break }
        } catch { Start-Sleep -Milliseconds 200 }
    }
    if (-not $ready) { throw 'The preview did not become ready.' }
    $stateJson = @{pid=$process.Id;url=$url;started=[DateTime]::UtcNow.ToString('o');mode='Wi-Fi practice preview'} | ConvertTo-Json
    [System.IO.File]::WriteAllText($statePath,$stateJson,(New-Object System.Text.UTF8Encoding $false))
} catch {
    if (-not $process.HasExited) { Stop-Process -Id $process.Id }
    throw
}
Write-Output "Open $url in Chrome on your phone, on the same Wi-Fi. Keep this laptop awake."
Write-Output 'This is a browser-only practice preview. Account setup is unavailable on this address.'
Write-Output 'Stop with: powershell -NoProfile -File tools\phone-preview.ps1 -Action Stop'
