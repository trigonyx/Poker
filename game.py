from player import Player

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
            return
        
        player = Player(name, self.start_capital)
        self.players.append(player)

    
    
    def _call(self):
        if not self.has_started:
            raise RuntimeWarning("Game not started yet, cannot call!")
            return
        
        player = self.players[self.active_player_idx]
        
    def _meet(self, call_from_raise: bool = False):
        if not self.has_started:
            raise RuntimeWarning("Game not started yet, cannot meet!")
            return
        
        player = self.players[self.active_player_idx]

        difference = self.to_meet - player.currently_betted
        if difference >= player.money:
            
            all_in = input("You are about to go all-in. Confirm [Y / N]: ")
            if all_in == "Y":   # replace with input or so
                difference = player.money
                player.is_all_in = True
            
            else:
                if call_from_raise:
                    # add functionality, so player has to select different action
                    return
                
                fold = input("Rather fold? [Y / N]: ")
                if fold == "Y":
                    self._fold()
                
                else:
                    difference = player.money
                    player.is_all_in = True


        player.money -= difference
        player.currently_betted += difference
        self.pot += difference

    def _raise(self, amount: int):
        if not self.has_started:
            raise RuntimeWarning("Game not started yet, cannot raise!")
            return
        
        player = self.players[self.active_player_idx]

        # cinfirm player has enough money

        # then increase self.to_meet and call self.meet() on player

    def _fold(self):
        if not self.has_started:
            raise RuntimeWarning("Game not started yet, cannot fold!")
            return

        self.players.pop(self.active_player_idx)
        self.active_player_idx -= 1


    # starts the game and runs it's loops
    def start(self):
        self.has_started = True
        self.betting_players = self.players.copy()

        while True:
            player = self.players[self.active_player_idx]
            print(f"{player.name}'s turn")
            action = input("Action: ")
            pass

            #self._meet()  - replace with player action + logic
            self.active_player_idx += 1

    
    def finish_round(self):
        self.pot = 0
        self.to_meet = 0
        self.active_player_idx = 0
        self.has_started = False

        for player in self.players:
            player.finish_round()