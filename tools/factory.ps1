param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$FactoryArgs
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$script = Join-Path $PSScriptRoot "factory.py"

$candidates = @()

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCommand) {
  $candidates += $pythonCommand.Source
}

$pyCommand = Get-Command py -ErrorAction SilentlyContinue
if ($pyCommand) {
  $candidates += $pyCommand.Source
}

$bundled = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path $bundled) {
  $candidates += $bundled
}

if ($candidates.Count -eq 0) {
  throw "No Python runtime found. Install Python or use the Codex bundled runtime."
}

Push-Location $repoRoot
try {
  & $candidates[0] $script @FactoryArgs
  exit $LASTEXITCODE
}
finally {
  Pop-Location
}
