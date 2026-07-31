# Sino — Windows installer (PowerShell)
#
# Usage (in PowerShell or Windows Terminal):
#   irm https://github.com/crossberry-in/sino-lang-docs/raw/main/install.ps1 | iex
#
# Or download and run:
#   iwr -OutFile install.ps1 https://github.com/crossberry-in/sino-lang-docs/raw/main/install.ps1
#   .\install.ps1
#
# This script:
#   1. Detects the architecture (x86_64 only on Windows)
#   2. Downloads the latest sino-windows-x86_64.exe binary
#   3. Installs it to $env:USERPROFILE\.sino\bin\sino.exe
#   4. Adds $env:USERPROFILE\.sino\bin to the user PATH
#   5. Verifies the installation
#

$ErrorActionPreference = "Stop"

$Repo = "crossberry-in/sino-lang-docs"
$InstallDir = "$env:USERPROFILE\.sino\bin"
$BinaryName = "sino.exe"
$AssetName = "sino-windows-x86_64.exe"

function Write-Info    { param([string]$Msg) Write-Host "[info]  $Msg" -ForegroundColor Cyan }
function Write-OK      { param([string]$Msg) Write-Host "[ok]    $Msg" -ForegroundColor Green }
function Write-Warn    { param([string]$Msg) Write-Host "[warn]  $Msg" -ForegroundColor Yellow }
function Write-Err     { param([string]$Msg) Write-Host "[error] $Msg" -ForegroundColor Red }

Write-Host ""
Write-Host "  ===================================" -ForegroundColor Cyan
Write-Host "   Sino Language Installer (Windows)" -ForegroundColor Cyan
Write-Host "  ===================================" -ForegroundColor Cyan
Write-Host ""

# --- Detect architecture ------------------------------------------------

$arch = $env:PROCESSOR_ARCHITECTURE
if ($arch -eq "AMD64") { $arch = "x86_64" }
elseif ($arch -eq "ARM64") {
    Write-Err "ARM64 Windows is not yet supported by Sino. Please open an issue:"
    Write-Err "  https://github.com/crossberry-in/sino-lang-docs/issues"
    exit 1
}
else {
    Write-Err "Unsupported architecture: $arch"
    exit 1
}

Write-Info "Detected platform: windows-$arch"
Write-Info "Target asset:      $AssetName"

# --- Get the latest release version -------------------------------------

Write-Info "Fetching latest release version..."
$ReleaseApiUrl = "https://api.github.com/repos/$Repo/releases/latest"
try {
    $release = Invoke-RestMethod -Uri $ReleaseApiUrl -Headers @{ "User-Agent" = "sino-installer" }
} catch {
    Write-Err "Failed to fetch release info: $_"
    exit 1
}
$Version = $release.tag_name
Write-Info "Latest version:    $Version"

# --- Download binary ----------------------------------------------------

$DownloadUrl = "https://github.com/$Repo/releases/download/$Version/$AssetName"
$TmpFile = [System.IO.Path]::GetTempFileName() + ".exe"

Write-Info "Downloading $AssetName..."
try {
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $TmpFile -UseBasicParsing
} catch {
    Write-Err "Download failed: $_"
    exit 1
}

# --- Install ------------------------------------------------------------

Write-Info "Installing to $InstallDir..."
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}
$FinalPath = Join-Path $InstallDir $BinaryName
Move-Item -Path $TmpFile -Destination $FinalPath -Force

# --- Add to PATH --------------------------------------------------------

$PathEnv = [Environment]::GetEnvironmentVariable("Path", "User")
if ($PathEnv -notlike "*$InstallDir*") {
    Write-Info "Adding $InstallDir to user PATH..."
    [Environment]::SetEnvironmentVariable("Path", "$PathEnv;$InstallDir", "User")
    # Also update current session
    $env:Path = "$env:Path;$InstallDir"
} else {
    Write-Info "$InstallDir is already on the user PATH."
}

# --- Verify -------------------------------------------------------------

Write-Info "Verifying installation..."
& $FinalPath --version
if ($LASTEXITCODE -eq 0) {
    Write-OK "Sino is installed and working!"
} else {
    Write-Warn "Sino was installed but verification failed."
    Write-Warn "Open a new PowerShell window and run: sino --version"
}

Write-Host ""
Write-OK "Done! For docs, visit: https://github.com/crossberry-in/sino-lang-docs"
Write-Host ""
Write-Info "Run the REPL:        sino"
Write-Info "Run a script:        sino my_script.si"
Write-Host ""
Write-Warn "Note: Open a NEW PowerShell window for 'sino' to be on your PATH."
