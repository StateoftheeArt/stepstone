$ErrorActionPreference = 'Stop'
$appDirectory = $PSScriptRoot
$port = 8090
$healthUrl = "http://127.0.0.1:$port/api/health"
try {
    # Keep the browser on localhost (saved sessions), but avoid slow IPv6
    # fallback in Windows PowerShell when checking the IPv4-only local server.
    $health = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 5
    if ($health.app -eq 'stepstone') { Start-Process "http://localhost:$port"; exit 0 }
} catch {}
if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
    throw "Port $port is in use by another app. Close that app or run server.py with a different --port."
}
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
$launcherCommand = Get-Command py.exe -ErrorAction SilentlyContinue
if (Test-Path -LiteralPath $bundledPython) { $pythonPath = $bundledPython; $arguments = @('-B','server.py','--desktop','--port',"$port") }
elseif ($launcherCommand) { $pythonPath = $launcherCommand.Source; $arguments = @('-3','-B','server.py','--desktop','--port',"$port") }
elseif ($pythonCommand) { $pythonPath = $pythonCommand.Source; $arguments = @('-B','server.py','--desktop','--port',"$port") }
else { throw 'Install Python 3.10 or newer to start the local Stepstone pilot.' }
$logDirectory = Join-Path $env:LOCALAPPDATA 'Stepstone\logs'
New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null
$process = Start-Process -FilePath $pythonPath -ArgumentList $arguments -WorkingDirectory $appDirectory -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logDirectory 'server.log') -RedirectStandardError (Join-Path $logDirectory 'server-error.log') -PassThru
for ($attempt = 0; $attempt -lt 40; $attempt++) {
    Start-Sleep -Milliseconds 250
    try {
        $health = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 2
        if ($health.app -eq 'stepstone') { Start-Process "http://localhost:$port"; exit 0 }
    } catch {}
    if ($process.HasExited) { throw "Stepstone did not start. See $logDirectory\server-error.log" }
}
throw "Stepstone did not become ready. See $logDirectory\server-error.log"

