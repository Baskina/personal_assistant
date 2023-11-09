from src.user_actions_handler import get_handler
from src.utils.constants import INVITE_MESSAGE, TYPE_OR_ATTRIBUTE_ERROR_MESSAGE
from src import globals
from src.utils.parser import parser
from src.interface import Terminal


def main():
    while globals.IS_LISTENING:
        user_line = input(INVITE_MESSAGE)

        if user_line:
            try:
                command, data = parser(user_line)
                handler = get_handler(command)
                result = handler(data)
                terminal = Terminal()
                terminal.show_result(result)
                continue
            except AttributeError:
                print(f'{TYPE_OR_ATTRIBUTE_ERROR_MESSAGE} \n{get_handler("help")()}')


if __name__ == "__main__":
    main()
