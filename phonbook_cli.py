import sys
from typing import List, Dict


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            return f'Error: {type(e).__name__}. Message: {e}'
    return wrapper


@handle_errors
def command_parse(prompt: str) -> None:
    prompt_list = prompt.strip().replace(',', '').replace('.', '').split()
    command = prompt_list.pop(0)
    if command in ('add', 'change') and len(prompt_list) >= 2 \
            and prompt_list[-1].isdigit() and len(prompt_list[-1]) in (10, 11):
        name = ' '.join(list(map(lambda i: i.capitalize(), prompt_list[:-1])))
        num = prompt_list[-1]
        if command == 'add':
            return add_contact(contact_dict, name, num)
        elif command == 'change':
            return edit_contact(contact_dict, name, num)
    elif command in ('phone', 'del') and len(prompt_list) >= 1:
        name = ' '.join(list(map(lambda i: i.capitalize(), prompt_list)))
        if command == 'phone':
            return get_number(contact_dict, name)
        elif command == 'del':
            return delete_contact(contact_dict, name)
    elif command == 'hello' and len(prompt_list) == 0:
        hello()
    else:
        raise ValueError('Check your command')
    return None


@handle_errors
def add_contact(contacts: Dict, name: str, num: str) -> str:
    if name not in contacts:
        contacts[name] = num
        return f'New contact "{name}: {num}" was added to contact list'
    raise ValueError(f'Name {name} already exist')


@handle_errors
def edit_contact(contacts: Dict, name: str, num: str) -> str:
    if name in contacts:
        contacts[name] = num
        return f'Phone number for "{name}" was changed to "{num}"'
    raise KeyError(f'Name {name} does not exist')


@handle_errors
def get_number(contacts: Dict, name: str) -> str:
    if name in contacts:
        return f'{name}: {contacts[name]}'
    raise KeyError(f'Name {name} does not exist')


@handle_errors
def delete_contact(contacts: Dict, name: str) -> str:
    if name in contacts:
        del contacts[name]
        return f'Contact "{name}" was deleted'
    raise KeyError(f'Name {name} does not exist')


def view_contacts(contacts: Dict) -> List:
    if not contacts:
        return ['\nYour contact list is empty']
    else:
        return [f'{k:<12}>>>{v:>15}' for k, v in contacts.items()]


def hello() -> str:
    return '\nHello. How can I help you?'


def main():
    tip = ("""
List of available commands:
        hello                   - Greetings
        add <name> <phone>      - Add new contact (<phone> : 10 or 11 digits)
        change <name> <phone>   - Change phone number (10 or 11 digits) for existing contact name
        phone <name>            - View phone number for existing contact name
        del <name>              - Delete existing contact
        show all                - View all contacts
        good bye | close | exit - Close program

        Command>>> """)
    while True:
        try:
            print(f'{" v0.0.1 ":*^70}')
            choice = input(tip).lower()
            if not choice:
                raise ValueError
            elif choice in ('good bye', 'close', 'exit'):
                raise KeyboardInterrupt
        except (KeyboardInterrupt, ValueError):
            print('\nGood bye!')
            sys.exit(0)
        else:
            if choice == 'hello':
                print(hello())
            elif choice == 'show all':
                print(*view_contacts(contact_dict), sep='\n')
            else:
                print(command_parse(choice))


if __name__ == '__main__':
    contact_dict = {'Lokist': '0005555555', 'Ollika': '0007777777'}  # For debugging
    # contact_dict = {}
    main()
