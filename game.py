from player import Player
from helper import get_integer_input, get_str_input, clear, alert


class Game:

    def __init__(self, start_capital: int, start_bet: int):
        self.players: list[Player] = []
        self.betting_players: list[Player] = []
        self.active_player_idx = 0

        self.start_capital = start_capital
        self.start_bet = start_bet

        self.pot = 0
        self.to_meet = 0

        self.has_started = False

    def add_player(self, name: str):
        if self.has_started:
            raise RuntimeWarning("Game has already started, cannot add player!")
            return False

        if name in [p.name for p in self.players]:
            alert(name, "is already playing!")
            return

        player = Player(name, self.start_capital)
        self.players.append(player)

    def _call(self) -> bool:
        if not self.has_started:
            raise RuntimeWarning("Game not started yet, cannot call!")
            return False

        player = self.betting_players[self.active_player_idx]

        if self.to_meet > player.currently_betted:
            alert("You can't call, you have to either meet or fold", amount=2)
            return False

        return True

    def _meet(self, call_from_raise: bool = False) -> bool:
        if not self.has_started:
            raise RuntimeWarning("Game not started yet, cannot meet!")
            return False

        player = self.betting_players[self.active_player_idx]

        difference = self.to_meet - player.currently_betted
        if difference >= player.money:

            all_in = get_str_input("You are about to go all-in. Confirm [Y / N]")
            if all_in.lower() == "y":
                difference = player.money
                player.is_all_in = True

            else:
                if call_from_raise:
                    alert("Then select a different amount or don't raise!", amount=2)
                    return False

                fold = get_str_input("Rather fold? [Y / N]")
                if fold.lower() == "y":
                    self._fold()

                else:
                    difference = player.money
                    player.is_all_in = True

        player.money -= difference
        player.currently_betted += difference
        self.pot += difference

        return True

    def _raise(self, amount: int) -> bool:

        if not self.has_started:
            raise RuntimeWarning("Game not started yet, cannot raise!")
            return False

        player = self.betting_players[self.active_player_idx]

        if not amount:
            amount = get_integer_input("raise amount")

        new_meet = self.to_meet + amount

        if new_meet - player.currently_betted > player.money:
            alert("You don't have enough money to raise!")
            return False

        self.to_meet = new_meet
        res = self._meet(call_from_raise=True)
        if not res:
            self.to_meet -= amount
        return res

    def _fold(self) -> bool:
        if not self.has_started:
            raise RuntimeWarning("Game not started yet, cannot fold!")
            return False

        self.betting_players.pop(self.active_player_idx)
        self.active_player_idx -= 1

        if len(self.betting_players) == 1:
            self.finish_round(self.betting_players[0])

        return True

    # starts the game and runs it's loops
    def start(self):
        self.has_started = True
        self.betting_players = self.players.copy()

        while True:
            clear()
            self.print_state()

            player = self.betting_players[self.active_player_idx]

            if player.is_all_in:
                if all(p.is_all_in for p in self.betting_players):
                    print("All players are all-in or folded")
                    self.selct_winner()
                    break
                self.active_player_idx += 1
                self.active_player_idx %= len(self.betting_players)
                continue

            print(f"{player.name}'s turn")
            action = get_str_input("Action")

            success = self.handle_action(usr_inp=action)

            if success:
                self.active_player_idx += 1
                self.active_player_idx %= len(self.betting_players)

            if not self.has_started:
                break

    def handle_action(self, usr_inp: str):
        if usr_inp.lower().startswith("raise") or usr_inp.startswith("r"):
            num = ''.join(c for c in usr_inp if c.isdigit())
            num = int(num) if num != "" else None
            return self._raise(num)

        match usr_inp.lower():
            case "call" | "c":
                return self._call()
            case "meet" | "m":
                return self._meet()
            case "fold" | "f":
                return self._fold()
            case "end" | "e":
                self.selct_winner()
            case _:
                print("Invalid input:", usr_inp)
                action = get_str_input("Action")
                return self.handle_action(usr_inp=action)

    def selct_winner(self):

        winner_name = get_str_input("Winner")

        for player in self.betting_players:
            if player.name == winner_name:
                self.finish_round(winner=player)
                return

        alert("Name not found in betting_players:", winner_name, amount=2)

    def finish_round(self, winner: Player):
        winner.money += self.pot
        self.pot = 0
        self.to_meet = 0
        self.active_player_idx = 0
        self.has_started = False

        for player in self.players:
            player.finish_round()

    def print_state(self):
        print("Players:")
        max_name_length = max(len(player.name) for player in self.players)
        for player in self.players:
            spaces_after_name = max_name_length + 1 - len(player.name)
            money = str(player.money)
            spaces = len(str(self.start_capital)) + 3 - len(money)
            print(
                f"{player.name}:"
                + " " * spaces_after_name
                + f"{money}€"
                + " " * spaces
                + f"Bet: {player.currently_betted}€"
                + (" (all-in)" if player.is_all_in else "")
                + (" (folded)" if player not in self.betting_players else "")
            )
        print(f"\nPot: {self.pot}€\n\n")

    def __str__(self):
        return "\n".join([str(player) for player in self.players])
