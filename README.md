# celebrityAIBot

# Basic Setup
1. python -m venv venv (on powershell in the folder in file explorer)
2. pip install django
3. pip freeze > requirements.txt (to generate requirements.txt)

# Django Creation
1. Created project (celebrityAIBot is the name of the project, . means in this directory) : django-admin startproject celebrityAIBot .
Creating app : python manage.py startapp celebrityAIBotApp

# Testing
1. Running the server : python manage.py runserver
2. URL : http://127.0.0.1:8000/
3. Setup on shell to get API key value from Azure keyvault
    - set AZURE_CLIENT_ID
    - set AZURE_TENANT_ID
    - set AZURE_CLIENT_SECRET

# Links
1. Azure : https://celeb-ai-chatbot.azurewebsites.net/celebAI
2. Local :  http://127.0.0.1:8000/celebAI

# -
1. Created a ManagedIdentity
2. Gave the Azure Keyvault permisson to the ManagedIdentity

# Keyvault
1. Go to Microsoft Azure Portal - https://portal.azure.com/?quickstart=true#home  
2. Click "Key vaults"
3. Click "Create"
4. Create the keyvault under the existing resource group, give it a name, a pricing tier. Click next
5. Select the permisson model to be "Vault acess policy", and the resouce access to be "Azure Virtual Machines for deployment"
6. Enable public access

# Access Policies
1. Go to Microsoft Azure Portal - https://portal.azure.com/?quickstart=true#home  
2. Click on your keyvault
3. On the left hand side, click on "Access Policies" 
