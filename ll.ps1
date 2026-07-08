# Self-bootstrapping launcher: creates .venv on first run, then executes ll.py.
$ErrorActionPreference = 'Stop'

$repo = $PSScriptRoot
$venv = Join-Path $repo '.venv'
$venvPython = if ($IsWindows -or $env:OS -eq 'Windows_NT') {
    Join-Path $venv 'Scripts\python.exe'
} else {
    Join-Path $venv 'bin/python'
}

if (-not (Test-Path $venvPython)) {
    $basePython = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'python3' }
    & $basePython -m venv $venv
    & $venvPython -m pip install --quiet --disable-pip-version-check -r (Join-Path $repo 'requirements.txt')
}

& $venvPython (Join-Path $repo 'll.py') @args
exit $LASTEXITCODE
