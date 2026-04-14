# sync-from-global.ps1 — Pull skills từ global → project zones (Windows PowerShell)
# Usage:
#   ./scripts/sync-from-global.ps1
#   ./scripts/sync-from-global.ps1 -Zone claudekit
#   ./scripts/sync-from-global.ps1 -DryRun

[CmdletBinding()]
param(
  [string]$Zone = "",
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$CkGlobal = Join-Path $HOME ".claude/skills"
$AgGlobal = Join-Path $HOME ".gemini/antigravity/skills"

function Sync-Zone {
  param([string]$Name, [string]$LocalPath, [string]$GlobalPath, [string[]]$Exclude)

  Write-Host ""
  Write-Host "=== Zone: $Name ==="
  Write-Host "  Source: $GlobalPath"
  Write-Host "  Dest:   $LocalPath"

  if (-not (Test-Path $GlobalPath)) {
    Write-Host "  SKIP: global path không tồn tại"
    return
  }

  if (-not (Test-Path $LocalPath)) { New-Item -ItemType Directory -Path $LocalPath -Force | Out-Null }

  $count = 0; $skipped = 0
  foreach ($skill in Get-ChildItem -Path $GlobalPath -Directory) {
    if ($Exclude -contains $skill.Name) {
      $skipped++; continue
    }
    if ($DryRun) {
      Write-Host "  [DRY] would copy $($skill.Name)"
    } else {
      Copy-Item -Recurse -Force $skill.FullName (Join-Path $LocalPath $skill.Name)
    }
    $count++
  }
  Write-Host "  -> Synced $count skills (excluded $skipped)"
}

Write-Host "=========================================="
Write-Host "Sync FROM GLOBAL -> PROJECT"
if ($DryRun) { Write-Host "[DRY-RUN MODE - no changes]" }
Write-Host "=========================================="

if (-not $Zone -or $Zone -eq "claudekit") {
  Sync-Zone -Name "claudekit" `
    -LocalPath (Join-Path $ProjectRoot ".claude/skills/claudekit") `
    -GlobalPath $CkGlobal `
    -Exclude @("vci-skill-cuongbx", "xia", "vci-cuongbx")
}

if (-not $Zone -or $Zone -eq "others") {
  Sync-Zone -Name "others" `
    -LocalPath (Join-Path $ProjectRoot ".claude/skills/others") `
    -GlobalPath $AgGlobal `
    -Exclude @("antigravity-awesome-skills", "skill-creator-ultra", "vci-skill-cuongbx")
}

if (-not $Zone -or $Zone -eq "vci" -or $Zone -eq "xia") {
  Write-Host ""
  Write-Host "Note: Bidirectional zones (vci, xia) không auto-overwrite local."
  Write-Host "Use 'sync-to-global.ps1' để push local changes lên global."
}

Write-Host ""
if (-not $DryRun) {
  $stamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
  Set-Content -Path (Join-Path $ProjectRoot "scripts/.last-sync.txt") -Value $stamp
  Write-Host "Sync state saved: scripts/.last-sync.txt ($stamp)"
}
