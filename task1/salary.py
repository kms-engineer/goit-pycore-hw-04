from pathlib import Path
from decimal import Decimal

def read_salary_data(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found")

    salaries = []
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