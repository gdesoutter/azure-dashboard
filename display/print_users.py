from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

console = Console()

def print_inactive_users(inactifs):
    table = Table(title=f"Utilisateurs inactifs depuis 90 jours")
    table.add_column("Nom", style="cyan")
    table.add_column("Email", style="white")
    table.add_column("Inactivité", style="red")

    for nom, mail, inactivite in inactifs:
        table.add_row(nom, mail, inactivite)

    console.print(table)

def print_users(user, user_memberof, user_roles):
    content_user_details = f"DisplayName  : {user[0][0]}\nUPN : {user[0][1]}\nMail: {user[0][2]}\nJobTitle: {user[0][3]}\nPhone: {user[0][4]}"
    console.print(Panel(content_user_details, title="USER DETAILS"))
    groups = "\n".join(user_memberof)
    content_user_memberof = f"{len(user_memberof)} groupes:\n{groups}"
    console.print(Panel(content_user_memberof, title="GROUPS"))
    roles = "\n".join(user_roles)
    content_user_roles = f"{len(user_roles)} rôles:\n{roles}"
    console.print(Panel(content_user_roles, title="ROLEs"))