from rich.console import Console
from services.graphclient import GraphClient
from display.print_groups  import print_members
from display.print_users   import print_inactive_users, print_users
from display.search_functions import search_group, search_inactive_users, search_user
import pyfiglet
import os



def main():
    console = Console()
    client = GraphClient()
    console_title = pyfiglet.figlet_format("Azure Dashboard", font="slant")
    os.system('cls' if os.name == 'nt' else 'clear')


    while True:
        console.print(f"[bold cyan]{console_title}[/bold cyan]")
        console.print("  [1] Recherche un utilisateur")
        console.print("  [2] Utilisateurs inactifs depuis 90 jours")
        console.print("  [3] Rechercher un groupe")
        console.print("  [[bold cyan]Q[/bold cyan]] Quitter")

        choice = input("\n  Ton choix : ")

        if choice.lower() == "q":
            break

        elif choice == "1":
            username = input("Nom de l'user : ")
            req_user = client.graph_get_user(username)
            result = search_user(req_user)
            if result is not None:
                user, user_memberof, user_roles = result
                print_users(user, user_memberof, user_roles)

        elif choice == "2":
            req_inactives_users = client.graph_get_inactive_users()
            inactives_users = search_inactive_users(req_inactives_users)
            print_inactive_users(inactives_users)

        elif choice == "3":
            group_name = input("Nom du groupe : ")
            if group_name == "":
                console.print("[bold red]Entrée vide[/bold red]")
                continue
            req_groups = client.graph_search_group(group_name)
            group = search_group(req_groups)
            if group is not None:
                print_members(client.graph_get_members(group['id']), group['displayName'])

if __name__ == "__main__":
    main()