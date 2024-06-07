Compress-Archive -Path ..\module-3\Home.py, ..\module-3\requirements.txt -DestinationPath .\module-4

az webapp deploy --resource-group "genai-on-azure" --name "genai-on-azure-chatbot-app-service" --src-path .\module-4.zip