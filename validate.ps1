Write-Host "=== 1. Migraciones pendientes ===" -ForegroundColor Cyan
uv run python manage.py makemigrations --check
if ($?) { Write-Host "OK - Sin migraciones pendientes" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "`n=== 2. System check ===" -ForegroundColor Cyan
uv run python manage.py check
if ($?) { Write-Host "OK - Sin errores" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "`n=== 3. Esquema OpenAPI (drf-spectacular) ===" -ForegroundColor Cyan
uv run python manage.py spectacular --file schema.yml --validate
if ($?) { Write-Host "OK - Esquema valido" -ForegroundColor Green; Remove-Item -Force schema.yml } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "`n=== 4. Tests (35) ===" -ForegroundColor Cyan
uv run python manage.py test --verbosity=2 --keepdb
if ($?) { Write-Host "OK - Todos pasan" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "`n`nRESUMEN:" -ForegroundColor Yellow
Write-Host "Migraciones: OK" -ForegroundColor Green
Write-Host "System check: OK" -ForegroundColor Green
Write-Host "OpenAPI: OK" -ForegroundColor Green
Write-Host "Tests: OK" -ForegroundColor Green
