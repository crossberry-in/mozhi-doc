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
#   2. Downloads the mozhi-interpreter-windows-x86_64.exe asset
#      (tries the latest release first, falls back to v2.5.0 —
#      the newest release line with a Windows build)
#   3. Installs it as mozhi.exe (canonical, used by all docs) and
#      keeps a mozhi-interpreter.exe copy for compatibility
#   4. Adds $env:USERPROFILE\.mozhi\bin to the user PATH
#   5. Verifies the installation
#

$ErrorActionPreference = "Stop"

$Repo = "crossberry-in/mozhi-doc"
$InstallDir = "$env:USERPROFILE\.mozhi\bin"
$BinaryName = "mozhi.exe"
$CompatName = "mozhi-interpreter.exe"
$AssetName = "mozhi-interpreter-windows-x86_64.exe"
$FallbackVersion = "v2.5.0"

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

# --- Download binary (latest release first, pinned fallback) -------------

$TmpFile = [System.IO.Path]::GetTempFileName() + ".exe"
$Version = $release.tag_name
$DownloadUrl = "https://github.com/$Repo/releases/download/$Version/$AssetName"

Write-Info "Downloading $AssetName from $Version..."
$downloaded = $true
try {
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $TmpFile -UseBasicParsing
} catch {
    $downloaded = $false
}

if (-not $downloaded) {
    Write-Warn "$Version has no Windows build yet — falling back to $FallbackVersion."
    $Version = $FallbackVersion
    $DownloadUrl = "https://github.com/$Repo/releases/download/$Version/$AssetName"
    try {
        Invoke-WebRequest -Uri $DownloadUrl -OutFile $TmpFile -UseBasicParsing
    } catch {
        Write-Err "Download failed: $_"
        exit 1
    }
}

# --- Install ------------------------------------------------------------

Write-Info "Installing to $InstallDir..."
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}
$FinalPath = Join-Path $InstallDir $BinaryName
Move-Item -Path $TmpFile -Destination $FinalPath -Force
Copy-Item -Path $FinalPath -Destination (Join-Path $InstallDir $CompatName) -Force

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
$TestScript = [System.IO.Path]::GetTempFileName() + ".mz"
'echo "Mozhi interpreter OK"' | Set-Content -Path $TestScript
& $FinalPath $TestScript
Remove-Item $TestScript -ErrorAction SilentlyContinue
if ($LASTEXITCODE -eq 0) {
    Write-OK "Mozhi interpreter is installed and working!"
} else {
    Write-Warn "Mozhi interpreter was installed but verification failed."
}

Write-Host ""
Write-OK "Done! For docs, visit: https://crossberry-in.github.io/mozhi-doc/"
Write-Host ""
Write-Info "The interpreter is installed as 'mozhi' (also as 'mozhi-interpreter' for compatibility)."
Write-Host ""
Write-Info "Get started:"
Write-Info "  mozhi                    # start REPL"
Write-Info "  mozhi run my_script.mz   # run a script"
Write-Info "  mozhi new myapp          # scaffold a new project"
Write-Host ""
Write-Warn "Note: Open a NEW PowerShell window for PATH changes to take effect."
