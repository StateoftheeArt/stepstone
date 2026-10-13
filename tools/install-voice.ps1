param([string]$PythonExecutable = 'python')
$ErrorActionPreference = 'Stop'
$voiceRoot = Join-Path $env:LOCALAPPDATA 'Stepstone\voice'
$basePython = (Get-Command $PythonExecutable -ErrorAction Stop).Source
$voicePython = Join-Path $voiceRoot 'runtime\Scripts\python.exe'
New-Item -ItemType Directory -Force -Path $voiceRoot | Out-Null
if (-not (Test-Path -LiteralPath $voicePython)) {
    & $basePython -m venv (Join-Path $voiceRoot 'runtime')
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the isolated voice runtime.' }
}
& $voicePython -m pip install --disable-pip-version-check 'kokoro-onnx==0.6.1'
if ($LASTEXITCODE -ne 0) { throw 'Voice package installation did not finish.' }
$models = @(
    @{name='kokoro-v1.0.onnx';hash='beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a'},
    @{name='voices-v1.0.bin';hash='bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d'}
)
foreach ($model in $models) {
    $destination = Join-Path $voiceRoot $model.name
    if ((Test-Path -LiteralPath $destination) -and ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -eq $model.hash)) { continue }
    $partial = $destination + '.download'
    Invoke-WebRequest -UseBasicParsing -Uri ('https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/' + $model.name) -OutFile $partial
    if ((Get-FileHash -LiteralPath $partial -Algorithm SHA256).Hash -ne $model.hash) { throw ('Voice checksum mismatch: ' + $model.name) }
    Move-Item -LiteralPath $partial -Destination $destination -Force
}
$physicalHome = & $voicePython -c 'import pathlib,sys; print(pathlib.Path(sys.executable).resolve().parents[2])'
$appRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
New-Item -ItemType Directory -Force -Path (Join-Path $appRoot 'data') | Out-Null
$configJson = @{home=$physicalHome;voice='af_heart';package='kokoro-onnx==0.6.1';modelRelease='model-files-v1.1';model='kokoro-v1.0.onnx';modelSha256='beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a'} | ConvertTo-Json
[System.IO.File]::WriteAllText((Join-Path $appRoot 'data\voice-runtime.json'),$configJson,(New-Object System.Text.UTF8Encoding $false))
Write-Output "Installed the local Kokoro Heart voice in $physicalHome."
