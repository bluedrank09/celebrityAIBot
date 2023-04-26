from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

if __name__ == "__main__":
    try:
        # get api key from azure keyvault
        kv_uri = "https://kv-celeb-ai-chatbot.vault.azure.net/"
        kv_name = "kv-celeb-ai-chatbot"
        secret_name = "OPENAI-API-KEY"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kv_uri, credential=credential)

        openai_api_key = client.get_secret(secret_name).value

    except Exception as error:
        raise error
    
    finally:
        print(f":D")