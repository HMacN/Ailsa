import inspect
from pathlib import Path
from colorama import Fore, Back, Style


def debug_print(*messages):
    """
    A helpful debugging function.  Prints out the given arguments as a string, along with the location and line number
    of the print statement in the code.

    @param messages: A series of arguments, which are the messages to print to console.
    @return:
    """
    print(Fore.YELLOW, end="")
    print("DEBUG >>> ", end='')
    print(Style.RESET_ALL, end="")

    for item in messages:
        print(item, end='')

    print(Fore.YELLOW, end="")
    calling_location: str = __calling_item_on_stack_as_string__()
    print(Fore.YELLOW, end="")
    print(calling_location, end='')

    print("")
    print(Style.RESET_ALL, end="")


def __calling_item_on_stack_as_string__() -> str:
    """
    Generates a string which corresponds to the stack item that called this function.

    @return: A str which describes the calling stack item.
    """
    stack = inspect.stack()
    stack_item = stack[2]

    file_path: str = str(stack_item[1])
    file_name: str = Path(file_path).name
    line_number: str = str(stack_item[2])
    fn_name: str = str(stack_item[3])

    full_string: str = " >>> located in the function " + fn_name + "() on line " + line_number + " in " + file_name

    return full_string


def display_progress_percent(current_value: int, final_value: int):
    """
    Displays a percentage progress bar to the console.  Deletes and re-writes itself to avoid filling the console.

    @param current_value:   An int, which is the absolute value of current progress.
    @param final_value:     An int, which is the absolute value of the completed process.
    @return:
    """
    progress_percent = int((current_value / final_value) * 100)

    print(Style.BRIGHT, Fore.BLACK, Back.LIGHTYELLOW_EX, end="")
    print("\r  Progress:" + str(progress_percent) + "%  ", end="")
    print(Style.RESET_ALL, end="")

    if current_value == final_value:
        print("")
