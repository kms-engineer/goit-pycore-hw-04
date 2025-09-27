import re
from typing import Dict, List, Tuple, Callable, Union

def main() -> None:
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!\n"
          "Available commands:\n"
          "  hello                     - Show greeting\n"
          "  add <username> <phone>    - Add new contact\n"
          "  change <username> <phone> - Update existing contact\n"
          "  phone <username>          - Show contact's phone number\n"
          "  all                       - Show all contacts\n"
          "  close, exit               - Exit the bot\n")

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

            command, args = parse_input(user_input)
            result = handle_command(command, args, contacts)

            if result == "exit":
                print("Good bye!")
                break
            print(result)

        except KeyboardInterrupt:
            print("\nGood bye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    args = user_input.split()
    if not args:
        return "", []

    command = args[0].lower()
    args = args[1:] if len(args) > 1 else []
    return command, args

def handle_command(command: str, args: List[str], contacts: Dict[str, str]) -> str:
    commands: Dict[str, Callable[[List[str], Dict[str, str]], str]] = {
        "hello": lambda args, contacts: "How can I help you?",
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": lambda args, contacts: show_all(contacts)
    }

    match command:
        case "close" | "exit":
            return "exit"
        case cmd if cmd in commands:
            return commands[cmd](args, contacts)
        case _:
            available = ', '.join(sorted(commands.keys()) + ['close', 'exit'])
            return f"Invalid command. Available commands: {available}"

def validate_phone(phone: str) -> str:
    if not re.match(r'^[+\-()\d\s]+$', phone):
        raise ValueError("Phone number can only contain digits, spaces, parentheses (), hyphens -, and plus sign +")

    digit_count = len(re.findall(r'\d', phone))
    if digit_count < 5 or digit_count > 15:
        raise ValueError("Phone number must contain between 5 and 15 digits")

    return phone

def parse_contact_args(args: List[str], required_count: int, operation: str) -> Union[str, Tuple[str, str]]:
    if len(args) < required_count:
        missing = required_count - len(args)
        arg_names = ["username", "phone"] if required_count == 2 else ["username"]
        raise ValueError(f"{operation} requires {required_count} arguments: {', '.join(arg_names[:required_count])}. Missing {missing} argument(s).")

    if required_count == 1:
        return args[0].strip()
    elif required_count == 2:
        username, phone = args[0].strip(), args[1].strip()
        return username, validate_phone(phone)

    return args[:required_count]

def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    try:
        username, phone = parse_contact_args(args, 2, "Add command")
    except ValueError as e:
        return str(e)

    if username in contacts:
        return f"Contact '{username}' already exists. Use 'change' command to update."

    contacts[username] = phone
    return "Contact added."

def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    try:
        username, phone = parse_contact_args(args, 2, "Change command")
    except ValueError as e:
        return str(e)

    if username not in contacts:
        return f"Contact '{username}' not found."

    contacts[username] = phone
    return "Contact updated."

def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    try:
        username = parse_contact_args(args, 1, "Phone command")
    except ValueError as e:
        return str(e)

    if username not in contacts:
        return f"Contact '{username}' not found."

    return f"Phone: {contacts[username]}"

def show_all(contacts: Dict[str, str]) -> str:
    if not contacts:
        return "No contacts found."

    result = "All contacts:\n"
    for username, phone in sorted(contacts.items()):
        result += f"{username}: {phone}\n"

    return result.rstrip()

if __name__ == "__main__":
    main()

