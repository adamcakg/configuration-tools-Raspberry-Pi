keeper = {}


def add_to_keeper(item_dict):
    keeper.update(item_dict)
    print(keeper)


def is_in_keeper(string):
    print(keeper)
    if string in keeper:
        return True
    else:
        return False


def update_keeper(page, string, text):
    keeper[page][string] = text


def get_atribute_from_keeper(page, string):
    return keeper[page][string]
