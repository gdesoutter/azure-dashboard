import requests
from auth import get_token
from datetime import datetime, timezone, timedelta

def get_inactive_users():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,accountEnabled,signInActivity"

    jours = 90
    response = requests.get(url, headers=headers).json()
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