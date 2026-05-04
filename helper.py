def get_integer_input(name: str):
    user_input = "0"
    while not isinstance(user_input, int):
        user_input = input(f"Set {name}")
        if user_input.isdigit():
            user_input = int(user_input)  # type: ignore[assignment]
        else:
            print(f"Please enter a valid number for {name}!")
