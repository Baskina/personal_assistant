from datetime import datetime

from src.error_handler import *


class Field:
    def __init__(self, value):
        self.__value = value
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if len(value) == 2:
            first_name, second_name = value
            if not first_name.isalpha():
                raise ValueError("First name may not have numbers")
            elif not second_name.isalpha():
                raise ValueError("Second name may not have numbers")
            else:
                new_user = f"{first_name.lower()}, {second_name.lower()}"
                self.value = new_user
        elif len(value) == 1:
            value = value[0]
            if not value.isalpha():
                raise ValueError("Second name may not have numbers")
            else:
                new_user = value
                self.value = new_user.lower()
        else:
            raise ValueError("Wrong name input")

    def __str__(self):
        return self.value.title()


class Birthday(Field):
    def __init__(self, birthday):
        if birthday is None:
            self.birthday = birthday
        else:
            birthday = ''.join(filter(str.isdigit, birthday))
            if len(birthday) == 6:
                dt_bd = datetime.strptime(birthday, "%d%m%y")
                self.birthday = dt_bd
            elif len(birthday) == 8:
                dt_bd = datetime.strptime(birthday, "%d%m%Y")
                self.birthday = dt_bd
            else:
                raise ValueError(
                    "Date should be in format dd/mm/yy or dd/mm/yyyy")

    def __str__(self):
        if self.birthday is None:
            return "\"\""
        else:
            return str(self.birthday.date())


class Phone(Field):
    def __init__(self, value: str) -> None:
        value = ''.join(filter(str.isdigit, value))
        if len(value) == 10:
            self.value = value
        elif len(value) == 8:
            self.value = "80" + value
        else:
            raise WrongPhoneNumberError

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name}\nBirthday: {self.birthday}\nPhones: {'; '.join(p.value for p in self.phones)}"

    def find_phone(self, phone):
        for p in self.phones:
            if phone == p.value:
                return p
        return

    def add_phone(self, phone: str) -> str:
        new_phone = Phone(phone)
        self.phones.append(new_phone)
        return f"Added {new_phone} to {self.name}"

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return self
        raise ValueError

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                self.remove_phone(old_phone)
                self.add_phone(new_phone)
                return self
        raise ValueError
    
    def edit_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday.birthday is None:
            return None
        today_date = datetime.now()
        current_year = today_date.year
        birthday = self.birthday.birthday
        next_birthday = birthday.replace(year=current_year)

        if next_birthday < today_date:
            next_birthday = birthday.replace(year=current_year+1)
        days_to_bd = next_birthday - today_date

        return days_to_bd.days