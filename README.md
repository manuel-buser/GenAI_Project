# Generative AI on Microsoft Azure 🦜

Associated Code Base for O'Reilly Course 'Generative AI on Microsoft Azure'.

## Prerequsites

- Azure Subscription

## Module 1 Setup ⚙️

VS Code was leveraged to run all examples in the module-1 folder. Microsoft has great [documentation](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) on how to setup Jupyter in VS Code. The two most important steps here are to ensure your [virtual environment](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_setting-up-your-environment) is created leveraging the requirements.txt file and to ensure the .env.sample environment file is filled out with your Azure OpenAI & Azure Search information.

You will also want to make sure you have Python installed. The version I had installed during the time of recording was [3.11.9](https://www.get-python.org/downloads/release/python-3119/)

Since we will be deploying infrastructure in this module, we need to install [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/install). You will also need [Azure PowerShell](https://learn.microsoft.com/en-us/powershell/azure/install-azps-windows?view=azps-12.0.0&tabs=powershell&pivots=windows-psgallery) so you can login to your Azure subscription to deploy the resources.

Once Bicep and Azure PowerShell are installed, open a PowerShell terminal and run:

```powershell
Connect-AzAccount
```

## Module 2 Setup ⚙️

If the prerequsite steps were followed in Module 1 to setup VS Code, Jupyter, and Python, the same steps apply here. Make sure to use module-2's requirements.txt and .env.sample environment file.



python -m streamlit run Home.py --server.port 8000 --server.address 0.0.0.0