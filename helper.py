import time
import os


def get_integer_input(name: str):
    user_input = "0"
    while not isinstance(user_input, int):
        user_input = input(f"Set {name}: ")
        if user_input.isdigit():
            user_input = int(user_input)  # type: ignore[assignment]
        else:
            print(f"Please enter a valid positive number for {name}!")

    return user_input


def get_str_input(text: str):
    user_input = input(text + ": ")
    return user_input.strip()


def clear():
    os.system("clear")


def alert(*args, amount=1.5):
    clear()
    print(*args)
    time.sleep(amount)
    return
