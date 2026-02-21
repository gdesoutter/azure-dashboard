import requests
from auth import get_token
from rich.table import Table
from rich.console import Console
from datetime import datetime, timezone, timedelta

console = Console()

def search_group(group_name):
    token = get_token()

    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName,'{group_name}')&$select=id,displayName"

    response = requests.get(url, headers=headers)
    return response.json()

def get_members(group_id):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$select=displayName,mail,accountEnabled"

    response = requests.get(url, headers=headers)
    return response.json()

def print_members(members, group_name):
    table = Table(title=f'Groupe: {group_name}')

    table.add_column("Nom", style="cyan")
    table.add_column("Email", style="white")
    table.add_column("Status", style="green")

    for user in members['value']:
        name    = user['displayName']
        mail    = user['mail'] or "--"
        statut  = "Actif" if user['accountEnabled'] else "Inactif"
        table.add_row (name, mail, statut)
    
    console.print(table)

def get_inactive_users(jours=90):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,accountEnabled,signInActivity"

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
            inactifs.append((user['displayName'], user.get('mail') or "--", f"{delta} jours"))
    return inactifs
#group_name = "Admin_SCSQ"
#group = search_group(group_name)
#group_id = group['value'][0]['id']
#print_members(get_members(group_id), group_name)

while True:
    console.print("\n[bold cyan]--- Azure Dashboard ---[/bold cyan]")
    console.print(" [1] Rechercher un groupe")
    console.print(" [2] Utilisateurs Inactifs depuis 90 jours")
    console.print(" [[bold cyan]Q[/bold cyan]] Quitter")

    choice = input("\n Ton choix : ")

    if choice.lower() == "q":
        break
    
    elif choice == "1":

        group_name = input ("Nom du groupe: ")
        groups = search_group(group_name)

        if not groups['value']:
            console.print("[red]Aucun groupe trouve[/red]")
            continue

        if len(groups['value']) > 1:
            console.print("Plusieurs groupes trouvés:")
            for i, g in enumerate(groups['value']):
                console.print(f" [{i}] {g['displayName']}")
            choix = int(input("Ton choix: "))
        else:
            choix = 0

        group = groups['value'][choix]
        members = get_members(group['id'])
        print_members(members, group['displayName'])
    
    elif choice == "2":

        inactives_users = get_inactive_users()

        table = Table(title=f"Utilisateurs inactifs depuis 90 jours")
        table.add_column("Name", style="cyan")
        table.add_column("Mail", style="white")
        table.add_column("Inactivité", style="red")

        for nom, mail, inactivite in inactives_users:
            table.add_row(nom,mail,inactivite)
        console.print(table)
