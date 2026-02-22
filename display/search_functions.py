from rich.console import Console
from datetime import datetime, timezone, timedelta
from services.graphclient import GraphClient

def search_group(groups):
    console = Console()
    if not groups['value']:
        console.print("[red]Aucun groupe trouvé[/red]")
        return

    if len(groups['value']) > 1:
        console.print("Plusieurs groupes trouvés :")
        for i, g in enumerate(groups['value']):
            console.print(f"  [{i}] {g['displayName']}")
        choix = int(input("Ton choix : "))
    else:
        choix = 0

    group = groups['value'][choix]
    return group

def search_inactive_users(inactive_users):
    jours = 90 # limite nombre de jours inactifs

    limit_date = datetime.now(timezone.utc) - timedelta(days=jours)
    inactifs = []
            
    for user in inactive_users['value']:
        sign_in = user.get('signInActivity')
        if not sign_in:
            inactifs.append((user['displayName'], user.get('mail') or "—", "Jamais connecté"))
            continue

        last_login = datetime.fromisoformat(sign_in['lastSignInDateTime'].replace("Z", "+00:00"))
        if last_login < limit_date:
            delta = (datetime.now(timezone.utc) - last_login).days
            inactifs.append((user['displayName'], user.get('mail') or "—", f"{delta} jours"))
    return inactifs

def search_user(user):
    console = Console()
    client = GraphClient()
    if not user['value']:
        console.print("[red]Aucun Utilisateur trouvé[/red]")
        return

    if len(user['value']) > 1:
        console.print("Plusieurs utilisateur trouvés :")
        for i, g in enumerate(user['value']):
            console.print(f"  [{i}] {g['displayName']}")
        try:
            choix = int(input("Ton choix : "))
            if choix > (len(user['value'])-1):
                console.print(f"[red]Entrée invalide merci de choisir un chiffre valide[/red]")
                return None
        except ValueError:
            console.print("[red]Entrée invalide[/red]")
            return None
    else:
        choix = 0

    user_data = []
    user_selected = user['value'][choix]
    user_data.append((user_selected['displayName'], user_selected['userPrincipalName'], user_selected.get('mail') or "N/A", user_selected.get('jobTitle') or "N/A", user_selected.get('mobilePhone') or 'N/A'))
    user_memberof = []
    user_roles = []
    userid = user_selected['id']
    memberoflist = client.graph_get_user_groups(userid)
    #print(memberoflist)
    for memberof in memberoflist['value']:
        if memberof['@odata.type'] == '#microsoft.graph.group':
            if memberof['displayName']:
                user_memberof.append((memberof['displayName']))
            else:
                continue
        elif memberof['@odata.type'] == '#microsoft.graph.directoryRole':
            if memberof['displayName']:
                user_roles.append((memberof['displayName']))
            else:
                continue
    return user_data,user_memberof, user_roles
