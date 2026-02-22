import requests
from auth import get_token

def search_group(group_name):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName,'{group_name}')&$select=id,displayName"
    return requests.get(url, headers=headers).json()

def get_members(group_id):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$select=displayName,mail,accountEnabled"
    return requests.get(url, headers=headers).json()