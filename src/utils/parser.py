import difflib

from src.utils.constants import BOT_COMMANDS


def parser(line):
    possible_command = " ".join(line.split(" ")[:2])
    data = line[len(possible_command) + 1 :]
    command = difflib.get_close_matches(possible_command, BOT_COMMANDS, n=1, cutoff=0.7)
    if not len(command):
        raise AttributeError
    data = data.strip().split(" ") if len(data) > 0 else None

    return command[0], data
