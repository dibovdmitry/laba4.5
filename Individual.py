#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import sys
import logging
from typing import List
import xml.etree.ElementTree as ET


"""
Выполнить индивидуальное задание 2 лабораторной работы 2.19, добавив аннтотации типов.
Выполнить проверку программы с помощью утилиты mypy.
"""


class UnknownCommandError(Exception):

    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class Airplane:
    path: str
    number: int
    model: int


@dataclass
class Race:
    airplanes: List[Airplane] = field(default_factory=lambda: [])

    def add(self, path: str, number: int, model: int) -> None:
        self.airplanes.append(
            Airplane(
                path=path,
                number=number,
                model=model,
            )
        )
        self.airplanes.sort(key=lambda airplane: airplane.number)

    def __str__(self) -> str:
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолёта"
            )
        )
        table.append(line)
        for idx, airplane in enumerate(self.airplanes, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    airplane.path,
                    airplane.number,
                    airplane.model
                )
            )
        table.append(line)
        return '\n'.join(table)

    def select(self) -> List[Airplane]:
        sel = input('Введите номер вашего самолёта: ')
        count = 0
        result: List[Airplane] = []
        for i, num in enumerate(number, 1):
            if sel == num['path']:
                count += 1
                result.append(airplane)
        return result

    def load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as fin:
            xml = fin.read()
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.fromstring(xml, parser=parser)

        self.airplanes = []
        for airplane_element in tree:
            path, number, model = None, None, None

            for element in airplane_element:
                if element.tag == 'path':
                    path = element.text
                elif element.tag == 'number':
                    number = element.text
                elif element.tag == 'model':
                    model = element.text

                if path is not None and number is not None \
                        and number is not None:
                    self.airplanes.append(
                        Airplane(
                            path=path,
                            number=number,
                            model=model
                        )
                    )

    def save(self, filename: str) -> None:
        root = ET.Element('airplanes')
        for airplane in self.airplanes:
            airplane_element = ET.Element('airplane')
            path_element = ET.SubElement(airplane_element, 'path')
            path_element.text = airplane.path
            number_element = ET.SubElement(airplane_element, 'number')
            number_element.text = str(airplane.number)
            model_element = ET.SubElement(airplane_element, 'model')
            model_element.text = airplane.model
            root.append(airplane_element)
        tree = ET.ElementTree(root)
        with open(filename, "w", encoding="utf-8") as fout:
            tree.write(fout, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    logging.basicConfig(
        filename='races.log',
        level=logging.INFO
    )

    race = Race()

    while True:
        try:
            command = input(">>> ").lower()
            if command == 'exit':
                break
            elif command == 'add':
                    path = input("Пункт назначения: ")
                    number = input("Номер рейса: ")
                    model = input("Тип самолёта: ")
                    race.add(path, number, model)
                    logging.info(
                    f"Добавлен самолёт: {path}, с номером рейса {number}, "
                    f"тип самолёта {model}")
            elif command == 'list':
                    print(race)
                    logging.info("Отображен список рейсов.")
            elif command.startswith('select '):
                    parts = command.split(maxsplit=1)
                    selected = race.select()
                    if selected:
                        for idx, airplane in enumerate(selected, 1):
                            print(
                            '{:>4}: {}'.format(idx, airplane.path)
                            )
                            logging.info(
                            f"Найдено {len(selected)} рейсов с "
                            f":номером {parts[1]}."
                            )
                    else:
                        print("Самолёты с данным номером не найдены.")
                        logging.warning(
                        f"Самолётов с номером: {parts[1]}  не найдено."
                        )
            elif command.startswith('load '):
                    parts = command.split(maxsplit=1)
                    race.load(parts[1])
                    logging.info(f"Загружены данные из файла {parts[1]}.")
            elif command.startswith('save '):
                    parts = command.split(maxsplit=1)
                    race.save(parts[1])
                    logging.info(f"Сохранены данные в файл {parts[1]}.")
            elif command == 'help':
                    print("Список команд:\n")
                    print("add - добавить рейс;")
                    print("list - вывести список рейсов;")
                    print("select  - запрос самолёта с заданным номером;")
                    print("load <имя_файла> - загрузить данные из файла;")
                    print("save <имя_файла> - сохранить данные в файл;")
                    print("help - отобразить справку;")
                    print("exit - завершить работу с программой.")
            else:
                raise UnknownCommandError(command)
        except Exception as exc:
            logging.error(f"Ошибка: {exc}")
            print(exc, file=sys.stderr)
