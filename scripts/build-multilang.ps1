#requires -Version 5.1
<#
.SYNOPSIS
  Compila main.tex nelle tre lingue (EN/IT/ES) producendo tre PDF datati e nominati.
.DESCRIPTION
  Sezione "Fase 5" di .claude/context/roadmap.md: main.tex è parametrizzato per lingua tramite
  \CVlanguage (\providecommand, default "en") e la macro \cvtext{italiano}{spagnolo}{inglese}.
  Questo script compila il documento una volta per ciascuna lingua, iniettando
  "\providecommand\CVlanguage{<lingua>}\input{main.tex}" come argomento di pdflatex al posto del
  nome file: main.tex usa \providecommand (non \newcommand), quindi l'iniezione esterna vince
  senza errori di "comando già definito".

  Compila con pdflatex direttamente, non con latexmk: due passaggi fissi, sufficienti per questo
  documento (hyperref/pdfx richiedono un secondo passaggio per riferimenti e bookmark, osservato
  nelle build reali di questo progetto). Non usa latexmk perché l'argomento iniettato non è un
  vero nome di file: comprometterebbe l'analisi delle dipendenze di latexmk, comunque inutile per
  una singola build pulita come questa.

  I PDF prodotti si chiamano cv-sopranzi-alessio-<lingua>-<AAAA-MM-GG>.pdf, raccolti in
  sottocartelle separate per lingua sotto OutDir (OutDir/en/, OutDir/it/, OutDir/es/): a
  differenza di main.pdf (un solo file che si aggiorna, versionato per ADR-004), questi PDF
  datati si accumulano nel tempo, e le sottocartelle per lingua evitano che si mescolino tutti
  insieme nella stessa cartella dopo settimane di build (richiesta del 2026-07-07). Il nome del
  file mantiene comunque la lingua, così resta riconoscibile anche se estratto dalla cartella
  (es. condiviso via email). Senza componente oraria nel nome, rilanciare lo script più volte lo
  stesso giorno sovrascrive semplicemente il file di quel giorno, mentre le date diverse restano
  distinte come istantanee storiche.
.PARAMETER Main
  File .tex principale. Default: main.tex nella radice del progetto.
.PARAMETER OutDir
  Cartella base sotto cui creare le sottocartelle per lingua (OutDir/en, OutDir/it, OutDir/es).
  Default: dated-builds/ nella radice del progetto (cartella dedicata e gitignored, ADR-005 in
  .claude/memory/decisions.md; main.pdf resta invece nella radice, versionato per ADR-004).
.PARAMETER TexDir
  Cartella di TinyTeX (default: $env:APPDATA\TinyTeX).
.EXAMPLE
  pwsh scripts/build-multilang.ps1
#>
[CmdletBinding()]
param(
    [string]$Main,
    [string]$OutDir,
    [string]$TexDir
)

$ErrorActionPreference = 'Stop'
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
if (-not $Main)   { $Main   = Join-Path $ProjectRoot 'main.tex' }
if (-not $OutDir) { $OutDir = Join-Path $ProjectRoot 'dated-builds' }
if (-not $TexDir) { $TexDir = Join-Path $env:APPDATA 'TinyTeX' }

if (-not (Test-Path $Main)) { throw "[build-multilang] File non trovato: $Main" }

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
if (-not $pdflatex) { throw "[build-multilang] pdflatex non trovato. Esegui prima scripts/setup-tex.ps1." }

$date      = Get-Date -Format 'yyyy-MM-dd'
$languages = @('en', 'it', 'es')
$mainDir   = Split-Path -Parent $Main
$mainName  = [System.IO.Path]::GetFileNameWithoutExtension($Main)

Push-Location $mainDir
try {
    foreach ($lang in $languages) {
        $jobname  = "cv-sopranzi-alessio-$lang-$date"
        $texInput = "\providecommand\CVlanguage{$lang}\input{$mainName.tex}"
        $langDir  = Join-Path $OutDir $lang
        New-Item -ItemType Directory -Force -Path $langDir | Out-Null
        Write-Host "[build-multilang] Compilo $mainName.tex in lingua '$lang' -> $lang/$jobname.pdf ..."
        for ($pass = 1; $pass -le 2; $pass++) {
            & $pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 -file-line-error "-jobname=$jobname" $texInput | Out-Null
            if ($LASTEXITCODE -ne 0) {
                throw "[build-multilang] Compilazione fallita (lingua $lang, passaggio $pass, exit $LASTEXITCODE). Vedi $jobname.log."
            }
        }
        $producedPdf = Join-Path $mainDir "$jobname.pdf"
        if (-not (Test-Path $producedPdf)) { throw "[build-multilang] PDF non prodotto per la lingua ${lang}: $producedPdf" }
        # Sposta TUTTI i file prodotti da questo jobname (pdf, aux, log, out, synctex.gz), non
        # solo il pdf: pdflatex li scrive sempre in $mainDir (la radice del progetto) perché è
        # la cartella corrente al momento della compilazione, e senza questo spostamento
        # restavano lì a sporcare la root a ogni build (richiesta del 2026-07-08).
        Get-ChildItem -Path $mainDir -Filter "$jobname.*" -File | ForEach-Object {
            Move-Item -Force $_.FullName (Join-Path $langDir $_.Name)
        }
        $destPdf = Join-Path $langDir "$jobname.pdf"
        Write-Host "[build-multilang] Fatto: $destPdf"
    }
} finally { Pop-Location }

Write-Host ""
Write-Host "[build-multilang] Tutte le lingue compilate in $OutDir."
