#requires -Version 5.1
<#
.SYNOPSIS
  Verifica la raggiungibilità di tutti i link citati dal CV, per categoria.
.DESCRIPTION
  Generalizzazione di scripts/check-skill-links.ps1, che verificava 5 URL su 52 bersagli: 45 link
  del CV non avevano alcun controllo automatico. L'elenco dei link non viene ricavato da una
  regex propria ma dal JSON di tools/extract-cv-links.py, così esiste una sola definizione di
  cosa sia un link del CV, condivisa con l'inventario e con il grafo delle dipendenze.

  I redirect si seguono un salto alla volta, fino a -MaxHops, e la destinazione finale viene
  riportata. È il modo per sapere, senza aprire un browser, quali dei 10 redirect tinyurl puntano
  ancora a Google Drive: è esattamente il dato che serve per chiudere il tracciamento della
  migrazione dei due target di tesi (vedi .claude/context/external-links.md).

  Avvertenza sui tag del blog: uno stato 2xx dice che la topic page esiste, non che il suo
  contenuto sia pertinente all'interesse che la linka. La pertinenza si verifica sul sorgente del
  blog, non qui.

  Non fa parte della build (build.ps1 non lo invoca): si lancia a mano prima di una build
  definitiva, dopo una modifica ai siti satellite, o periodicamente.
.PARAMETER Category
  Una o più categorie fra contatti, skills, projects, blog, proton, gdrive, tinyurl, terzi.
  Il valore predefinito "all" verifica tutto.
.PARAMETER ShowFinalUrl
  Riporta la destinazione finale di ogni link, non solo di quelli che hanno seguito un redirect.
.PARAMETER TimeoutSec
  Timeout per singola richiesta. Predefinito 20.
.PARAMETER MaxHops
  Numero massimo di redirect da seguire per link. Predefinito 5.
.EXAMPLE
  powershell -NoProfile -File scripts/check-links.ps1
.EXAMPLE
  powershell -NoProfile -File scripts/check-links.ps1 -Category tinyurl -ShowFinalUrl
#>
[CmdletBinding()]
param(
    [string[]]$Category = @('all'),
    [switch]$ShowFinalUrl,
    [int]$TimeoutSec = 20,
    [int]$MaxHops = 5
)

$ErrorActionPreference = 'Stop'
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Windows PowerShell 5.1 negozia per default protocolli che molti server hanno dismesso: senza
# questa riga una parte dei link fallirebbe con un errore di connessione che somiglia a un link
# rotto e non lo è.
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
} catch {
    Write-Verbose "[check-links] Impossibile forzare TLS 1.2: $($_.Exception.Message)"
}

$KnownCategories = @('contatti', 'skills', 'projects', 'blog', 'proton', 'gdrive', 'tinyurl', 'terzi')
$Labels = @{
    contatti = 'Contatti e identità'
    skills   = 'skills-repo'
    projects = 'projects'
    blog     = 'blog'
    proton   = 'Proton Drive'
    gdrive   = 'Google Drive'
    tinyurl  = 'Redirect tinyurl'
    terzi    = 'Siti di terze parti'
}

# Invocato con -File, PowerShell passa "gdrive,proton" come una stringa sola e non la spezza:
# il binding su [string[]] vale solo per le chiamate dall'interno di una sessione. Si normalizza
# qui, così la forma documentata funziona in entrambi i modi.
$Category = $Category | ForEach-Object { $_ -split ',' } | Where-Object { $_ } | ForEach-Object { $_.Trim().ToLowerInvariant() }

$wanted = if ($Category -contains 'all') { $KnownCategories } else { $Category }
$unknown = $wanted | Where-Object { $KnownCategories -notcontains $_ }
if ($unknown) {
    throw "[check-links] Categoria non riconosciuta: $($unknown -join ', '). Ammesse: all, $($KnownCategories -join ', ')."
}

# L'elenco dei link arriva dalla proiezione tabellare dell'estrattore: categoria, lingua, URL.
$extractor = Join-Path $ProjectRoot 'tools/extract-cv-links.py'
if (-not (Test-Path $extractor)) {
    throw "[check-links] Estrattore non trovato: $extractor"
}
$rows = & python $extractor '--format' 'urls'
if ($LASTEXITCODE -ne 0) {
    throw "[check-links] L'estrattore ha restituito codice $LASTEXITCODE."
}

