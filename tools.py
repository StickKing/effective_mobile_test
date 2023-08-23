from os import system, name, stat
from re import match
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing import Callable


def write_str(info: str, edit: bool = False) -> str:
    """Функция ввода строковых данных"""
    console = Console()
    value = None
    # В цикле запрашиваем значение пока оно не будет корректным
    while True:
        value = console.input(f'[cyan]Введите[/cyan] [green]{info}[/green]: ')
        value = value.strip()
        if value.isalpha():
            return value.title()
        else:
            if edit and value == '':
                # Пропуск пустой строки значение редактируется
                return value
            else:
                # Ошибка
                info = '{}Ошибка:{} вводимое значение должно состоять из букв'
                info.format(
                    '[bold]',
                    '[/bold]'
                )
                console.print(
                    info,
                    style='red')


def write_phone_number(
        info: str,
        find: bool = False,
        edit: bool = False) -> str:
    """Функция ввода телефонных номеров.
    Возвращает строку с номером соответствующий
    регулярным выражениям."""

    console = Console()
    # Регулярное выражение нового и редактруемого занчения
    context = r'^\d\(\d{3}\)\d{3}\-\d\d\-\d\d$'
    find_context = r'^\d\(\d{3}\)'

    error_str = '[bold]Ошибка:[/bold] номер не соответствует формату'
    value = None
    # В цикле запрашиваем значение пока оно не будет корректным
    while True:
        value = console.input(f'[cyan]Введите[/cyan] [green]{info}: ')
        value = value.strip()
        if not find:
            if match(context, value):
                return value
            else:
                if edit and value == '':
                    return value
                else:
                    console.print(
                        error_str,
                        style='red')
        else:
            if match(find_context, value):
                return value
            else:
                console.print(
                    error_str,
                    style='red')


def table_creator(
        headers: tuple[tuple],
        rows: list[list],
        title: str = '',
        tab_type: bool = True
) -> Table:
    """Функция создающая таблицу.
    В качестве входных данных выстают
    заголовки, строки и заглавие таблицы"""
    table = Table(title=title)

    for head in headers:
        table.add_column(head[0], style=head[1])
    if tab_type:
        for row in rows:
            table.add_row(*row)
    else:
        for row in rows:
            fio = f'{row[0]} {row[1][0]}.{row[2][0]}.'
            table.add_row(fio, *row[3:])

    return table


def pagination(data: list) -> tuple[int, list]:
    """Функция производит пагинацию данных.
    Возвращает количество страниц и
    данные разбитые постранично"""
    # Список в данными поделёнными на старницы
    page_data = []
    # Количетсво страниц
    pages = 0
    for i in range(0, len(data), 5):
        pages += 1
        page_data.append(data[:5])
        data = data[5:]
    return (pages - 1, page_data)


def clear_console(func: Callable) -> Callable:
    """Декоратор оборачивающий функцию"""
    def wrapper(*args, **kwargs) -> None:
        """Функция очищающая консоль и выполняющая
        вложенную функцию"""
        system('cls' if name == 'nt' else 'clear')
        func(*args, **kwargs)
    return wrapper


def ready_data(list_list: bool = True) -> list[list | str]:
    """Функция выгружает всю информацию из файла и возвращает в
    виде списка"""
    with open('db.txt', 'r', encoding='utf-8') as db:
        if list_list:
            data = [i.split(':') for i in db.readlines()]
        else:
            data = [i for i in db.readlines()]
    return data


def check_data_file() -> bool:
    """Функция проверяющая файл на существование
    и пустоту, в последнем случае возвращает True
    если он не пустой и False в обратном случае"""

    db = Path('db.txt')
    if not db.exists():
        # Создание файла если его нет
        db = open('db.txt', 'w')
        db.close()
        return False
    else:
        return stat('db.txt').st_size != 0
