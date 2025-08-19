#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

file1 = 'en_us.lang'
file2 = 'ru_ru.lang'
out_file = 'out.txt'

def read_lang_file(path):
    # Возвращает список кортежей.
    entries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith('#') or stripped.startswith('//'):
                    continue
                if '=' in line:
                    key, _ = line.split('=', 1)
                    key = key.strip()
                else:
                    key = stripped
                entries.append((key, line))
        return entries
    except Exception as e:
        print(f"Ошибка при чтении файла '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def write_lines(path, lines):
    # Запись в файл
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    except Exception as e:
        print(f"Ошибка при записи в файл '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    global file1, file2, out_file
    parser = argparse.ArgumentParser(
        description="Сравнить ключи двух .lang файлов и вывести строки из первого, которых нет во втором."
    )
    parser.add_argument(
        "file1",
        nargs="?",
        default=file1,
        help="путь к первому .lang (по умолчанию en_us.lang)"
    )
    parser.add_argument(
        "file2",
        nargs="?",
        default=file2,
        help="путь ко второму .lang (по умолчанию ru_ru.lang)"
    )
    parser.add_argument(
        "out",
        nargs="?",
        default=out_file,
        help="путь к выходному файлу (по умолчанию out.txt)"
    )

    args = parser.parse_args()

    entries1 = read_lang_file(args.file1)
    entries2 = read_lang_file(args.file2)

    keys2 = {key for key, _ in entries2}
    diff_lines = [line for key, line in entries1 if key not in keys2] # Сравнение значений строк

    write_lines(args.out, diff_lines)

    print(f"Найдено {len(diff_lines)} строк. Результат в '{args.out}'.")

if __name__ == "__main__":
    main()