$targets = @()
foreach ($row in $rows) {
    if ([string]::IsNullOrWhiteSpace($row)) { continue }
    $parts = $row -split "`t"
    if ($parts.Count -lt 3) { continue }
    $targets += [pscustomobject]@{
        Category = $parts[0]
        Lang     = $parts[1]
        Url      = $parts[2]
    }
}

function Invoke-LinkProbe {
    param([string]$Url, [string]$Method)
    # Perché HttpWebRequest e non Invoke-WebRequest. Su Windows PowerShell 5.1 la combinazione
    # -MaximumRedirection 0 solleva una InvalidOperationException generica e non espone alcuna
    # risposta, quindi lo stato 3xx e l'header Location sono irrecuperabili: verificato su tutti e
    # dieci i redirect tinyurl, che risultavano non raggiungibili mentre funzionavano. HttpWebRequest
    # con AllowAutoRedirect disattivato restituisce invece la risposta 3xx come tale, ed è l'unico
    # modo su 5.1 di leggere la destinazione di un redirect senza seguirla.
    $response = $null
    try {
        $request = [System.Net.HttpWebRequest]::Create($Url)
        $request.Method = $Method.ToUpperInvariant()
        $request.AllowAutoRedirect = $false
        $request.Timeout = $TimeoutSec * 1000
        $request.UserAgent = 'my-cv-check-links'
        $response = $request.GetResponse()
        return [pscustomobject]@{
            Status   = [int]$response.StatusCode
            Location = $response.Headers['Location']
            Error    = $null
        }
    } catch [System.Net.WebException] {
        $response = $_.Exception.Response
        if ($response) {
            $location = $null
            try { $location = $response.Headers['Location'] } catch { $location = $null }
            return [pscustomobject]@{
                Status   = [int]$response.StatusCode
                Location = $location
                Error    = $null
            }
        }
        return [pscustomobject]@{ Status = 0; Location = $null; Error = $_.Exception.Message }
    } catch {
        return [pscustomobject]@{ Status = 0; Location = $null; Error = $_.Exception.Message }
    } finally {
        if ($response) { try { $response.Close() } catch { } }
    }
}

function Resolve-Link {
    param([string]$Url)
    $current = $Url
    $hops = 0
    while ($true) {
        $probe = Invoke-LinkProbe -Url $current -Method 'Head'
        # Un 405 o un 501 sono il rifiuto del metodo HEAD, non un link rotto: si riprova in GET.
        if ($probe.Status -eq 405 -or $probe.Status -eq 501) {
            $probe = Invoke-LinkProbe -Url $current -Method 'Get'
        }
        if ($probe.Error) {
            return [pscustomobject]@{ Ok = $false; Status = 0; Final = $current; Hops = $hops; Detail = $probe.Error }
        }
        $isRedirect = @(301, 302, 303, 307, 308) -contains $probe.Status
        if ($isRedirect -and $probe.Location -and $hops -lt $MaxHops) {
            try {
                $current = ([Uri]::new([Uri]$current, $probe.Location)).AbsoluteUri
            } catch {
                return [pscustomobject]@{ Ok = $false; Status = $probe.Status; Final = $current; Hops = $hops; Detail = "Location non risolvibile: $($probe.Location)" }
            }
            $hops++
            continue
        }
        if ($isRedirect) {
            $detail = if ($probe.Location) { "redirect non seguito oltre $MaxHops salti" } else { 'redirect senza header Location' }
            return [pscustomobject]@{ Ok = $false; Status = $probe.Status; Final = $current; Hops = $hops; Detail = $detail }
        }
        $ok = ($probe.Status -ge 200 -and $probe.Status -lt 300)
        return [pscustomobject]@{ Ok = $ok; Status = $probe.Status; Final = $current; Hops = $hops; Detail = $null }
    }
}

$selected = $targets | Where-Object { $wanted -contains $_.Category }
Write-Host "[check-links] $($selected.Count) URL da verificare, categorie: $($wanted -join ', ')"
Write-Host ''

