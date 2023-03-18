import inspect
from pathlib import Path
from colorama import Fore, Back, Style


def debug_print(*messages):
    print("DEBUG >>> ", end='')

    for item in messages:
        print(item, end='')

    print(__calling_item_on_stack_as_string(), end='')

    print("")


def __calling_item_on_stack_as_string() -> str:
    stack = inspect.stack()
    stack_item = stack[2]

    file_path: str = str(stack_item[1])
    file_name: str = Path(file_path).name
    line_number: str = str(stack_item[2])
    fn_name: str = str(stack_item[3])

    full_string: str = " >>> located in the function " + fn_name + "() on line " + line_number + " in " + file_name

    return full_string
