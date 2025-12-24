$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$repoRoot = Resolve-Path (Join-Path $scriptDir '..')

Push-Location $repoRoot
try {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        Write-Host "未检测到 Python，可执行文件或环境配置。请激活 `xiaoshuo` 虚拟环境或将解释器加入 PATH 后重试。"
        exit 1
    }

    Write-Host "运行 memory 健康检查..."
    & $pythonCmd.Source "scripts/healthcheck_memory.py"
    $code = $LASTEXITCODE

    if ($code -eq 0) {
        Write-Host "Memory healthcheck: OK"
    }
    else {
        Write-Host "Memory healthcheck: FAIL (exit code $code)"
        exit $code
    }
}
finally {
    Pop-Location
}