$failed = @()
$warned = @()
$skipped = @()
$unverifiable = @()
foreach ($cat in $KnownCategories) {
    if ($wanted -notcontains $cat) { continue }
    $group = $selected | Where-Object { $_.Category -eq $cat }
    if (-not $group) { continue }
    Write-Host "$($Labels[$cat]) ($($group.Count))"
    foreach ($t in $group) {
        # mailto: e tel: non sono risorse HTTP: verificarle non ha significato, si dichiarano
        # saltate invece di essere contate come errori.
        if ($t.Url -match '^(mailto:|tel:)') {
            $skipped += $t
            Write-Host ("  SKIP        {0}" -f $t.Url)
            continue
        }
        $lang = if ($t.Lang -eq '-') { '' } else { "[$($t.Lang)] " }
        # I link Proton non sono verificabili con una richiesta HTTP, per due motivi cumulativi:
        # /urls/<id> appartiene a una single-page application che risponde 200 a qualunque
        # percorso (verificato con l'identificativo inventato ZZZZZZZZZZ), e la chiave di
        # decifratura dopo il # non viene mai inviata al server. Si controlla quindi la forma e si
        # dichiara che la verifica end-to-end e' manuale, invece di stampare un OK che non vale.
        if ($cat -eq 'proton') {
            $shaped = $t.Url -match '^https://drive\.proton\.me/urls/[A-Za-z0-9]{10}#\S{8,}$'
            if ($shaped) {
                $unverifiable += [pscustomobject]@{ Url = $t.Url; Category = $cat }
                $keyLen = ($t.Url -split '#')[-1].Length
                Write-Host ("  FORMA ok    {0}{1}  (chiave {2} car)" -f $lang, $t.Url, $keyLen)
            } else {
                $failed += [pscustomobject]@{ Url = $t.Url; Category = $cat; Status = 0; Detail = 'forma inattesa per un link condiviso Proton' }
                Write-Host ("  FORMA NO    {0}{1} (forma inattesa: atteso /urls/<10 caratteri>#<chiave>)" -f $lang, $t.Url)
            }
            continue
        }
        $r = Resolve-Link -Url $t.Url
        if ($r.Ok) {
            $suffix = ''
            if ($r.Hops -gt 0) { $suffix = " -> $($r.Final)" }
            elseif ($ShowFinalUrl) { $suffix = " -> $($r.Final)" }
            Write-Host ("  OK   {0,3}   {1}{2}{3}" -f $r.Status, $lang, $t.Url, $suffix)
        } else {
            $detail = if ($r.Detail) { " ($($r.Detail))" } else { '' }
            $record = [pscustomobject]@{ Url = $t.Url; Category = $cat; Status = $r.Status; Detail = $r.Detail }
            # Uno stato 0 è un fallimento a livello di rete, non una risposta del server: può
            # dipendere dal resolver locale e non dal link. Verificato concretamente il 2026-09-03
            # su intrawelt.com, che il DNS del router non risolveva mentre 8.8.8.8 e 1.1.1.1
            # restituivano regolarmente il suo indirizzo. Confondere le due classi produce
            # esattamente quel falso allarme, quindi si separano e si separano anche i codici di
            # uscita: 1 per un errore HTTP, 2 quando ci sono solo errori di rete.
            if ($r.Status -eq 0) {
                $warned += $record
                Write-Host ("  WARN   -   {0}{1}{2}" -f $lang, $t.Url, $detail)
            } else {
                $failed += $record
                Write-Host ("  FAIL {0,3}   {1}{2}{3}" -f $r.Status, $lang, $t.Url, $detail)
            }
        }
    }
    Write-Host ''
}

if ($skipped.Count -gt 0) {
    Write-Host "[check-links] $($skipped.Count) non-HTTP saltati (mailto/tel)."
}
if ($unverifiable.Count -gt 0) {
    Write-Host "[check-links] $($unverifiable.Count) link Proton con forma corretta ma NON verificabili via HTTP."
    Write-Host "[check-links] La chiave dopo il # non raggiunge mai il server e /urls/<id> risponde 200 a qualunque identificativo: l'unica verifica reale e aprire il link in una finestra privata."
}
if ($warned.Count -gt 0) {
    Write-Host "[check-links] $($warned.Count) su $($selected.Count) non raggiungibili a livello di rete:"
    $warned | ForEach-Object { Write-Host "  ? [$($_.Category)] $($_.Url)" }
    Write-Host "[check-links] Un errore di rete può dipendere dal resolver locale: prima di considerare rotto il link, riprovare la risoluzione con un DNS pubblico (nslookup <host> 8.8.8.8)."
}
if ($failed.Count -gt 0) {
    Write-Host "[check-links] $($failed.Count) su $($selected.Count) hanno risposto con un errore HTTP:"
    $failed | ForEach-Object { Write-Host "  - [$($_.Category)] $($_.Url) (status $($_.Status))" }
    exit 1
}
if ($warned.Count -gt 0) {
    exit 2
}
Write-Host "[check-links] Tutti i link verificati sono raggiungibili."
