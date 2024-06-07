param appServicePlanName string
param chatbotAppServiceName string

module serverFarmDeployment 'br/public:avm/res/web/serverfarm:0.1.1' = {
  name: 'app-service-deployment'
  params: {
    name: appServicePlanName
    kind: 'Linux'
    reserved: true
    sku: {
      capacity: 1
      family: 'B'
      name: 'B1'
      size: 'B1'
      tier: 'Basic'
    }
    location: 'East US 2'
  }
}

module chatbotAppServiceDeployment 'br/public:avm/res/web/site:0.3.5' = {
  name: 'app-deployment'
  params: {
    kind: 'app'
    name: chatbotAppServiceName
    serverFarmResourceId: serverFarmDeployment.outputs.resourceId
    appSettingsKeyValuePairs: {
      SCM_DO_BUILD_DURING_DEPLOYMENT: 'true'
    }
    location: 'East US 2'
    siteConfig: {
      alwaysOn: true
      linuxFxVersion: 'PYTHON|3.11'
    }
  }
}
