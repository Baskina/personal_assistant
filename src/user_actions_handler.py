from pathlib import Path

from error_handler import *
from address_book.contact_book import AddressBook
import globals
from utils.constants import WARNING_MESSAGE, ABORTING_OPERATION_MESSAGE, SORTING_PROGRESS_MESSAGE, BOT_COMMANDS, \
    GREETING_MESSAGE, BYE_MESSAGE
from file_config import FILE_NOTES
import pickle
from notes import note_book
from sort_file import sort


def get_book():
    return AddressBook()


book = get_book()


def get_notes():
    return note_book.NoteBook()


notes = get_notes()


def handler_greetings(*args):
    return GREETING_MESSAGE


def handler_bye(*args):
    globals.IS_LISTENING = False

    return BYE_MESSAGE


def handler_sort(dir_path):
    """
    Handler function for sorting a directory.

    Args:
        dir_path (str): The path of the directory to be sorted.

    Returns:
        str: A message indicating the status of the sorting operation.
    """
    # Prompt the user for confirmation
    choice = input(WARNING_MESSAGE)
    if choice.lower() == "n":
        return ABORTING_OPERATION_MESSAGE

    # Print progress message
    print(SORTING_PROGRESS_MESSAGE + dir_path[0])

    # Sort the directory
    sort.main(Path(dir_path[0]))

    return "Done!"


@input_error
def handler_add_note(data):
    tags = []
    new_data = data
    for i in data:
        if '#' in i:
            tags.append(i)

    for i in new_data:
        for j in tags:
            if j == i:
                new_data.remove(i)

    if tags:

        for i in new_data:
            for j in tags:
                if j == i:
                    new_data.remove(i)
        text = ' '.join(new_data)
    else:
        text = ' '.join(data)

    if tags:

        n = note_book.Note(text, tags)

        notes.add_note(n)

        print(f'Note has been added successfully:')
        for i in notes.data.values():
            if type(i) == list:
                for j in i:
                    print(str(j))
            print(str(i))

        return '>>>'

    else:
        n = note_book.Note(text)
        notes.add_note(n)

        print(f'Note has been added successfully:')
        for i in notes.data.values():
            if type(i) == list:
                for j in i:
                    print(str(j))
            print(str(i))
        return '>>>'


@input_error
def handler_add_tag(data):
    notes.add_tag(data[1], data[2])
    print(f'Tag has been added successfully:')
    for i in notes.data.values():
        if type(i) == list:

            for j in i:
                print(str(j))
        print(str(i))
    return '>>>'


@input_error
def handler_edit_title(data):
    notes.edit_title(data[0], data[1])
    print(f'Tag has been added successfully:')
    for i in notes.data.values():
        if type(i) == list:

            for j in i:
                print(str(j))
        print(str(i))
    return '>>>'


@input_error
def handler_edit_text(data):
    notes.edit_text(data[0], data[1])
    print(f'Tag has been added successfully:')
    for i in notes.data.values():
        if type(i) == list:
            print('here')
            for j in i:
                print(str(j))
        print(str(i))
    return '>>>'


@input_error
def handler_sort_note(*args):
    print('Start sorting')

    return print(notes.sort_note())


@input_error
def handler_find_note(data):
    lst = []

    for i in data:
        lst.append(notes.find_note(i))
    return '\n'.join(lst)


@input_error
def handler_delete_note(data):
    for i in data:
        notes.delete_note(i)
    print(f'Note(s) has been deleted successfully. Remained notes:')
    for i in notes.data.values():
        if type(i) == list:
            for j in i:
                print(str(j))

        print(str(i))
    return '>>>'


@input_error
def handler_add_contact(name):
    '''usage: 

    add contact [firstname] [surname]
    or: add contact [name]

    names should not include numbers!!'''
    if name:
        return book.add_record(name)
    else:
        raise EmptyNameError


def handler_help(*args):
    return "Available commands: \n" + "\n".join(sorted(BOT_COMMANDS))


@input_error
def handler_show_all(input):
    '''usage:
        show all'''
    out = "Contacts found:\n"
    name = book.find_all("")
    for n in name:
        out += f"{n}\n"
    if len(name) > 0:
        return out
    else:
        return "Contact list is empty"


@input_error
def handler_add_phone(arg: list):
    '''usage:
        add phone [name] [phone]
    phones should be either 8 or 10 char long'''
    name, phone = name_splitter(arg)
    result = book.get(name.lower()).add_phone(phone)
    book.save()
    return result


@input_error
def handler_search(arg):
    '''usage:
        search contacts [any str or int]'''
    if len(arg) == 1:
        input = arg[0]
        out = "Contacts found:\n"
        results = book.find_all(input)
        for res in results:
            out += f"{res}\n"
        if len(results) > 0:
            return out
        else:
            return "Nothing found"
    else:
        return "Too many words"


@input_error
def handler_find(arg: list):
    '''usage:
        find contact [name]
    or  find contact [first name] [second name]'''
    name = name_splitter(arg)
    return book.find(name.lower())


@input_error
def handler_change_birthday(arg):
    '''usage: 
        change birthday [name] [new birthday in format xx/xx/xxxx]'''
    name, birthday = name_splitter(arg)
    book.get(name.lower(), None).edit_birthday(birthday)
    book.save()
    return f"Changed birthday of {name} to {birthday}"


def handler_delete_contact(input):
    name = name_splitter(input)
    book.delete(name.lower())
    book.save()
    return f"Contact {name} deleted"


def name_splitter(input: list) -> tuple:
    '''function to check if contact in addressbook, and handle single name / firstname, surname'''
    if len(input) == 1:
        name = input[0]
        if not book.get(name.lower(), None):
            raise ContactNotFoundError
        return name
    elif len(input) == 2:
        # can be only name, surname OR name, argument
        name, arg = input
        long_name = f"{name.lower()}, {arg.lower()}"
        if book.get(name.lower(), None):
            return name, arg
        elif book.get(long_name.lower(), None):
            return long_name
        else:
            raise ContactNotFoundError
    elif len(input) == 3:
        firstname, surname, arg = input
        name = f"{firstname.lower()}, {surname.lower()}"
        if not book.get(name.lower(), None):
            raise ContactNotFoundError
    return name, arg


def get_handler(operator):
    return OPERATORS[operator]


OPERATORS = {
    "hello": handler_greetings,
    "hi": handler_greetings,
    "close": handler_bye,
    "exit": handler_bye,
    "good bye": handler_bye,
    "sort dir": handler_sort,
    "add contact": handler_add_contact,
    'add note': handler_add_note,
    'edit notetext': handler_edit_text,
    'edit notetitle': handler_edit_title,
    'sort note': handler_sort_note,
    'find note': handler_find_note,
    'delete note': handler_delete_note,
    'add notetag': handler_add_tag,
    "help": handler_help,
    "show all": handler_show_all,
    "add phone": handler_add_phone,
    "change birthday": handler_change_birthday,
    "search contacts": handler_search,
    "find contact": handler_find,
    "delete contact": handler_delete_contact
}
