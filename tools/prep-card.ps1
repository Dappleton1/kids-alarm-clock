# Prepare a microSD card for the DFPlayer: FAT32, folder 01, tracks copied in order.
# Usage (PowerShell, card inserted, note its drive letter in Explorer first):
#   .\tools\prep-card.ps1 -Drive E        (-Yes skips the confirmation, for scripted runs)
# ERASES THE CARD. Double-check the letter.
param(
    [Parameter(Mandatory = $true)][ValidatePattern('^[D-Z]$')][string]$Drive,
    # sounds\dfplayer holds the re-encodes from tools/encode_tracks.py; raw downloads crackle on YX5200 clones.
    [string]$Source = (Join-Path $PSScriptRoot '..\sounds\dfplayer'),
    [switch]$Yes
)
$ErrorActionPreference = 'Stop'
$root = "$Drive`:\"
if (-not (Test-Path $root)) { throw "No drive $Drive" }
$vol = Get-Volume -DriveLetter $Drive
if ($vol.Size -gt 64GB) { throw "$Drive is $([math]::Round($vol.Size/1GB)) GB - that is not a microSD. Stopping." }
$tracks = Get-ChildItem "$Source\0*.mp3" | Sort-Object Name
if ($tracks.Count -lt 1) { throw "No 0NN.mp3 files in $Source" }

Write-Host "About to FORMAT $root ($([math]::Round($vol.Size/1GB)) GB, label '$($vol.FileSystemLabel)') as FAT32 and copy $($tracks.Count) tracks."
if (-not $Yes) {
    $ok = Read-Host "Type YES to continue"
    if ($ok -ne 'YES') { Write-Host 'Aborted.'; exit 1 }
}

Format-Volume -DriveLetter $Drive -FileSystem FAT32 -NewFileSystemLabel 'ALARM' -Confirm:$false | Out-Null
New-Item -ItemType Directory -Path "$root\01" | Out-Null
foreach ($t in $tracks) {
    Copy-Item $t.FullName "$root\01\$($t.Name)"     # one at a time, in order: DFPlayer indexes by copy order
    Write-Host "  $($t.Name)"
}
# TRACKS.md may sit next to the tracks or one level up.
$md = @("$Source\TRACKS.md", (Join-Path (Split-Path $Source -Parent) 'TRACKS.md')) | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($md) { Copy-Item $md "$root\TRACKS.md" }
Write-Host "Done. Eject $Drive before pulling the card."
