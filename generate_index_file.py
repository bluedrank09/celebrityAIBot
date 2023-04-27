# GENERATING INDEX FILE
#importing libraries needed - os is pre-installed
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import os

if __name__ == "__main__":
    try:
        # get api key from azure keyvault
        kv_uri = "https://kv-celeb-ai-chatbot.vault.azure.net/"
        kv_name = "kv-celeb-ai-chatbot" # name of the keyvault
        secret_name = "OPENAI-API-KEY"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kv_uri, credential=credential)

        openai_api_key = client.get_secret(secret_name).value
        os.environ["OPENAI_API_KEY"] = openai_api_key # setting api key in the environment as an environemnt variable

        documents = SimpleDirectoryReader('docs').load_data() # loading the data from the docs folder to genertae the index json file

        index = GPTSimpleVectorIndex.from_documents(documents) # creating index

        index.save_to_disk('data/actor_index.json') #creating a json file under the folder called data. this json file is what OPENAI will use 

    except Exception as error:
        raise error # raising potential errors if there is one
    
    finally:
        print(f":D")