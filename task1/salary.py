from pathlib import Path
from decimal import Decimal
from typing import List, Tuple, Union

def read_salary_data(file_path: Union[str, Path]) -> List[Tuple[str, Decimal]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found")

    salaries: List[Tuple[str, Decimal]] = []
    with path.open('r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    name, salary = line.split(',')
                    salaries.append((name.strip(), Decimal(salary.strip())))
                except ValueError:
                    continue

    return salaries