from rich.console import Console
from services.graphclient import GraphClient
from display.groups  import print_members
from display.users   import print_inactive_users

def main():
    console = Console()
    client = GraphClient()

    while True:
        console.print("\n[bold cyan]--- Azure Dashboard ---[/bold cyan]")
        console.print("  [1] Rechercher un groupe")
        console.print("  [2] Utilisateurs inactifs depuis 90 jours")
        console.print("  [[bold cyan]Q[/bold cyan]] Quitter")

        choice = input("\n  Ton choix : ")

        if choice.lower() == "q":
            break

        elif choice == "1":
            group_name = input("Nom du groupe : ")
            groups = client.search_group(group_name)

            if not groups['value']:
                console.print("[red]Aucun groupe trouvé[/red]")
                continue

            if len(groups['value']) > 1:
                console.print("Plusieurs groupes trouvés :")
                for i, g in enumerate(groups['value']):
                    console.print(f"  [{i}] {g['displayName']}")
                choix = int(input("Ton choix : "))
            else:
                choix = 0

            group = groups['value'][choix]
            print_members(client.get_members(group['id']), group['displayName'])

        elif choice == "2":
            print_inactive_users(client.get_inactive_users())

if __name__ == "__main__":
    main()