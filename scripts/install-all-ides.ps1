# install-all-ides.ps1 — Cài skills sang nhiều IDE locations (Windows)
# Usage:
#   ./scripts/install-all-ides.ps1
#   ./scripts/install-all-ides.ps1 -Target claude-code -Global
#   ./scripts/install-all-ides.ps1 -Copy

[CmdletBinding()]
param(
  [string]$Target = "",
  [switch]$Global,
  [switch]$Copy,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path $PSScriptRoot -Parent

$IdePaths = @{
  "claude-code"    = ".claude/skills"
  "antigravity"    = ".gemini/skills"
  "cursor"         = ".cursor/skills"
  "kilo"           = ".kilo/skills"
  "codex"          = ".codex/skills"
  "opencode"       = ".opencode/skills"
  "windsurf"       = ".windsurf/skills"
  "cline"          = ".cline/skills"
  "github-copilot" = ".github/copilot/skills"
}

function Install-ToIde {
  param([string]$Ide, [string]$RelPath)

  $base = if ($Global) { $HOME } else { (Get-Location).Path }
  $destRoot = Join-Path $base $RelPath

  Write-Host ""
  Write-Host "=== Install to: $Ide ($destRoot) ==="
  if (-not (Test-Path $destRoot)) { New-Item -ItemType Directory -Path $destRoot -Force | Out-Null }

  foreach ($zone in @("vci", "claudekit", "xia", "others")) {
    $src = Join-Path $ProjectRoot ".claude/skills/$zone"
    if (-not (Test-Path $src)) {
      Write-Host "  SKIP zone $zone (not present)"
      continue
    }

    $dest = Join-Path $destRoot $zone
    if (Test-Path $dest) {
      if ($Force) { Remove-Item -Recurse -Force $dest } else {
        Write-Host "  SKIP: $dest exists (use -Force)"
        continue
      }
    }

    if ($Copy) {
      Copy-Item -Recurse $src $dest
      Write-Host "  COPY: $zone -> $dest"
    } else {
      # Junction (Windows symlink for directories, no admin needed)
      New-Item -ItemType Junction -Path $dest -Target $src | Out-Null
      Write-Host "  LINK: $zone -> $dest"
    }
  }
}

Write-Host "=========================================="
Write-Host "Install skills to IDE(s)"
Write-Host "  Scope: $(if ($Global) {'Global (~)'} else {'Project (cwd)'})"
Write-Host "  Method: $(if ($Copy) {'Copy'} else {'Symlink (junction)'})"
Write-Host "=========================================="

if (-not $Target -or $Target -eq "all") {
  foreach ($ide in $IdePaths.Keys) {
    Install-ToIde -Ide $ide -RelPath $IdePaths[$ide]
  }
} else {
  if (-not $IdePaths.ContainsKey($Target)) {
    Write-Error "Unknown IDE '$Target'. Valid: $($IdePaths.Keys -join ', ') all"
    exit 1
  }
  Install-ToIde -Ide $Target -RelPath $IdePaths[$Target]
}

Write-Host ""
Write-Host "=========================================="
Write-Host "Done."
