# argon-lol:// şemasını bu kullanıcı için kaydeder (yönetici izni gerekmez).
# Çalıştır: powershell -ExecutionPolicy Bypass -File tools\register_protocol.ps1
# WindowsApps altındaki 0 baytlık Store kısayolu yerine gerçek yorumlayıcının yolu
$python = & python -c "import sys; print(sys.executable)"
$bridge = Join-Path $PSScriptRoot 'argon_bridge.py'
$key = 'HKCU:\Software\Classes\argon-lol'

New-Item -Path "$key\shell\open\command" -Force | Out-Null
Set-ItemProperty -Path $key -Name '(default)' -Value 'URL:Argon LoL Squad'
Set-ItemProperty -Path $key -Name 'URL Protocol' -Value ''
Set-ItemProperty -Path "$key\shell\open\command" -Name '(default)' -Value "`"$python`" -X utf8 `"$bridge`" `"%1`""

Write-Host "argon-lol:// kaydedildi -> $python $bridge"
