from collections import UserList
import pickle

from file_config import FILE_NOTES



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Title(Field):
    def __init__(self, value):
        self.value = value


class Text(Field):
    def __init__(self, value):
        self.value = value


class Note:

    def __init__(self, note, tags=None):
        if tags:

            if type(tags) == str:
                self.title = Title(tags[1:])
            if type(tags) == list:
                self.title = Title(tags[0][1:])
        else:
            self.title = Title('No title')

        if tags:
            if type(tags) == list():

                for i in tags:
                    note = note + i
            else:
                note = note + tags
        self.note = Text(note)
        print(self.note)

    def __str__(self):
        tags = str(self.note).find('#')

        if self.title.value == 'No title':
            return f"Title: {self.title.value}, Text: {self.note.value}, Tags: No tags"
        if tags != -1:
            return f"Title: {self.title.value}, Text: {self.note.value[:tags]}, Tags: {self.note.value[tags:]}"
        else:
            return f"Title: {self.title.value}, Text: {self.note.value}, Tags: No tags"


class NoteBook(UserList):
    def __init__(self):
        try:
            with open(FILE_NOTES, "rb") as f:
                fr = f.read()
                if fr:
                    data = pickle.loads(fr)
                    self.data = data
                else:
                    self.data = []
        except FileNotFoundError:
            self.data = []

    def save(self):
        with open(FILE_NOTES, "wb") as fh:
            pickle.dump(self.data, fh)


    def add_note(self, note):

        if note.title.value == 'No title':
            self.data.append(note)
            #self.data['No title'] = self.data

        else:
            self.data[note.title.value] = note
        self.save()
        return self.data

    def add_tag(self, text, tag):
        for i in self.data.get('No title'):

            if text in str(i):
                self.data.get('No title').remove(i)
                n = Note(text, tag)
                # notes.add_note(n)
                if not self.data['No title']:
                    self.data.pop('No title')
        return self.data

    def edit_title(self, tag, new_tag):
        for k in self.data.keys():
            if k == tag:
                value = self.data.get(k)

        self.data[new_tag] = value
        self.data.pop(tag)

        return self.data

    def edit_text(self, tag, new_text):
        self.data[tag] = Note(new_text)
        return self.data

    def sort_note(self):
        lst = []
        self.val = None

        for k, v in self.data.items():
            if type(v) == list:
                self.val = v
            lst.append(k)

        new_keys = sorted(lst[0::2])
        for i in new_keys:
            print(str((self.data.get(i))))
        for i in self.val:
            print(str(i))
        return 'Successfuly sorted'

    def delete_note(self, data):
        for k, v in self.data.items():
            if type(v) == list:

                for i in v:

                    if data == k:
                        self.data.pop(k)
                        return 'deleted'
                    if data in str(i) or data == str(i):
                        v.remove(i)
                if not self.data.get(k):
                    self.data.pop(k)
                    return f'deleted {self.data}'

                return self.data

            if data == k or data == str(v):
                self.data.pop(k)

                return self.data

    def find_note(self, data):
        for k, v in self.data.items():

            if type(v) == list:

                for i in v:
                    if data == k:
                        return f'Found note {(str(i))}'
                    if data in str(i):
                        return f'Found note {(str(i))}'

            if data == k or data in str(v):
                return f'Found note {(self.data.get(k))}'
