from user_actions_handler import get_handler, book, notes
from utils.constants import BOT_COMMANDS
import globals
from utils.parser import parser
import pickle
from file_config import file_contact_book, file_notes


def main():
    print(
        f"use these commands:\n{BOT_COMMANDS}\n"
    )
    while globals.is_listening:
        user_line = input(f"listening...\n")
        if user_line:
            try:
                command, data = parser(user_line)
                handler = get_handler(command)
                result = handler(data)
                print(result)
                with open(file_contact_book, "wb") as fh:
                    fh.write(pickle.dumps(book))
                with open(file_notes, "wb") as fh:
                    fh.write(pickle.dumps(notes))
                continue
            except AttributeError:
                print(f'Please, type one of the commands: {BOT_COMMANDS}')
            except TypeError:
                print(f'Please, type one of the commands: {BOT_COMMANDS}')
            except Exception as error:
                print(f"Something wrong happens: {error}")


if __name__ == "__main__":
    main()
