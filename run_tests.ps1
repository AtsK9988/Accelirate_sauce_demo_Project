param([string]$Marker = "", [string]$Browser = "chromium")

$pytestArgs = @("--browser", $Browser)
if ($Marker) { $pytestArgs += @("-m", $Marker) }

python -m pytest @pytestArgs
exit $LASTEXITCODE
