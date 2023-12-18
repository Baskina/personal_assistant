from collections import UserDict
import pickle

from record import Note
from file_config import FILE_NOTES


class NoteBook(UserDict):
    def __init__(self):
        try:
            with open(FILE_NOTES, "rb") as f:
                fr = f.read()
                if fr:
                    data = pickle.loads(fr)
                    self.data = data
                else:
                    self.data = {}
        except FileNotFoundError:
            self.data = {}

    def __repr__(self) -> str:
        out = ""
        for name in self:
            d = self.data.get(name, None)
            out += f"{d}\n"
        return out

    def save(self):
        with open(FILE_NOTES, "wb") as fh:
            pickle.dump(self.data, fh)

    def add_note(self, title: str) -> str:
        new_note = Note(title)
        self.data.update({new_note.title.value: new_note})
        return f"Sucsessfully added new note with title:\n{new_note}"

    def show_all_notes(self):
        out = []
        for item in self.data:
            out.append(item)
        return "\n".join(sorted(out))

    def find_note(self, name: str) -> Note:
        return self.data.get(name, None)

    def delete_note(self, name: str):
        if self.data.get(name, None):
            del self.data[name]
        else:
            return

    # def find_all(self, input: str) -> list:
    #     input = input.lower()
    #     find_result = []
    #     for contact in self.data.values():
    #         if input in str(contact.name).lower() and contact.name not in find_result:
    #             find_result.append(contact.name)
    #         for single_phone in contact.phones:
    #             if input in str(single_phone) and contact.name not in find_result:
    #                 find_result.append(contact.name)
    #     return find_result

    # def iterator(self, n=5):
    #     counter = 0
    #     output = {}
    #     for key, value in self.data.items():
    #         counter += 1
    #         if counter % n or counter == 0 or counter == len(self.data):
    #             output.update({key: value})
    #             if counter == len(self.data):
    #                 yield output
    #         else:
    #             output.update({key: value})
    #             yield output
    #             output = {}
