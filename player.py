class Player:
    def __init__(self, name: str, money: int):
        self.name = name
        self.money = money
        self.currently_betted = 0
        self.is_all_in = False

    def finish_round(self):
        self.currently_betted = 0
        self.is_all_in = False

    def __str__(self):
        return f"{self.name}: {self.money} points"