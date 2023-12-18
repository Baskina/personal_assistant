from pathlib import Path
import pickle

from error_handler import *
from address_book.contact_book import AddressBook
from notes.note_book import NoteBook
import globals
from utils.constants import (
    WARNING_MESSAGE,
    ABORTING_OPERATION_MESSAGE,
    SORTING_PROGRESS_MESSAGE,
    BOT_COMMANDS,
    GREETING_MESSAGE,
    BYE_MESSAGE,
    HELP_INFO,
)
from file_config import FILE_NOTES
from notes import note_book
from sort_file import sort


def get_book():
    return AddressBook()


book = get_book()


def get_notes():
    return NoteBook()


notes = get_notes()


def handler_greetings(*args):
    return GREETING_MESSAGE


def handler_bye(*args):
    globals.IS_LISTENING = False
    book.save()
    notes.save()
    return BYE_MESSAGE


@input_error
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
    """add note by title
    only one word is accepted as title"""
    if len(data) == 1:
        title = data[0]
        if not notes.get(title, None):
            notes.add_note(data)
            notes.save()
            return f"Add note successfully.\n{notes.get(title, None)}"
        else:
            return "This note already exists!"
    else:
        return "Title must be 1 word!"


@input_error
def handler_list_all_notes(*args):
    """list of titles from all notes"""
    return notes.show_all_notes()


@input_error
def handler_delete_note(data: list):
    """delete note by its name"""
    title = " ".join(data)
    notes.delete_note(title)
    notes.save()
    return "Note deleted."


@input_error
def handler_add_tag(data: list):
    """add multiple tags to a note by its name
    tags should start wit "#"
    """
    title = " ".join([item for item in data if not item.startswith("#")])
    note = notes.get(title.strip(), None)
    if note:
        note.add_tag(data)
        notes.save()
        return f"Updated note:\n{notes.get(title, None)}"
    else:
        return "Note not found"


@input_error
def handler_edit_text(data: list):
    """replaces text in a note by title"""
    title = data[0]
    text = data[1:]
    note = notes.get(title, None)
    if note:
        note.edit_note_text(text)
        notes.save()
        return f"Updated note:\n{notes.get(title, None)}"
    else:
        return "Note not found"


@input_error
def handler_find_note(data: list):
    """returns all note content by note title"""
    title = " ".join(data)
    found_note = notes.find_note(title)
    if found_note:
        return f"Found following note:\n{found_note}"
    else:
        return "Nothing found..."


@input_error
def handler_add_contact(name):
    """usage:

    add contact [firstname] [surname]
    or: add contact [name]

    names should not include numbers!!"""
    if name:
        return book.add_record(name)
    else:
        raise EmptyNameError


def handler_help(*args):
    return "Available commands: \n" + HELP_INFO


@input_error
def handler_show_all(input):
    """usage:
    show all"""
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
    """usage:
        add phone [name] [phone]
    phones should be either 8 or 10 char long"""
    name, phone = name_splitter(arg)
    result = book.get(name.lower()).add_phone(phone)
    book.save()
    return result


@input_error
def handler_search(arg):
    """usage:
    search contacts [any str or int]"""
    if len(arg) == 1:
        user_input = arg[0]
        out = "Contacts found:\n"
        results = book.find_all(user_input)
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
    """usage:
        find contact [name]
    or  find contact [first name] [second name]"""
    name = name_splitter(arg)
    return book.find(name.lower())


@input_error
def handler_change_birthday(arg):
    """usage:
    change birthday [name] [new birthday in format xx/xx/xxxx]"""
    name, birthday = name_splitter(arg)
    book.get(name.lower(), None).edit_birthday(birthday)
    book.save()
    return f"Changed birthday of {name} to {birthday}"


def handler_delete_contact(user_input):
    name = name_splitter(user_input)
    book.delete(name.lower())
    book.save()
    return f"Contact {name} deleted"


def name_splitter(user_input: list) -> tuple:
    """function to check if contact in addressbook, and handle single name / firstname, surname"""
    if len(user_input) == 1:
        name = user_input[0]
        if not book.get(name.lower(), None):
            raise ContactNotFoundError
        return name
    elif len(user_input) == 2:
        # can be only name, surname OR name, argument
        name, arg = user_input
        long_name = f"{name.lower()}, {arg.lower()}"
        if book.get(name.lower(), None):
            return name, arg
        elif book.get(long_name.lower(), None):
            return long_name
        else:
            raise ContactNotFoundError
    elif len(user_input) == 3:
        firstname, surname, arg = user_input
        name = f"{firstname.lower()}, {surname.lower()}"
        if not book.get(name.lower(), None):
            raise ContactNotFoundError
    else:
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
    "help": handler_help,
    # file sorting
    "sort dir": handler_sort,
    # contacts
    "add contact": handler_add_contact,
    "show all": handler_show_all,
    "add phone": handler_add_phone,
    "change birthday": handler_change_birthday,
    "search contacts": handler_search,
    "find contact": handler_find,
    "delete contact": handler_delete_contact,
    # notes
    "add note": handler_add_note,
    "list notes": handler_list_all_notes,
    "edit note_text": handler_edit_text,
    "find note": handler_find_note,
    "delete note": handler_delete_note,
    "add tags": handler_add_tag,  # tag to note, to avoid parser problems
}
