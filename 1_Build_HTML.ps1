Write-Host "Settings location to Hugo directory"
Set-Location .\main
Write-Host "Creating .HTML files"

hugo `
    --gc `
    --minify `
    --panicOnWarning `
    --printI18nWarnings `
    --printMemoryUsage `
    --printPathWarnings `
    --printUnusedTemplates `
    --templateMetrics `
    --templateMetricsHints
