from collections import UserDict
import pickle

from record import Record
from file_config import FILE_CONTACT_BOOK


class AddressBook(UserDict):
    def __init__(self):
        try:
            with open(FILE_CONTACT_BOOK, "rb") as f:
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
        with open(FILE_CONTACT_BOOK, "wb") as fh:
            pickle.dump(self.data, fh)

    def add_record(self, record: set):
        new_user = Record(record)
        self.data.update({new_user.name.value: new_user})
        self.save()
        return f"Sucsessfully added new contact:\n{new_user}"

    def find(self, name: str) -> Record:
        return self.data.get(name, None)

    def find_all(self, user_input: str) -> list:
        user_input = user_input.lower()
        find_result = []
        for contact in self.data.values():
            if (
                    user_input in str(contact.name).lower()
                    and contact.name not in find_result
            ):
                find_result.append(contact.name)
            for single_phone in contact.phones:
                if user_input in str(single_phone) and contact.name not in find_result:
                    find_result.append(contact.name)
        return find_result

    def delete(self, name: str):
        if self.data.get(name, None):
            del self.data[name]
        else:
            print("unsucsessfull")
            return

    def iterator(self, n=5):
        counter = 0
        output = {}
        for key, value in self.data.items():
            counter += 1
            if counter % n or counter == 0 or counter == len(self.data):
                output.update({key: value})
                if counter == len(self.data):
                    yield output
            else:
                output.update({key: value})
                yield output
                output = {}
