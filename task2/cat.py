from pathlib import Path
from typing import List, Dict, Union

def read_cat_data(file_path: Union[str, Path]) -> List[Dict[str, str]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found")

    cats: List[Dict[str, str]] = []
    with path.open('r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    cat_id, name, age = line.split(',')
                    cats.append({
                        "id": cat_id.strip(),
                        "name": name.strip(),
                        "age": age.strip()
                    })
                except ValueError:
                    continue

    return cats