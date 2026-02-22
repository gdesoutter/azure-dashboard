import requests
from auth import get_token
from datetime import datetime, timezone, timedelta

class GraphClient:
    def __init__(self):
        self.token = get_token()
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def search_group(self,group_name):
        url = f"https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName,'{group_name}')&$select=id,displayName"
        return requests.get(url, headers=self.headers).json()

    def get_members(self,group_id):
        url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$select=displayName,mail,accountEnabled"
        return requests.get(url, headers=self.headers).json()
    
    def get_inactive_users(self):
        url = "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,accountEnabled,signInActivity"

        jours = 90
        response = requests.get(url, headers=self.headers).json()
        limit_date = datetime.now(timezone.utc) - timedelta(days=jours)
        inactifs = []
        
        for user in response['value']:
            sign_in = user.get('signInActivity')
            if not sign_in:
                inactifs.append((user['displayName'], user.get('mail') or "—", "Jamais connecté"))
                continue

            last_login = datetime.fromisoformat(sign_in['lastSignInDateTime'].replace("Z", "+00:00"))

            if last_login < limit_date:
                delta = (datetime.now(timezone.utc) - last_login).days
                inactifs.append((user['displayName'], user.get('mail') or "—", f"{delta} jours"))

        return inactifs