# install-companion.ps1 — Clone companion skill repos vào .claude/skills/ (Windows)
# Usage:
#   ./scripts/install-companion.ps1 -Target claudekit
#   ./scripts/install-companion.ps1 -Target all
#   ./scripts/install-companion.ps1 -Target xia -Global

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)]
  [ValidateSet('claudekit','xia','others','all')]
  [string]$Target,
  [switch]$Global
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path $PSScriptRoot -Parent

# EDIT these URLs when companion repos are pushed to GitHub
$RepoUrls = @{
  'claudekit' = 'https://github.com/cuongbx/skills-claudekit.git'
  'xia'       = 'https://github.com/cuongbx/skills-xia.git'
  'others'    = 'https://github.com/cuongbx/skills-others.git'
}

$Targets = if ($Target -eq 'all') { @('claudekit', 'xia', 'others') } else { @($Target) }
$BaseDir = if ($Global) { Join-Path $HOME '.claude/skills' } else { Join-Path $ProjectRoot '.claude/skills' }

if (-not (Test-Path $BaseDir)) { New-Item -ItemType Directory -Path $BaseDir -Force | Out-Null }

foreach ($t in $Targets) {
  $url = $RepoUrls[$t]
  $dest = Join-Path $BaseDir $t

  Write-Host ""
  Write-Host "=== Install: $t ===" -ForegroundColor Cyan
  Write-Host "  Repo: $url"
  Write-Host "  Dest: $dest"

  if (Test-Path $dest) {
    Write-Host "  EXISTS — pulling latest..."
    Push-Location $dest
    git pull --ff-only
    Pop-Location
  } else {
    git clone --depth 1 $url $dest
  }
  Write-Host "  OK" -ForegroundColor Green
}

Write-Host ""
Write-Host "Done. Scope: $(if ($Global) {'Global'} else {'Project'})" -ForegroundColor Green
