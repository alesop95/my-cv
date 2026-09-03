#requires -Version 5.1
<#
.SYNOPSIS
  Involucro storico: verifica i soli link a skills-repo invocando scripts/check-links.ps1.
.DESCRIPTION
  Fino al 2026-09-03 questo script conteneva una propria estrazione a regex dei soli URL
  https://alesop95.github.io/skills/... citati nel .tex, e verificava 5 link su 52 bersagli del
  CV. Quella logica è stata generalizzata in scripts/check-links.ps1, che prende l'elenco dei
  link dal JSON di tools/extract-cv-links.py e copre tutte le categorie.

  Il nome resta perché è citato per nome in .claude/context/deployment.md, nella Fase 4 di
  .claude/context/roadmap.md e nel registro delle decisioni: un rinvio esplicito costa meno di
  una caccia ai riferimenti, e mantiene valida la documentazione storica.

  Per verificare tutto il CV, non solo skills-repo, usare direttamente:
    powershell -NoProfile -File scripts/check-links.ps1
.PARAMETER Main
  Accettato e ignorato: l'elenco dei link non viene più ricavato da un file .tex passato a mano
  ma dall'estrattore, che conosce main.tex, altacv.cls e i template delle macro di collegamento.
.EXAMPLE
  powershell -NoProfile -File scripts/check-skill-links.ps1
#>
[CmdletBinding()]
param(
    [string]$Main
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Main) {
    Write-Host "[check-skill-links] Il parametro -Main non ha più effetto: l'elenco dei link arriva da tools/extract-cv-links.py."
}

Write-Host "[check-skill-links] Involucro su check-links.ps1 -Category skills."
& (Join-Path $ScriptDir 'check-links.ps1') -Category 'skills'
exit $LASTEXITCODE
