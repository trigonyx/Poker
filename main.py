from game import Game
from helper import get_integer_input


start_capital = get_integer_input("starting capital")
start_bet = get_integer_input("starting bet")

game = Game(start_capital=start_capital, start_bet=start_bet)

# Game Loop
while True:
    # ask for action (add player, start game, change settings, quit)
    pass