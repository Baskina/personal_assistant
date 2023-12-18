import zipfile

from utils.constants import BOT_COMMANDS


class EmptyPhoneNumberError(Exception):
    pass


class WrongPhoneNumberError(Exception):
    pass


class EmptyNameError(Exception):
    pass


class EmptyNamePhoneError(Exception):
    pass


class ContactNotFoundError(Exception):
    pass


def input_error(handler):
    def error_handler(data):
        try:
            return handler(data)
        except EmptyPhoneNumberError:
            return f"Phone is required"
        except WrongPhoneNumberError:
            return f"Phone length should be 8 or 10 numbers"
        except EmptyNameError:
            return f"Enter contact name"
        except EmptyNamePhoneError:
            return f"Enter contact name and phone number"
        except ContactNotFoundError:
            return f"Contact does not exists"
        except KeyError:
            return f"Please, type one of the commands: {BOT_COMMANDS}"
        except FileNotFoundError:
            return f'Directory "{data[0]}" does not exist, please, check your path.'
        except zipfile.BadZipfile:
            pass
        except Exception as error:
            return f"Something happens: {error}"

    return error_handler
