import inspect
from pathlib import Path
from colorama import Fore, Back, Style


def debug_print(*messages):
    print("DEBUG >>> ", end='')

    for item in messages:
        print(item, end='')

    print(__calling_item_on_stack_as_string__(), end='')

    print("")


def __calling_item_on_stack_as_string__() -> str:
    stack = inspect.stack()
    stack_item = stack[2]

    file_path: str = str(stack_item[1])
    file_name: str = Path(file_path).name
    line_number: str = str(stack_item[2])
    fn_name: str = str(stack_item[3])

    full_string: str = " >>> located in the function " + fn_name + "() on line " + line_number + " in " + file_name

    return full_string


def display_progress_percent(current_value: int, final_value: int):
    progress_percent = int((current_value / final_value) * 100)

    print(Style.BRIGHT, Fore.BLACK, Back.LIGHTYELLOW_EX, end="")
    print("\r  Progress:" + str(progress_percent) + "%  ", end="")
    print(Style.RESET_ALL, end="")

    if current_value == final_value:
        print("")

