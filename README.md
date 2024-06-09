# Generative AI on Microsoft Azure 🦜

Associated Code Base for O'Reilly Course 'Generative AI on Microsoft Azure'.

## Prerequsites

- Azure Subscription

## Setup ⚙️

VS Code was leveraged to run all Jupyter notebooks in this repo. Microsoft has great [documentation](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) on how to setup Jupyter in VS Code. The two most important steps here are to ensure your [virtual environment](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_setting-up-your-environment) is created leveraging the requirements.txt file and to ensure the .env.sample environment file is filled out with your Azure OpenAI & Azure Search information.

You will also want to make sure you have Python installed. The version I had installed during the time of recording was [3.11.9](https://www.get-python.org/downloads/release/python-3119/)

Since we will be deploying infrastructure throughout the course, we need to install [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/install). You will also need [Azure PowerShell](https://learn.microsoft.com/en-us/powershell/azure/install-azps-windows?view=azps-12.0.0&tabs=powershell&pivots=windows-psgallery) so you can login to your Azure subscription to deploy the resources.

Once Bicep and Azure PowerShell are installed, open a PowerShell terminal and run:

```powershell
Connect-AzAccount
```

Make sure to install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli) on your machine. Once installed you will need to login to Azure

```powershell
az login
```

Ensure you request access to Azure OpenAI service via [this](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/limited-access#registration-process) link