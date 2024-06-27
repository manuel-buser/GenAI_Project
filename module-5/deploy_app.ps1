Compress-Archive -Path .\RAG_App.py, .\requirements.txt -DestinationPath .\app_zip.zip -Update

az webapp deploy --resource-group "genai-on-azure" --name "genai-on-azure-chatbot-app-service" --src-path .\app_zip.zip