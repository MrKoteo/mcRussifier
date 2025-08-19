#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import re

file2 = 'ru_ru.lang'
out_file = 'indexes.txt'

def is_english(text: str) -> bool:
    # Возвращает True, если в тексте есть латинские буквы и нет кириллицы.
    has_latin = bool(re.search(r'[A-Za-z]', text))
    has_cyrillic = bool(re.search(r'[А-Яа-яЁё]', text))
    return has_latin and not has_cyrillic

def find_english_values(path: str):
    # Возвращает список кортежей (номер_строки, значение), где значение после '=' написано на английском.
    results = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for idx, raw_line in enumerate(f, start=1):
                line = raw_line.rstrip('\n')
                if not line.strip() or line.lstrip().startswith(('#', '//')):
                    continue
                if '=' in line:
                    _, value = line.split('=', 1)
                    value = value.strip()
                    if is_english(value):
                        results.append((idx, value))
    except FileNotFoundError:
        print(f"Ошибка: файл '{path}' не найден.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении '{path}': {e}", file=sys.stderr)
        sys.exit(1)
    return results

def write_indexes(path: str, entries):
    # Записывает в файл строки вида "номер: значение\n"
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for idx, value in entries:
                f.write(f"{idx}: {value}\n")
    except Exception as e:
        print(f"Ошибка при записи в '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    global file2, out_file
    parser = argparse.ArgumentParser(
        description="Ищет в .lang-файле английские значения и сохраняет их номера в файл."
    )
    parser.add_argument(
        "lang_file",
        nargs="?",
        default=file2,
        help="input .lang файл (по умолчанию ru_ru.lang)"
    )
    parser.add_argument(
        "--out", "-o",
        default=out_file,
        help="выходной файл (по умолчанию indexes.txt)"
    )

    args = parser.parse_args()

    entries = find_english_values(args.lang_file)
    write_indexes(args.out, entries)
    print(f"Найдено {len(entries)} строк. Результат записан в '{args.out}'.")

if __name__ == "__main__":
    main()