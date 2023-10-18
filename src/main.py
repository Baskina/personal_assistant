from user_actions_handler import get_handler, book, notes
from utils.constants import INVITE_MESSAGE, TYPE_OR_ATTRIBUTE_ERROR_MESSAGE, UNDEFINED_ERROR_MESSAGE
import globals
from utils.parser import parser
import pickle
from file_config import FILE_NOTES, FILE_CONTACT_BOOK



def main():
    while globals.IS_LISTENING:
        user_line = input(INVITE_MESSAGE)
        
        if user_line:
            try:
                command, data = parser(user_line)
                handler = get_handler(command)
                result = handler(data)
                print(result)
                continue
            except AttributeError:
                print(f'{TYPE_OR_ATTRIBUTE_ERROR_MESSAGE} \n{get_handler("help")()}')


if __name__ == "__main__":
    main()
