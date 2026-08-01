# Mozhi — Windows installer (PowerShell)
#
# Usage (in PowerShell or Windows Terminal):
#   irm https://github.com/crossberry-in/mozhi-doc/raw/main/install.ps1 | iex
#
# Or download and run:
#   iwr -OutFile install.ps1 https://github.com/crossberry-in/mozhi-doc/raw/main/install.ps1
#   .\install.ps1
#
# This script:
#   1. Detects the architecture (x86_64 only on Windows)
#   2. Downloads the latest mozhi-windows-x86_64.exe binary
#   3. Installs it to $env:USERPROFILE\.mozhi\bin\mozhi-interpreter.exe
#      (Named 'mozhi-interpreter' to avoid conflict with the mozhi-pkg dispatcher)
#   4. Adds $env:USERPROFILE\.mozhi\bin to the user PATH
#   5. Verifies the installation
#

$ErrorActionPreference = "Stop"

$Repo = "crossberry-in/mozhi-doc"
$InstallDir = "$env:USERPROFILE\.mozhi\bin"
$BinaryName = "mozhi-interpreter.exe"
$AssetName = "mozhi-windows-x86_64.exe"

function Write-Info    { param([string]$Msg) Write-Host "[info]  $Msg" -ForegroundColor Cyan }
function Write-OK      { param([string]$Msg) Write-Host "[ok]    $Msg" -ForegroundColor Green }
function Write-Warn    { param([string]$Msg) Write-Host "[warn]  $Msg" -ForegroundColor Yellow }
function Write-Err     { param([string]$Msg) Write-Host "[error] $Msg" -ForegroundColor Red }

Write-Host ""
Write-Host "  ===================================" -ForegroundColor Cyan
Write-Host "   Mozhi Language Installer (Windows)" -ForegroundColor Cyan
Write-Host "  ===================================" -ForegroundColor Cyan
Write-Host ""

# --- Detect architecture ------------------------------------------------

$arch = $env:PROCESSOR_ARCHITECTURE
if ($arch -eq "AMD64") { $arch = "x86_64" }
elseif ($arch -eq "ARM64") {
    Write-Err "ARM64 Windows is not yet supported by Mozhi. Please open an issue:"
    Write-Err "  https://github.com/crossberry-in/mozhi-doc/issues"
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
    $release = Invoke-RestMethod -Uri $ReleaseApiUrl -Headers @{ "User-Agent" = "mozhi-installer" }
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
# The interpreter doesn't support --version; run a tiny script instead
$TestScript = [System.IO.Path]::GetTempFileName() + ".si"
'echo "Mozhi interpreter OK"' | Set-Content -Path $TestScript
& $FinalPath $TestScript
Remove-Item $TestScript -ErrorAction SilentlyContinue
if ($LASTEXITCODE -eq 0) {
    Write-OK "Mozhi interpreter is installed and working!"
} else {
    Write-Warn "Mozhi interpreter was installed but verification failed."
}

Write-Host ""
Write-OK "Done! For docs, visit: https://github.com/crossberry-in/mozhi-doc"
Write-Host ""
Write-Info "The interpreter is installed as 'mozhi-interpreter'."
Write-Info "Install the mozhi-pkg dispatcher ('mozhi') from:"
Write-Info "  https://github.com/crossberry-in/mozhi-pkg"
Write-Host ""
Write-Info "Then use the unified 'mozhi' command:"
Write-Info "  mozhi                    # start REPL"
Write-Info "  mozhi my_script.si       # run a script"
Write-Info "  mozhi build              # build a project"
Write-Host ""
Write-Warn "Note: Open a NEW PowerShell window for PATH changes to take effect."
