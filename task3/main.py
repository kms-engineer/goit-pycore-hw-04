import sys
from pathlib import Path
from colorama import Fore, Style

COLOR_DIR = Fore.BLUE
COLOR_FILE = Fore.GREEN
COLOR_TREE = Fore.BLACK
COLOR_ERROR = Fore.RED

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <directory_path>")
        sys.exit(1)

    try:
        dir_path = sys.argv[1]
        path = validate_directory_path(dir_path)

        print(f"{COLOR_DIR}{path.name}/{Style.RESET_ALL}")
        show_dir_structure(path)

    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def show_dir_structure(directory, level=1):
    path = Path(directory)
    prefix = '    ' * level

    try:
        items = sorted(path.iterdir(), key=lambda p: p.name.lower())
    except PermissionError:
        print(f"{prefix}{COLOR_ERROR}Permission Denied{Style.RESET_ALL}")
        return

    for item in items:
        if item.is_dir():
            print(f"{prefix}{COLOR_DIR}{item.name}{Style.RESET_ALL}")
            show_dir_structure(item, level + 1)
        else:
            print(f"{prefix}{COLOR_FILE}{item.name}{Style.RESET_ALL}")

def validate_directory_path(path_str):
    path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"Directory '{path_str}' does not exist")

    if not path.is_dir():
        raise NotADirectoryError(f"'{path_str}' is not a directory")

    return path

if __name__ == "__main__":
    main()

