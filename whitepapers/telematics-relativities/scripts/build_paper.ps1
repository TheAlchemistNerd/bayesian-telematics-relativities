param(
    [string]$SourcePath = "paper.md",
    [string]$OutputPath = "paper.docx",
    [string]$PythonPath = "python"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$source = [System.IO.Path]::GetFullPath((Join-Path $root $SourcePath))
$output = [System.IO.Path]::GetFullPath((Join-Path $root $OutputPath))
$build = Join-Path $root "build"
$assets = Join-Path $root "assets"

New-Item -ItemType Directory -Force -Path $build, $assets | Out-Null

$text = Get-Content -Raw -LiteralPath $source
$pattern = '(?ms)^```mermaid\s*\r?\n(.*?)\r?\n```'
$matches = [regex]::Matches($text, $pattern)
if ($matches.Count -ne 7) {
    throw "Expected seven Mermaid figures, found $($matches.Count)."
}

$rendered = $text
for ($index = $matches.Count - 1; $index -ge 0; $index--) {
    $number = $index + 1
    $sourceFigure = Join-Path $assets ("figure-{0}.mmd" -f $number)
    $outputFigure = Join-Path $assets ("figure-{0}.png" -f $number)
    $diagram = $matches[$index].Groups[1].Value.Trim() + [Environment]::NewLine
    Set-Content -LiteralPath $sourceFigure -Value $diagram -Encoding utf8
    & mmdc -i $sourceFigure -o $outputFigure -b white -t neutral -w 1800 -s 1.5 `
        -p (Join-Path $root "scripts\puppeteer-config.json")
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $outputFigure)) {
        throw "Mermaid rendering failed for figure $number."
    }
    # An empty alt label prevents Pandoc from treating the image description as
    # a second, implicit figure caption. The authored Figure N paragraph remains
    # the sole visible caption while the PNG retains a descriptive title.
    $replacement = "![](assets/figure-$number.png `"Architecture diagram $number`"){width=96%}"
    $rendered = $rendered.Remove($matches[$index].Index, $matches[$index].Length).Insert($matches[$index].Index, $replacement)
}

$renderSource = Join-Path $build "paper.render.md"
Set-Content -LiteralPath $renderSource -Value $rendered -Encoding utf8

$rawDocx = Join-Path $build "paper.raw.docx"
& pandoc $renderSource `
    --from=markdown+tex_math_dollars+raw_html `
    --to=docx `
    --standalone `
    --toc `
    --toc-depth=2 `
    --resource-path=$root `
    --output=$rawDocx
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $rawDocx)) {
    throw "Pandoc DOCX generation failed."
}

& $PythonPath (Join-Path $root "scripts\postprocess_docx.py") $rawDocx $output
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $output)) {
    throw "DOCX post-processing failed."
}

Write-Output "Created $output"
