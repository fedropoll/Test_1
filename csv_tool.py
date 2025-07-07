import argparse
import csv
from tabulate import tabulate


def read_csv(file_path):
    with open(file_path, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            data.append(row)
        return data


def try_float(value):
    try:
        return float(value)
    except:
        return value


def filter_data(rows, column, op, val):
    result = []
    for row in rows:
        cell = row.get(column)
        if cell is None:
            continue

        cell_val = try_float(cell)
        val_comp = try_float(val)

        if op == 'eq':
            if cell_val == val_comp:
                result.append(row)
        elif op == 'lt':
            if isinstance(cell_val, (int, float)) and isinstance(val_comp, (int, float)):
                if cell_val < val_comp:
                    result.append(row)
        elif op == 'gt':
            if isinstance(cell_val, (int, float)) and isinstance(val_comp, (int, float)):
                if cell_val > val_comp:
                    result.append(row)
        else:
            print(f"Неизвестный оператор: {op}")
            break
    return result


def aggregate_data(rows, column, operation):
    numbers = []
    for row in rows:
        val = try_float(row.get(column, ''))
        if isinstance(val, (int, float)):
            numbers.append(val)

    if not numbers:
        return None

    if operation == 'avg':
        return sum(numbers) / len(numbers)
    elif operation == 'min':
        return min(numbers)
    elif operation == 'max':
        return max(numbers)
    else:
        print(f"Неизвестная операция агрегации: {operation}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Простой CSV фильтр и агрегатор")
    parser.add_argument("file", help="CSV файл для обработки")
    parser.add_argument("--where", help="Фильтр, например price=gt=500")
    parser.add_argument("--aggregate", help="Агрегация, например price=avg")

    args = parser.parse_args()

    try:
        rows = read_csv(args.file)
    except Exception as e:
        print("Ошибка при чтении файла:", e)
        return

    if args.where:
        parts = args.where.split('=')
        if len(parts) != 3:
            print("Неправильный формат фильтра. Используй: column=operator=value")
            return
        column, op, val = parts
        rows = filter_data(rows, column, op, val)

    if args.aggregate:
        parts = args.aggregate.split('=')
        if len(parts) != 2:
            print("Неправильный формат агрегации. Используй: column=operation")
            return
        column, operation = parts
        res = aggregate_data(rows, column, operation)
        if res is None:
            print("Нет данных для агрегации.")
        else:
            print(tabulate([[column, operation, res]], headers=["Column", "Operation", "Result"]))
    else:
        if rows:
            print(tabulate(rows, headers="keys"))
        else:
            print("Нет данных для вывода.")


if __name__ == "__main__":
    main()