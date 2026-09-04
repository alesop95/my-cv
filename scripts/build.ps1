#requires -Version 5.1
<#
.SYNOPSIS
  Compila main.tex nelle tre lingue (EN/IT/ES), sovrascrivendo i tre PDF stabili versionati.
.DESCRIPTION
  Sostituisce la build a lingua singola (via latexmk) del 2026-07-06: da quando main.tex è
  parametrizzato per lingua (\CVlanguage), l'utente ha chiesto (2026-07-08) che ogni ricompilazione
  aggiorni sempre e comunque tutte e tre le lingue insieme, così che un commit non possa mai
  lasciarne una disallineata dalle altre.

  Produce cv-sopranzi-alessio-en.pdf, cv-sopranzi-alessio-it.pdf, cv-sopranzi-alessio-es.pdf nella
  radice del progetto: nomi stabili (nessuna data), pensati per essere versionati in git come link
  diretto e sempre aggiornato al CV in ciascuna lingua (estende ADR-004 alle tre lingue). Diverso
  da scripts/build-multilang.ps1, che produce invece istantanee DATATE in dated-builds/<lingua>/,
  un archivio storico locale non versionato (ADR-005): i due script coesistono per due scopi
  diversi, build.ps1 è quello da lanciare prima di ogni commit.

  Compila con pdflatex direttamente (due passaggi fissi), non con latexmk, per lo stesso motivo di
  build-multilang.ps1: l'argomento "-jobname" iniettato non è un vero nome di file e
  comprometterebbe l'analisi delle dipendenze di latexmk.
.PARAMETER Main
  File .tex principale. Default: main.tex nella radice del progetto.
.PARAMETER TexDir
  Cartella di TinyTeX (default: $env:APPDATA\TinyTeX).
.PARAMETER Clean
  Rimuove i PDF stabili e i loro ausiliari (aux/log/out/synctex.gz) dalla radice e termina.
.EXAMPLE
  pwsh scripts/build.ps1
#>
[CmdletBinding()]
param(
    [string]$Main,
    [string]$TexDir,
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
if (-not $Main)   { $Main   = Join-Path $ProjectRoot 'main.tex' }
if (-not $TexDir) { $TexDir = Join-Path $env:APPDATA 'TinyTeX' }

$languages = @('en', 'it', 'es')
$mainDir   = Split-Path -Parent $Main
$mainName  = [System.IO.Path]::GetFileNameWithoutExtension($Main)

if ($Clean) {
    foreach ($lang in $languages) {
        Get-ChildItem -Path $mainDir -Filter "cv-sopranzi-alessio-$lang.*" -File -ErrorAction SilentlyContinue |
            Remove-Item -Force
    }
    Write-Host "[build] Rimossi i PDF stabili e gli ausiliari nelle tre lingue."
    return
}

if (-not (Test-Path $Main)) { throw "[build] File non trovato: $Main" }

function Find-Bin {
    param([string]$Name, [string]$Root)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($rel in @("bin\windows\$Name.exe", "bin\windows\$Name", "bin\win32\$Name.exe", "bin\win32\$Name")) {
        $p = Join-Path $Root $rel
        if (Test-Path $p) { return $p }
    }
    return $null
}

$pdflatex = Find-Bin -Name 'pdflatex' -Root $TexDir
if (-not $pdflatex) { throw "[build] pdflatex non trovato. Esegui prima scripts/setup-tex.ps1." }

# I derivati di compilazione (.aux, .log, .out, .synctex.gz, .xmpi) vanno in build/ invece di
# ingombrare la radice: sono tredici file per tre lingue, tutti gia' ignorati da git, quindi il
# riordino non tocca nulla di versionato. I tre PDF vengono invece riportati in radice a
# compilazione finita, perche' ADR-004 e ADR-006 li vogliono la' per avere un URL stabile su
# GitHub: spostarli romperebbe ogni link salvato o condiviso.
$buildDir = Join-Path $mainDir 'build'
if (-not (Test-Path $buildDir)) { New-Item -ItemType Directory -Path $buildDir | Out-Null }

Push-Location $mainDir
try {
    foreach ($lang in $languages) {
        $jobname  = "cv-sopranzi-alessio-$lang"
        $texInput = "\providecommand\CVlanguage{$lang}\input{$mainName.tex}"
        Write-Host "[build] Compilo $mainName.tex in lingua '$lang' -> $jobname.pdf ..."
        for ($pass = 1; $pass -le 2; $pass++) {
            & $pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 -file-line-error "-output-directory=$buildDir" "-jobname=$jobname" $texInput | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "[build] Compilazione fallita (lingua $lang, passaggio $pass, exit $LASTEXITCODE). Vedi build/$jobname.log."
            }
        }
        $builtPdf = Join-Path $buildDir "$jobname.pdf"
        if (-not (Test-Path $builtPdf)) { throw "[build] PDF non prodotto per la lingua ${lang}: $builtPdf" }
        $producedPdf = Join-Path $mainDir "$jobname.pdf"
        Copy-Item -LiteralPath $builtPdf -Destination $producedPdf -Force
        Write-Host "[build] Fatto: $producedPdf"
    }
}
finally { Pop-Location }

Write-Host ""
Write-Host "[build] Tutte e tre le lingue aggiornate nella radice del progetto."
