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

