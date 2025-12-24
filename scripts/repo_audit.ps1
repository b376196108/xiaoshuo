$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$repoRoot = Resolve-Path (Join-Path $scriptDir '..')

Push-Location $repoRoot
try {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        Write-Host "Python executable not found. Activate the xiaoshuo env or select an interpreter in VSCode."
        exit 1
    }

    Write-Host "Running repository audit..."
    & $pythonCmd.Source "scripts/repo_audit.py"
    $code = $LASTEXITCODE
    if ($code -eq 0) {
        Write-Host "Repo audit: PASS"
    }
    else {
        Write-Host "Repo audit: FAIL (exit code $code)"
        exit $code
    }
}
finally {
    Pop-Location
}
