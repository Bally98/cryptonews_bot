class My_computer:

    def __init__(self, os, ram):  # инициализация атрибутов класса
        self.os = os
        self.ram = ram

    def __str__(self):  # магический метод для обращения к атрибуту путём вывода в понятном формате
        return f'os name is {self.os}'

    def __add__(self,
                other):  # магический метод для сложения чисел и атрибутов класса(уделить внимание позиции числа при взаимодействии с классом)
        print('__add__ called')
        if isinstance(other, (int, float)):
            return self.ram + other

    def __radd__(self,
                 other):  # магический метод для унификации сложения чисел с атрибутами класса(теперь неважно где стоит число, справа или слева)
        print('__radd__ called')
        return self + other
        # self.__price = price
    # def print_data(self):
    #     print(self.__os, self.__ram,self.__price)


# comp1 = My_computer('windows', 123)
# print(1 + comp1)

#Пример полиморфизма
class Bmw:
    def __init__(self, mark, color, year):
        self.mark = mark
        self.color = color
        self.year = year

    def __str__(self):
        return 'BMW'

    def get_info(self):
        return f'Age    : {2023 - self.year}, {self.color} color'


class Audi:
    def __init__(self, engine_capacity, color, year):
        self.engine_capacity = engine_capacity
        self.color = color
        self.year = year

    def __str__(self):
        return 'Audi'

    def get_info(self):
        return f'engine capacity:{self.engine_capacity}, Age:{2023 - self.year}'


class Mercedes:
    def __init__(self, factory_manufacturer, color, year):
        self.factory_manufacturer = factory_manufacturer
        self.color = color
        self.year = year

    def __str__(self):
        return 'Mercedes'

    def get_info(self):
        return f'factory{self.factory_manufacturer}, Age:{2023 - self.year}'


bmw_350 = Bmw('BMW 350', 'black', 2019)
audi_a7 = Audi(3.5, 'white', 2021)
mercedes_e350 = Mercedes('Dresden', 'grey', 2008)
list = [bmw_350, audi_a7, mercedes_e350]
#for car in list:
    #print(car, car.get_info())#вызов методов из разных классов с одним названием, но с разным функционалом


#Пример инкапсуляции (ограничения доступа к объектам класса извне)
class Pupils:
    def __init__(self, name, age):
        self.__name = name #Инициализируем приватные атрибуты двумя нижними подчёркиваниями
        self.__age = age

    def __str__(self):
        return self.name

    def get_info(self):#используем публичный метод для доступа к приватным атрибутам (этот метод также может быть приватным)
        return self.__name

pupil1 = Pupils('Tommy',12)
pupil2 = Pupils('Bob',11)
pupil3 = Pupils('John',16)

# print(pupil1.__name)#при вызове атрибута напрямую из класса в доступе будет отказано
# print(pupil2.__name)
# print(pupil3.__name)
# print()
# print(pupil1.get_info())#вызов атрибута через публичный метод будет успешен
# print(pupil2.get_info())
# print(pupil3.get_info())


class Main:

    car = 'Audi'
    def __init__(self, age, name):
        self.age = age
        self.name = name

    def print_smthg():
        print('Something')


class Second(Main):
    def __init__(self, height, weight):
        self.height = height
        self.weight = weight

    def show(self):
        print('Second class print')

# x = Second

# print(issubclass(Main, Second ))








a = 'хуйхуйхуй'
print(a[::-1])

















