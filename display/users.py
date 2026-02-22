from rich.table import Table
from rich.console import Console

console = Console()

def print_inactive_users(inactifs):
    table = Table(title=f"Utilisateurs inactifs depuis 90 jours")
    table.add_column("Nom", style="cyan")
    table.add_column("Email", style="white")
    table.add_column("Inactivité", style="red")

    for nom, mail, inactivite in inactifs:
        table.add_row(nom, mail, inactivite)

    console.print(table)