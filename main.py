from pick import pick
from rich.console import Console
from os import system, name
from rich.layout import Layout
from rich.panel import Panel
from tools import (clear_console,
                   table_creator,
                   write_phone_number,
                   write_str,
                   ready_data,
                   pagination,
                   check_data_file)


@clear_console
def edit_contact(
    edit: bool = False,
    data: list[str] = None,
    index: int = None
) -> None:
    """Функция добавление и редактирования контакта"""

    str_request = (
        'фамилию',
        'имя',
        'отчество',
        'название организации',
    )

    phone_request = (
        'номер рабочего телефона',
        'номер личного телефона',
    )

    if edit:
        info = '{}{}'.format(
            'Введите новое значение поля, ',
            'если оно не требует редакции нажмите enter'
        )
        console.print(info,
                      style='yellow')

    new_contact = []
    for req in str_request:
        new_contact.append(write_str(req, edit))

    info = '\nНомера телефонов вводятся в формате: [green3]8(916)384-97-54'
    console.print(info,
                  style='cyan')

    for req in phone_request:
        new_contact.append(write_phone_number(req, edit=edit))

    if not edit:
        # Добавление записи в файл
        db = open('db.txt', 'a', encoding='utf-8')
        # Новая запись преобразовывается в строку
        new_contact = ':'.join(new_contact) + '\n'
        db.write(new_contact)
        db.close()
        info = 'Контакт добавлен, нажмите enter для продолжения...'
        console.input(f'[green3]{info}[/green3]')
    else:
        # Изменение записи в файле
        if '' not in new_contact:
            # Новая запись преобразовывается в строку
            new_contact = ':'.join(new_contact) + '\n'
            data[index] = new_contact
        else:
            old_contact = data[index].split(':')
            for i in range(len(new_contact)):
                if new_contact[i] == '':
                    new_contact[i] = old_contact[i]

            if new_contact[-1][-1] != '\n':
                new_contact[-1] = new_contact[-1] + '\n'
            new_contact = ':'.join(new_contact)
            data[index] = new_contact

            # Запись информации в файл
        with open('db.txt', 'w', encoding='utf-8') as db:
            db.writelines(data)
        info = 'Контакт изменён, нажмите enter для продолжения...'
        console.input(f'[green3]{info}[/green3]')


@clear_console
def prepare_edit() -> None:
    """Функция редактирования контакта из стравочника"""
    console.print('Выберите запись, которую нужно изменить',
                  style='cyan')
    data = ready_data(False)
    pages, page_data = pagination(data)
    page = 0
    page_button = ['Следующая страница ->', 'Выйти']
    # Вывожу постранично контакты из справочника
    while True:
        temp_page_data = [i.replace(':', ' ') for i in page_data[page]]
        menu, index = pick(temp_page_data + page_button)

        if menu not in page_button:
            # Запуск процесса редатирования
            contact = page_data[page][index]
            id = data.index(contact)
            edit_contact(True, data, id)
            break
        if menu == 'Следующая страница ->':
            page += 1
        elif menu == '<- Предыдущая страница':
            page -= 1
        else:
            break

        if page == 0:
            page_button = ['Следующая страница ->', 'Выйти']
        elif page == pages:
            page_button = ['<- Предыдущая страница', 'Выйти']
        else:
            page_button = [
                'Следующая страница ->',
                '<- Предыдущая страница',
                'Выйти'
                ]


@clear_console
def show_contact() -> None:
    """Функция постраничного вывода контактов"""

    data = ready_data()
    pages, page_data = pagination(data)

    headers = (
        ('Фамилия', 'green3'),
        ('Имя', 'green3'),
        ('Отчество', 'green3'),
        ('Организация', 'dark_goldenrod'),
        ('Рабочий телефон', 'dark_goldenrod'),
        ('Личный телефон', 'green3')
    )

    value = 0
    while True:

        console.print(
            table_creator(headers, page_data[value], 'Список контактов')
            )
        info = '[cyan]{}[/cyan][violet]{}[/violet][cyan]{}[/cyan] {}{}'.format(
            'Страница №',
            value,
            '\nВсего страниц:',
            '[red1]',
            pages
        )
        console.print(info)
        info = 'Введите номер страницы (q если хотите выйти) и нажмите enter: '
        value = console.input(f'[green3]{info}[/green3]')

        if value.isdigit() and int(value) <= pages:
            value = int(value)

            system('cls' if name == 'nt' else 'clear')
        elif value.lower() == 'q':
            break
        else:
            system('cls' if name == 'nt' else 'clear')
            console.print('[bold]Ошибка:[/bold] неверное значение',
                          style='bright_red')
            value = 0


@clear_console
def search_contact() -> None:
    """Функция поиска по стравочнику по одному
    или нескольким критериям"""
    data = ready_data()
    title = 'Выберите поля по которым будет производиться поиск:'
    options = (
        'Фамилия',
        'Имя',
        'Отчество',
        'Компания',
        'Рабочий номер телефон',
        'Личный номер телефона'
        )

    selected = pick(options, title, multiselect=True, min_selection_count=1)

    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
    )
    layout['upper'].split_row(
                Layout(name='Критерии поиска'),
                Layout(name='Результат поиска')
            )

    headers = (
        ('ФИО', 'cyan'),
        ('Компания', 'cyan'),
        ('Раб. тел.', 'cyan'),
        ('Лич. тел.', 'cyan'),
    )

    search_info = ''
    search_data = []
    for i in selected:
        # Ввод значение выбранных полей
        if i[1] == 4 or i[1] == 5:
            value = write_phone_number(i[0], find=True)
        else:
            value = write_str(i[0].lower())

        # Поиск данных в файле
        for dd in data:
            check_data = dd[int(i[1])]
            if value in check_data:
                search_data.append(dd)

        # Вывод найденой информации
        table = table_creator(
            headers,
            search_data,
            tab_type=False,
            title='Результат поиска'
            )

        info = f'[green][bold]{i[0]}[/bold][/green] = [yellow]{value}\n'
        search_info += info
        layout['upper']['Критерии поиска'].update(
            Panel(search_info, expand=False)
            )
        layout['upper']['Результат поиска'].update(table)

        system('cls' if name == 'nt' else 'clear')

        console.print(layout, end='')

        data = search_data.copy()
        search_data = []

    console.input('[green3]Нажмите enter для продолжения...')


def main():
    """Главная функция"""

    # Запуск бесконечного вывода главного меню
    while True:
        # Пункты меню
        options = (
            'Добавить контакт',
            'Просмотреть контакты',
            'Поиск',
            'Изменить контакт',
            'Выход из программы'
        )
        info = '[red]Справочник пуст. Нажмите enter чтобы продолжить[/red]'
        # Вывод меню и работа с ним
        menu, index = pick(options, 'Меню')
        if index == 0:
            edit_contact()
        elif index == 1:
            if check_data_file():
                show_contact()
            else:
                console.input(info)
        elif index == 2:
            if check_data_file():
                search_contact()
            else:
                console.input(info)
        elif index == 3:
            if check_data_file():
                prepare_edit()
            else:
                console.input(info)
        elif index == 4:
            break

        system('cls' if name == 'nt' else 'clear')


if __name__ == '__main__':
    console = Console()
    main()
