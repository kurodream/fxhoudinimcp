[CmdletBinding()]
param(
    [switch]$ConfigureCodex,
    [string]$Python = "py",
    [string]$VenvPath = ""
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path $PSScriptRoot).Path
if ([string]::IsNullOrWhiteSpace($VenvPath)) {
    $VenvPath = Join-Path $repoRoot ".venv"
}
$venvPython = Join-Path $VenvPath "Scripts\python.exe"

if (-not (Get-Command $Python -ErrorAction SilentlyContinue)) {
    throw "Python launcher '$Python' was not found. Install Python 3.10+ and rerun with -Python <command>."
}

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host "Creating project-local virtual environment: $VenvPath"
    & $Python -m venv $VenvPath
}

Write-Host "Installing fxhoudinimcp from the current checkout"
& $venvPython -m pip install -e $repoRoot

if ($ConfigureCodex) {
    $codexDir = Join-Path $env:USERPROFILE ".codex"
    $codexConfig = Join-Path $codexDir "config.toml"
    New-Item -ItemType Directory -Force -Path $codexDir | Out-Null

    if (Test-Path -LiteralPath $codexConfig) {
        $configText = Get-Content -Raw -LiteralPath $codexConfig
        if ($configText -match '(?m)^\[mcp_servers\.fxhoudini\]\s*$') {
            throw "Codex already has an [mcp_servers.fxhoudini] entry. Update it manually or remove that block before rerunning."
        }
        Copy-Item -LiteralPath $codexConfig -Destination "$codexConfig.bak" -Force
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
    Add-Content -LiteralPath $codexConfig -Value $snippet -Encoding utf8NoBOM
    Write-Host "Configured Codex: $codexConfig"
}

Write-Host "Read-only server executable: $venvPython -m fxhoudinimcp.readonly"
if (-not $ConfigureCodex) {
    Write-Host "Run again with -ConfigureCodex to append the server to your user Codex config."
}

