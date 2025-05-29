Write-Host "Starting build process..."

# Make sure the script is running with correct environment
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found! Please ensure Python is installed."
    exit 1
}

# Setting encoding with UTF-8
$env:PYTHONUTF8 = 1
$env:PYTHONIOENCODING = "utf-8"

# Setting console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Write debug information
Write-Host "Current Output Encoding: $([Console]::OutputEncoding)"
Write-Host "Current Input Encoding: $([Console]::InputEncoding)"

# Build GUI version for Windows
Write-Host "Building GUI with Flet..."
$projectName = "INVAXION-Unlocker"
$productName = "INVAXION Unlocker"
$companyName = "GamerNoTitle"
$copyrightInfo = "Copyright (C) 2025 GamerNoTitle. Licensed under AGPL-3.0. See LICENSE for details."
$description = "INVAXION Unlocker is a tool for unlocking and managing game content in INVAXION games. It provides a user-friendly interface for gamers to access additional features and content."

# Build with flet build command
uv run flet build windows --project "$projectName" --product "$productName" --company "$companyName" --copyright "$copyrightInfo" --description "$description" --cleanup-app --cleanup-packages > flet_build.log 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "GUI build successful! Output in gui.build folder."
} else {
    Write-Error "GUI build failed! Check flet_build.log for details."
    Get-Content -Path flet_build.log -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "Build process completed."