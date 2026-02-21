from azure.identity import ClientSecretCredential
from config import TENANT_ID, CLIENT_ID, CLIENT_SECRET

def get_token():

    credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    token = credential.get_token("https://graph.microsoft.com/.default")

    return token.token