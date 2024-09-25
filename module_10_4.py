print("Потоки гостей в кафе")

from time import sleep
from datetime import datetime
from threading import Thread
from random import randint
import queue

class Table:
    def __init__(self, number):
        self.number= number
        self.guest = None # in de-fault

    def __bool__(self):
        if self.guest == None:
            return False
        return True


class Guest (Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):  # имитация задержки -- времени на обслуживание
        sleep(  randint(3, 10)  ) # (сменить на 3, 10)
        #pass

    def __str__(self):
        return self.name



class Cafe():

    def __init__(self,   *tables: Table ):
        #self.name = name # на будущее, добавить имя столу
        self.queue = queue.Queue()
        self.tables = {table.number: table for table in tables}



    def  guest_arrival (self, *guests): #прибытие гостей)
        for guest in guests:
            n = self._find_free_table()
            if n is None:
                self.queue.put(guest)
                print(f'{guest} в очереди' )
            else:
                self.tables[n].guest = guest
                guest.start()
                print(f'{guest} сел(-а) за стол номер {n}.')

    def discuss_guests(self): # обслужить гостей
        while not (self._all_tables_free() and self.queue.empty()):
            for n, t in self.tables.items():
                if not t.guest is None:
                    if not t.guest.is_alive():
                        print(f'{t.guest} покушал(-а) и ушёл(ушла).\nСтол номер {n} свободен.')
                        if not self.queue.empty():
                            self.tables[n].guest = self.queue.get()
                            self.tables[n].guest.start()
                            print(f'{t.guest} вышел(-ла) из очереди и сел(-а) за стол номер {n}.')
                        else:
                            self.tables[n].guest = None

            #print(f'В очереди {self.queue.qsize()} посетителей.')

    def _find_free_table(self):
        for n, table in self.tables.items():
            # print(n, table)
            if not table:    #
                return n

    def _all_tables_free(self):
        for n, table in self.tables.items():
            if table:
                return False
        return True


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = ['Мария', 'Олег', 'Вахтанг', 'Серёга', 'Даша', 'Арман', 'Виктория', 'Никита', 'Павел', 'Илья',
                'Александр']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()