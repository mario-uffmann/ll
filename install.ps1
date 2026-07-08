# Installs the ll function into the PowerShell profile and pre-creates the venv.
# Idempotent: running it again changes nothing.
$ErrorActionPreference = 'Stop'

$repo = $PSScriptRoot
$launcher = Join-Path $repo 'll.ps1'
$fn = "function ll { & '$launcher' @args }"

if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

if (Select-String -Path $PROFILE -Pattern 'll\.ps1' -Quiet) {
    Write-Output "ll function already present in $PROFILE"
} else {
    Add-Content -Path $PROFILE -Value "`n# ll (https://github.com/mario-uffmann/ll)`n$fn"
    Write-Output "ll function added to $PROFILE"
}

& $launcher $repo | Out-Null
Write-Output 'venv ready - open a new shell and run: ll'
