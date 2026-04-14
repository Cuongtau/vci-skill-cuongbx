# install.ps1 — Sync 2-zone skill library sang IDE khác (Windows PowerShell)
# Usage:
#   ./install.ps1 -Target antigravity
#   ./install.ps1 -Target cursor -Global
#   ./install.ps1 -Target all -Copy        # dùng copy thay symlink
#
# Supported targets: claude-code, antigravity, cursor, kilo, codex, opencode,
#                    windsurf, cline, github-copilot, all

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('claude-code','antigravity','cursor','kilo','codex','opencode',
                 'windsurf','cline','github-copilot','all')]
    [string]$Target,

    [switch]$Global,   # install vào ~ (user home) thay vì project cwd
    [switch]$Copy,     # copy thay vì symlink (slower, disk-heavy)
    [switch]$Force     # xoá target nếu đã tồn tại
)

$ErrorActionPreference = 'Stop'
$SkillsRoot = $PSScriptRoot    # .claude/skills/
$ProjectRoot = Split-Path (Split-Path $SkillsRoot -Parent) -Parent

# Map target → skill folder path
$TargetPaths = @{
    'claude-code'    = '.claude/skills'
    'antigravity'    = '.gemini/skills'
    'cursor'         = '.cursor/skills'
    'kilo'           = '.kilo/skills'
    'codex'          = '.codex/skills'
    'opencode'       = '.opencode/skills'
    'windsurf'       = '.windsurf/skills'
    'cline'          = '.cline/skills'
    'github-copilot' = '.github/copilot/skills'
}

function Install-Zone {
    param([string]$TargetName, [string]$RelPath)

    $BaseDir = if ($Global) { $HOME } else { $ProjectRoot }
    $DestRoot = Join-Path $BaseDir $RelPath

    if (-not (Test-Path $DestRoot)) {
        New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null
    }

    foreach ($Zone in @('vci-cuongbx','claudekit')) {
        $SrcPath = Join-Path $SkillsRoot $Zone
        $DestPath = Join-Path $DestRoot $Zone

        if (Test-Path $DestPath) {
            if ($Force) { Remove-Item -Recurse -Force $DestPath }
            else { Write-Host "SKIP: $DestPath exists (use -Force)"; continue }
        }

        if ($Copy) {
            Copy-Item -Recurse $SrcPath $DestPath
            Write-Host "COPY: $Zone -> $DestPath"
        } else {
            # Junction works for directories on Windows without admin
            New-Item -ItemType Junction -Path $DestPath -Target $SrcPath | Out-Null
            Write-Host "LINK: $Zone -> $DestPath"
        }
    }
}

$Targets = if ($Target -eq 'all') { $TargetPaths.Keys } else { @($Target) }

foreach ($t in $Targets) {
    Write-Host ""
    Write-Host "=== Installing to: $t ===" -ForegroundColor Cyan
    Install-Zone -TargetName $t -RelPath $TargetPaths[$t]
}

Write-Host ""
Write-Host "Done. Scope: $(if($Global){'Global (user home)'}else{'Project (cwd)'})" -ForegroundColor Green
Write-Host "Method: $(if($Copy){'Copy'}else{'Symlink (junction)'})" -ForegroundColor Green
