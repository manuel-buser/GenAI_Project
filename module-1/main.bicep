param aoaiServiceName string
param searchServiceName string
param region string

module aoaiDeployment 'br/public:avm/res/cognitive-services/account:0.5.3' = {
  name: 'aoai-deployment'
  params: {
    kind: 'OpenAI'
    name: aoaiServiceName
    location: region
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}

module searchServiceDeployment 'br/public:avm/res/search/search-service:0.4.2' = {
  name: 'search-service-deployment'
  params: {
    name: searchServiceName
    location: region
    sku: 'free'
    partitionCount: 1
    replicaCount: 1
    disableLocalAuth: false
  }
}
