#requires -Version 5.1
<#
.SYNOPSIS
  Verifica che i link a skills-repo citati nel .tex principale siano ancora raggiungibili.
.DESCRIPTION
  Sezione "Fase 4" di .claude/context/roadmap.md: la tassonomia di skills-repo
  (alesop95.github.io/skills/) non e' congelata, le pagine Capability possono essere
  rinominate, spostate o rimosse. Questo script estrae ogni URL
  https://alesop95.github.io/skills/... citato nel file .tex e verifica con una richiesta
  HTTP HEAD che risponda 2xx. Da eseguire prima di ogni build definitiva del CV, o
  periodicamente, non fa parte della build stessa.
.PARAMETER Main
  File .tex da analizzare. Se omesso e nella radice c'e' un solo .tex, usa quello.
.EXAMPLE
  pwsh scripts/check-skill-links.ps1
#>
[CmdletBinding()]
param(
    [string]$Main
)

$ErrorActionPreference = 'Stop'
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

if (-not $Main) {
    $texFiles = Get-ChildItem -Path $ProjectRoot -Filter '*.tex' -File
    if ($texFiles.Count -eq 1) { $Main = $texFiles[0].FullName }
    elseif ($texFiles.Count -eq 0) { throw "[check-skill-links] Nessun .tex nella radice: specifica -Main." }
    else { throw "[check-skill-links] Piu' .tex nella radice: specifica -Main <file.tex>." }
} elseif (-not (Test-Path $Main)) {
    $Main = Join-Path $ProjectRoot $Main
}

$content = Get-Content -Raw -LiteralPath $Main
$pattern = 'https://alesop95\.github\.io/skills/[A-Za-z0-9\-/]+/'
$urls = [regex]::Matches($content, $pattern) | ForEach-Object { $_.Value } | Sort-Object -Unique

if ($urls.Count -eq 0) {
    Write-Host "[check-skill-links] Nessun link a skills-repo trovato in $Main."
    exit 0
}

Write-Host "[check-skill-links] Verifico $($urls.Count) link a skills-repo citati in $Main ..."
$broken = @()
foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing -TimeoutSec 15
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300) {
            Write-Host "  OK    $url"
        } else {
            Write-Host "  WARN  $url (status $($response.StatusCode))"
            $broken += $url
        }
    } catch {
        Write-Host "  FAIL  $url ($($_.Exception.Message))"
        $broken += $url
    }
}

Write-Host ""
if ($broken.Count -gt 0) {
    Write-Host "[check-skill-links] $($broken.Count) di $($urls.Count) link non raggiungibili:"
    $broken | ForEach-Object { Write-Host "  - $_" }
    exit 1
}

Write-Host "[check-skill-links] Tutti i $($urls.Count) link sono raggiungibili."
