from game import Game
from helper import get_integer_input, get_str_input, clear

clear()
start_capital = get_integer_input("starting capital")
start_bet = get_integer_input("starting bet")
clear()

game = Game(start_capital=start_capital, start_bet=start_bet)

# Game Loop
while True:
    print("POKER\n")
    print("Players:")
    for player in game.players:
        print(f"{player.name}: {player.money}€")

    print()

    inpt = get_str_input(
        "Press enter to start, q to quit, or enter a string to add a user"
    )

    if inpt == "":
        game.start()
    elif inpt == "q":
        break
    else:
        game.add_player(inpt.strip())

    clear()
