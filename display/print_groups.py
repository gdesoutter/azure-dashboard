from rich.table import Table
from rich.console import Console

console = Console()

def print_members(members, group_name):
    table = Table(title=f"Groupe : {group_name}\n Membres:")
    table.add_column("Nom", style="cyan")
    table.add_column("Email", style="white")
    table.add_column("Statut", style="green")

    for user in members['value']:
        mail   = user['mail'] or "—"
        statut = "Actif" if user['accountEnabled'] else "Inactif"
        table.add_row(user['displayName'], mail, statut)

    console.print(table)