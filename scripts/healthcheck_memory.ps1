$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

Write-Host "开始执行内存健康检查..."
Push-Location $repoRoot
try {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        Write-Host "未检测到 python 命令，请激活 xiaoshuo 虚拟环境或在 VSCode 选择解释器。"
        exit 1
    }

    & $pythonCmd.Source "scripts/healthcheck_memory.py"
    $code = $LASTEXITCODE
    if ($code -ne 0) {
        Write-Host "[EXIT] code=$code"
        exit $code
    }
    else {
        Write-Host "[EXIT] code=0"
        exit 0
    }
}
finally {
    Pop-Location
}

