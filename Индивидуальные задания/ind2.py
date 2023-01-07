#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import jsonschema
import sys


def get_prod():
    name = input("Введите название для товара: ")
    shope = input("Введите название магазина:  ")
    price = float(input("Стоимость товара:  "))
    return {
        'name': name,
        'price': price,
        'shope': shope,
    }


def list_1(products):
    # Заголовок таблицы.
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 5,
        '-' * 20,
        '-' * 14,
        '-' * 17
    )
    print(line)
    print(
        '| {:^5} | {:^20} | {:^14} | {:^17} |'.format(
            "№",
            "Название товара",
            "Цена",
            "Название магазина"
        )
    )
    print(line)

    # Вывести данные о всех товарах.
    for idx, product in enumerate(products, 1):
        print(
            '| {:>5} | {:<20} | {:<14.2f} | {:>17} |'.format(
                idx,
                product.get('name', ''),
                product.get('price', 0),
                product.get('shope', '')
            )
        )
    print(line)


def select(products):
    # Проверить наличие товара.
    nalich = "new balance"

    flag = False
    for product in products:
        if nalich in product['name']:
            print(f'Товар в наличии: {product["name"]}\nЦена: {product["price"]:.2f}\n')
            flag = True

    if not flag:
        print(f'\nТаких товаров нет: {nalich}')


def help_1():
    print("Список команд:\n")
    print("add - добавить товар")
    print("list - вывести список товаров")
    print("select - товары в наличии")
    print("help - отобразить справку")
    print("save - сохранить список студентов;")
    print("load - загрузить список студентов;")
    print("exit - завершить работу с программой")


def save_products(file_name, products):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(products, fout, ensure_ascii=False, indent=4)


def load_products(file_name):
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "price": {"type": "number"},
                    "shope": {"type": "string"},
                },
                "required": ["name", "price", "shope"]
            }
        ]
    }
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadfile):
                print("Валидация прошла успешно")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации", file=sys.stderr)
            exit()
    return loadfile


def main():
    print("help - список всех команд")
    products = []

    while True:
        command = input(">>> ").lower()

        if command == 'exit':
            break

        elif command == "add":
            product = get_prod()

            products.append(product)
            products.sort(key=lambda item: item.get('name', ''))

        elif command == 'list':
            list_1(products)

        elif command == 'select':
            select(products)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_products(file_name, products)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            products = load_products(file_name)

        elif command == "help":
            help_1()
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
