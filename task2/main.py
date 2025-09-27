from pathlib import Path
from typing import List, Dict, Union
from cat import read_cat_data

def get_cats_info(path: Union[str, Path]) -> List[Dict[str, str]]:
    return read_cat_data(path)

def main() -> None:
    current_dir = Path(__file__).parent
    cats_file = current_dir / "cats.txt"

    try:
        print(get_cats_info(cats_file))
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

