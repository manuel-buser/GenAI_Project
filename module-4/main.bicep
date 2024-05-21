param appServicePlanName string
param apiAppServiceName string
param frontEndAppServiceName string


module serverFarmDeployment 'br/public:avm/res/web/serverfarm:0.1.0' = {
  name: 'app-service-deployment'
  params: {
    name: appServicePlanName
    kind: 'Linux'
    reserved: true
    sku: {
      capacity: 1
      family: 'F'
      name: 'F1'
      size: 'F1'
      tier: 'Free'
    }
    location: 'East US 2'
  }
}

module apiAppServiceDeployment 'br/public:avm/res/web/site:0.3.5' = {
  name: 'app-api-deployment'
  params: {
    kind: 'app'
    name: apiAppServiceName
    serverFarmResourceId: serverFarmDeployment.outputs.resourceId
    location: 'East US 2'
    siteConfig: {
      alwaysOn: false
    }
  }
}

module frontEndAppServiceDeployment 'br/public:avm/res/web/site:0.3.5' = {
  name: 'app-front-end-deployment'
  params: {
    kind: 'app'
    name: frontEndAppServiceName
    serverFarmResourceId: serverFarmDeployment.outputs.resourceId
    location: 'East US 2'
    siteConfig: {
      alwaysOn: false
    }
  }
}
