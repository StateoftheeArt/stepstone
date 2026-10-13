param(
    [string]$DestinationDirectory = [Environment]::GetFolderPath('Desktop')
)
$ErrorActionPreference = 'Stop'
$appDirectory = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$launchPath = Join-Path $appDirectory 'launch.ps1'
$iconPath = Join-Path $appDirectory 'public\icons\stepstone.ico'
$powershellPath = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
foreach ($requiredPath in @($launchPath, $iconPath, $powershellPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Missing launcher file: $requiredPath"
    }
}
if (-not (Test-Path -LiteralPath $DestinationDirectory -PathType Container)) {
    throw "The desktop folder was not found: $DestinationDirectory"
}
$desktopDirectory = (Resolve-Path -LiteralPath $DestinationDirectory).Path
$shortcutPath = Join-Path $desktopDirectory 'Stepstone.lnk'
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $powershellPath
$shortcut.Arguments = '-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + $launchPath + '"'
$shortcut.WorkingDirectory = $appDirectory
$shortcut.IconLocation = "$iconPath,0"
$shortcut.WindowStyle = 7
$shortcut.Description = 'Open Stepstone - learning, practical skills, and your next step.'
$shortcut.Save()
if (-not (Test-Path -LiteralPath $shortcutPath -PathType Leaf)) {
    throw 'Windows did not save the Stepstone shortcut.'
}
Write-Output "Created $shortcutPath"
Write-Output "Icon: $iconPath"
