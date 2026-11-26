from sqlite3 import Error
from battle import starters
from game import begin, take_turn
from history import read_history, setup_history, standings

def console_menu():
    """Show the terminal menu"""
    setup_history()
    battle = None
    while True:
        print("\n1 New battle   2 Attack   3 History   4 Scores   5 Exit")
        option = input("Choice: ").strip()
        try:
            if option == "1":
                name = input("Trainer name: ")
                print(", ".join(starters()))
                battle, message = begin(name, input("Starter: ").strip().lower())
                print (message)
            elif option == "2":
                move = input("Basic or type: ").strip().title()
                battle, message = take_turn(battle, move)
                print(message, "| HP (you, rival):", battle["hp"])
            elif option =="3":
                for trainer, move, message in read_history():
                    print(trainer, "|", move, "|", message)
            elif option == "4":
                rows, total = standings()
                print("Finished battles:", total)
                for trainer, wins, played in rows:
                    print(trainer, "| wins:", wins, "| played:", played)
            elif option =="5":
                return
            else:
                print("Choose 1 to 5")
        except ValueError as error:
            print(error)
        except (OSError, Error):
            print("Could not read or save the game files")
