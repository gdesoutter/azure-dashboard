import requests
import collections
from auth import get_token


class GraphClient:
    def __init__(self):
        self.token = get_token()
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def graph_search_group(self,group_name):
        url = f"https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName,'{group_name}')&$select=id,displayName"
        return requests.get(url, headers=self.headers).json()

    def graph_get_members(self,group_id):
        url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$select=displayName,mail,accountEnabled"
        return requests.get(url, headers=self.headers).json()
    
    def graph_get_inactive_users(self):
        url = "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,accountEnabled,signInActivity"
        return requests.get(url, headers=self.headers).json()

    def graph_get_user(self, username):
        url = f"https://graph.microsoft.com/v1.0/users?$filter=startswith(displayName,'{username}') or startswith(userPrincipalName,'{username}')&$select=displayName,userPrincipalName,mail,jobTitle,mobilePhone,id"
        return requests.get(url, headers=self.headers).json()
    
    def graph_get_user_groups(self, user_id): #On peut recuperer les roles et les groupes dans la meme requete
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/memberOf?$select=displayName"
        return requests.get(url, headers=self.headers).json()