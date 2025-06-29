import os

def create_division(message: str) -> str:
    columns = os.get_terminal_size().columns
    padding_length = columns - len(message) - 2
    left_padding = '#' * (padding_length // 2)
    right_padding = '#' * ((padding_length + 1) // 2)
    return f"{left_padding} {message} {right_padding}"

print(create_division('END PROGRAM'))