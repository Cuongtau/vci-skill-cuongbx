# restore-claudekit.ps1 — Restore full claudekit zone (179 skills, ~325MB) from global
# Usage: ./restore-claudekit.ps1
#
# Copy toàn bộ ~/.claude/skills/* vào .claude/skills/claudekit/
# Dùng khi: (a) clone repo mới, (b) reset claudekit zone, (c) update từ global
#
# Prerequisite: ~/.claude/skills/ phải có sẵn (cài qua `ck skills` hoặc `npm install -g claudekit-cli`)

$ErrorActionPreference = 'Stop'

$ScriptDir = $PSScriptRoot
$Src = Join-Path $HOME '.claude/skills'
$Dst = Join-Path $ScriptDir 'claudekit'

if (-not (Test-Path $Src)) {
    Write-Error "Source $Src not found. Install ClaudeKit first:`n  npm install -g claudekit-cli`n  ck skills --list   # populate ~/.claude/skills/"
    exit 1
}

New-Item -ItemType Directory -Path $Dst -Force | Out-Null
Write-Host "Source: $Src"
Write-Host "Dest:   $Dst"
Write-Host ""
Write-Host "Copying ~179 skills (~325MB)..."
$start = Get-Date

$count = 0
foreach ($skill in Get-ChildItem -Path $Src -Directory) {
    $destPath = Join-Path $Dst $skill.Name
    if (-not (Test-Path $destPath)) {
        Copy-Item -Recurse $skill.FullName $destPath
        $count++
    }
}

$elapsed = (Get-Date) - $start
Write-Host ""
Write-Host "Done. Copied $count new skills in $([int]$elapsed.TotalSeconds)s" -ForegroundColor Green
Write-Host "Total in claudekit/: $((Get-ChildItem $Dst).Count) items"
