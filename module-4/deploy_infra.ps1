param (
    [switch]$deploy,
    [string]$resourceGroupName,
    [string]$subscription
)

$today = Get-Date -Format "yyyy-MM-dd-hh-mm"
$deploymentName = "create_genai_resources" + "$today"
$subscriptionName = $subscription
$resourceGroupName = $resourceGroupName
$templateFile = "$PSScriptRoot\main.bicep"
$templateParameterFile = "$PSScriptRoot\main.bicepparam"

Write-Host "Azure Subscription: $subscriptionName"
Write-Host "Name $name"
Write-Host "resourceGroupName $resourceGroupName"
Write-Host "TemplateFile: $templateFile"
Write-Host "TemplateParameterFile: $templateParameterFile"

$VerbosePreference = "Continue"
$ErrorActionPreference = "Stop"

if ((Get-AzContext).Subscription.Name -ne $subscriptionName) {
    throw "Not logged in to correct subscription $subscriptionName"
}

if ($deploy) {
    New-AzResourceGroupDeployment -Name $deploymentName `
        -ResourceGroupName $resourceGroupName `
        -Mode Incremental `
        -Verbose `
        -TemplateFile $templateFile `
        -TemplateParameterFile $templateParameterFile 
} else {
    Test-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
        -TemplateParameterFile $templateParameterFile `
        -TemplateFile $templateFile `
        -Verbose

    New-AzResourceGroupDeployment -Name $deploymentName `
        -ResourceGroupName $resourceGroupName `
        -Mode Incremental `
        -Verbose `
        -TemplateFile $templateFile `
        -TemplateParameterFile $templateParameterFile `
        -WhatIf
}
