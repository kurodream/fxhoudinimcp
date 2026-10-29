[CmdletBinding()]
param(
    [switch]$ConfigureCodex,
    [string]$Python = "",
    [string]$VenvPath = ""
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path $PSScriptRoot).Path
if ([string]::IsNullOrWhiteSpace($VenvPath)) {
    $VenvPath = Join-Path $repoRoot ".venv"
}
$venvPython = Join-Path $VenvPath "Scripts\python.exe"

if ([string]::IsNullOrWhiteSpace($Python)) {
    $Python = @("py", "python", "python.exe") |
        Where-Object { Get-Command $_ -ErrorAction SilentlyContinue } |
        Select-Object -First 1
}
if ([string]::IsNullOrWhiteSpace($Python) -or -not (Get-Command $Python -ErrorAction SilentlyContinue)) {
    throw "No Python launcher was found. Install Python 3.10+ or rerun with -Python D:\App\Python312\python.exe."
}

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host "Creating project-local virtual environment: $VenvPath"
    & $Python -m venv $VenvPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $venvPython)) {
        throw "Could not create the project virtual environment. Run this script from a normal PowerShell outside Codex, then retry."
    }
}

& $venvPython -m pip --version *> $null
if ($LASTEXITCODE -ne 0) {
    throw "The project virtual environment exists but pip is unavailable: $VenvPath. Remove that incomplete .venv and rerun from a normal PowerShell outside Codex."
}

Write-Host "Installing fxhoudinimcp from the current checkout"
& $venvPython -m pip install -e $repoRoot
if ($LASTEXITCODE -ne 0) {
    throw "Installing fxhoudinimcp failed. Check the pip output above and rerun from a normal PowerShell."
}

if ($ConfigureCodex) {
    $codexDir = Join-Path $env:USERPROFILE ".codex"
    $codexConfig = Join-Path $codexDir "config.toml"
    New-Item -ItemType Directory -Force -Path $codexDir | Out-Null

    if (Test-Path -LiteralPath $codexConfig) {
        $configText = Get-Content -Raw -LiteralPath $codexConfig
        if ($configText -match '(?m)^\[mcp_servers\.fxhoudini\]\s*$') {
            throw "Codex already has an [mcp_servers.fxhoudini] entry. Update it manually or remove that block before rerunning."
        }
        $backupPath = "$codexConfig.bak"
        if (Test-Path -LiteralPath $backupPath) {
            $backupPath = "$codexConfig.bak.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        }
        try {
            Copy-Item -LiteralPath $codexConfig -Destination $backupPath
        }
        catch {
            throw "Could not back up $codexConfig. Fully exit Codex, then rerun this script from a normal PowerShell."
        }
        Write-Host "Backed up Codex config: $backupPath"
    }

    $tomlRoot = $repoRoot.Replace('\', '\\')
    $tomlPython = $venvPython.Replace('\', '\\')
    $snippet = @"

# Added by fxhoudinimcp/setup-readonly-mcp.ps1
[mcp_servers.fxhoudini]
command = "$tomlPython"
args = ["-m", "fxhoudinimcp.readonly"]
cwd = "$tomlRoot"
"@
    # Windows PowerShell 5.1 supports UTF8, but not the PowerShell 7
    # utf8NoBOM enum value. A UTF-8 BOM is valid for Codex's TOML config.
    Add-Content -LiteralPath $codexConfig -Value $snippet -Encoding UTF8
    Write-Host "Configured Codex: $codexConfig"
}

Write-Host "Read-only server executable: $venvPython -m fxhoudinimcp.readonly"
if (-not $ConfigureCodex) {
    Write-Host "Run again with -ConfigureCodex to append the server to your user Codex config."
}

