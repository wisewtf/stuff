param (
    [Parameter(Mandatory=$true)]
    [string]$GroupTag
)

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$hostname = $env:COMPUTERNAME

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
$scriptPath = "$env:ProgramFiles\WindowsPowerShell\Scripts"

Write-Host "Installing NuGet package provider..." -ForegroundColor Yellow
Install-PackageProvider -Name NuGet -Force -Confirm:$false | Out-Null

if (-not (Test-Path $scriptPath)) {
    Write-Host "Creating script path directory..." -ForegroundColor Yellow
    New-Item -Path $scriptPath -ItemType Directory -Force | Out-Null
}
if (-not ($env:PATH -like "*$scriptPath*")) {
    Write-Host "Setting script path in environment variables..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$scriptPath", [EnvironmentVariableTarget]::Machine)
}

if ((Get-PSRepository -Name 'PSGallery').InstallationPolicy -ne 'Trusted') {
    Write-Host "Setting PSGallery as a trusted repository..." -ForegroundColor Yellow
    Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted
}

if (-not (Get-Command Get-WindowsAutopilotInfo -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Get-WindowsAutopilotInfo script..." -ForegroundColor Yellow
    Install-Script -Name Get-WindowsAutopilotInfo -Scope CurrentUser -Force
}

Write-Host "Running Get-WindowsAutopilotInfo..." -ForegroundColor Yellow
Get-WindowsAutopilotInfo -GroupTag $GroupTag -OutputFile ".\$hostname.csv"

Write-Host "CSV file created. Send it over to ITL2, or upload it on Intune if you have access." -ForegroundColor Green
