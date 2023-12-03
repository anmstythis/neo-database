import sqlite3 as sql
from abc import ABC, abstractmethod
from staff import Staff 
from staffpost import StaffPost
from corpus import Corpus
from education import Education
from staff_in_corp import StaffInCorp
import os

def executequery(query, value = None):
    try:
        with sql.connect("neocorp.db") as conn:
            curs = conn.cursor()
            if value:
                curs.execute(query, value)
                conn.commit()
            else:
                curs.execute(query)
    except sql.Error as err:
        print(f"Ошибка {err}")

def deletecolumn(table, value):
    try:
        conn = sql.connect("neocorp.db")
        curs = conn.cursor()

        delete = f"delete from {table} where id = ?"
        curs.execute(delete, (value,))

        conn.commit()
        conn.close()
    except sql.Error as err:
        print(f"Ошибка {err}")

def staff_in_corp():
    script = '''
            create table if not exists staff_in_corp(
                id integer primary key,
                staff_id integer,
                corp_id integer,
                foreign key (staff_id) references staff (id),
                foreign key (corp_id) references corpus (id)
            )
    '''
    executequery(script)

def searchid(table, column, value):
    try:
        with sql.connect("neocorp.db") as conn:
            curs = conn.cursor()
            select = f"select id from {table} where {column} = \"{value}\""
            curs.execute(select)
            conn.commit()
            idkey = curs.fetchone()
    except sql.Error as err:
        print(f"Ошибка {err}")

    return idkey[0]

def addvalue(table, column, value):
    add = f"insert into {table} ({column}) values (\"{value}\")"
    executequery(add)

def updatevalue(table, column, value, id):
    insert = f"update {table} set {column} = \"{value}\" where id = \"{id}\""
    executequery(insert)

class Filter(ABC):
    def __init__ (self, table, column, value):
        self.table = table
        self.column = column
        self.value = value

    def filterdata(self):
        try:
            conn = sql.connect("neocorp.db")
            curs = conn.cursor()

            if self.column:
                command = f"select {self.column} from {self.table}"
                if self.value:
                    command = f"select {self.column} from {self.table} where {self.value}"
            else:
                command = f"select *from {self.table}"
                if self.value:
                    command = f"select *from {self.table} where {self.value}"

            cursor = curs.execute(command)
            return cursor
        
        except sql.Error as err:
            print(f"Ошибка {err}")
        
    @abstractmethod
    def fetchdata(self):
        pass

class AllData(Filter):
    def __init__ (self, table, column=None, value=None):
        super().__init__(table, column, value)

    def fetchdata(self):
        try:
            curs = super().filterdata()
            rows = curs.fetchall()

        except sql.Error as err:
            print(f"Ошибка {err}")

        return rows

class SeveralData(Filter):
    def __init__(self, table, amount, column=None, value=None):
        super().__init__(table, column, value)
        self.amount = amount

    def fetchdata(self):
        try:
            curs = super().filterdata()
            rows = curs.fetchmany(self.amount)

        except sql.Error as err:
            print(f"Ошибка {err}")

        return rows

class OneData(Filter):
    def __init__(self, table, column=None, value=None):
        super().__init__(table, column, value)

    def fetchdata(self):
        try:
            curs = super().filterdata()
            row = curs.fetchone()

        except sql.Error as err:
            print(f"Ошибка {err}")

        return row

def corpuscreate(title, sp):
    empcorp = Corpus(title, sp)
    create3 = empcorp.createtable()
    executequery(create3)
    staffcorpdata = empcorp.insertinfo('corpus')
    executequery(staffcorpdata)

def authorize():
    surname = input("Введите вашу фамилию: ").capitalize()
    name = input("Введите ваше имя: ").capitalize() 
    middlename = input("Введите ваше отчество (если есть): ").capitalize()
    while(True):
        try:
            day = int(input("Введите дату вашего рождения.\nДень: "))
            if day > 0 and day < 31:
                break
            else:
                continue
        except:
            print("Введите число!")
            continue
    while(True):
        try:
            month = int(input("Месяц: "))
            if month > 0 and month < 13:
                break
            else:
                continue
        except:
            print("Введите число!")
            continue
    while(True):
        try:
            year = int(input("Год: "))
            if year > 1899 and year < 2024:
                break
            else:
                continue
        except:
            print("Введите число!")
            continue
    birthday = f"{day}.{month}.{year}"
    post = input("Введите вашу должность: ")
    while(True):
        try:
            salary = int(input("Введите вашу среднюю зарплату: "))
            break
        except:
            print("Введите число!")
            continue
    while(True):
        edutype = input("Вы получили ООО, СОО, СПО или ВО?: ").upper()
        if edutype == "СПО" or edutype == "ВО":
            edu = input("Название учебного заведения, в котором вы получили СПО или ВО: ").title()
            spec = input("Специальность: ")
            qual = input("Квалификация: ")
            break
        elif edutype == "ООО" or edutype == "СОО":
            edu = input("Название учебного заведения, в котором вы получили ООО или СОО: ").title()
            spec = '-'
            qual = '-'
            break
        else:
            continue

    main = "Главный корпус Корпорации Нео"
    mainsp = "Руководство, управление корпусами, проведение собеседований"

    med = "Ветеринарно-медицинский корпус"
    medsp = "Разработка лекарств, лечение людей и животных"

    tech = "Корпус информационных технологий"
    techsp = "Программирование аппаратных средств и ПО, создание и проектирование баз данных, разработка нейросетей"

    bio = "Биохимический корпус"
    biosp = "Новые открытия в области биохимии"

    geo = "Геологический корпус"
    geosp = "Новые открытия в области геологии, географии и археологии"

    cosmo = "Космический корпус"
    cosmosp = "Новые открытия в космической области, разработка технологий для исследования космоса"
    
    if not os.path.exists("neocorp.db"):
        
        corpuscreate(main, mainsp)

        corpuscreate(med, medsp)

        corpuscreate(tech, techsp)

        corpuscreate(bio, biosp)

        corpuscreate(geo, geosp)

        corpuscreate(cosmo, cosmosp)

        staff_in_corp()

    corp = input("Выберите корпус:\n1. Главный корпус Корпорации Нео\n2. Ветеринарно-медицинский корпус"\
                 "\n3. Корпус информационных технологий\n4. Биохимический корпус\n5. Геологический корпус\n6. Космический корпус\n")

    match corp:
        case '1':
            corpid = searchid('corpus', 'title', main)
            addvalue('staff_in_corp', 'corp_id', corpid)
        case '2':
            corpid = searchid('corpus', 'title', med)
            addvalue('staff_in_corp', 'corp_id', corpid)
        case '3':
            corpid = searchid('corpus', 'title', tech)
            addvalue('staff_in_corp', 'corp_id', corpid)
        case '4':
            corpid = searchid('corpus', 'title', bio)
            addvalue('staff_in_corp', 'corp_id', corpid)
        case '5':
            corpid = searchid('corpus', 'title', geo)
            print(corpid)
            addvalue('staff_in_corp', 'corp_id', corpid)
        case '6':
            corpid = searchid('corpus', 'title', cosmo)
            addvalue('staff_in_corp', 'corp_id', corpid)
    
    emp = Staff(surname, name, middlename, birthday)
    emppost = StaffPost(post, salary)
    empedu = Education(edu, spec, qual, edutype)
    
    create1 = emp.createtable()
    executequery(create1)

    create = emppost.createtable()
    executequery(create)

    create2 = empedu.createtable()
    executequery(create2)

    staffpostdata = emppost.insertinfo('staff_post')
    executequery(staffpostdata)
    
    staffdata = emp.insertinfo('staff')
    executequery(staffdata)
    postid = searchid('staff_post', 'post', post)
    idstaff = searchid('staff', 'surname', surname)
    updatevalue('staff', 'post_id', postid, idstaff)

    staffedudata = empedu.insertinfo('education')
    executequery(staffedudata)
    eduid = searchid('education', 'title', edu)
    updatevalue('staff', 'edu_id', eduid, idstaff)

    updatevalue('staff_in_corp', "staff_id", idstaff, idstaff)

def tablesoutput():
    while(True):
        tablenum = input()
        if tablenum == '1':
            tablename = 'staff_post'
            keys = StaffPost(post=None, salary=None).keys()
            break
        elif tablenum == '2':
            tablename = 'staff'
            keys = Staff(surname=None, firstname=None, middlename=None, birthday=None).keys()
            break
        elif tablenum == '3':
            tablename = 'education'
            keys = Education(title=None, speciality=None, qualification=None, typeofedu=None).keys()
            break
        elif tablenum == '4':
            tablename = 'corpus'
            keys = Corpus(title=None, speciality=None).keys()
            break
        elif tablenum == '5':
            tablename = 'staff_in_corp'
            keys = StaffInCorp(staff_id=None, corp_id=None).keys()
            break
        else:
            print("Такой таблицы не существует.")

    print(f"\nКлючи: {keys}")

    return tablename

def changedata():
    print("Какую таблицу изменить?\n1. staff_post\n2. staff\n3. education\n4. corpus\n5. staff_in_corp")
    table = tablesoutput()
    corpstaff = AllData(table)
    data = corpstaff.fetchdata()
    print(f"Значения: {data}")
    while(True):
        idnum = int(input("\nВыберите id (самая первая цифра из кортежей): "))
        if idnum > data.__len__():
            print("Такого id нет.")
        else:
            break
    col = input("Выберите колонку: ")
    val = input("Введите значение: ")
   
    updatevalue(table, col, val, idnum)

def extravalue():
    ins = input("Вводить дополнительное условие?\n").lower()
    if ins == 'yes' or ins == 'y' or ins == 'да' or ins == 'д':
        value = input("Введите условие: ")
        return value
    else:
        return None

def filtering(table, column=None):
    while(True):
        sort = input("Выберите сортировку:\n1. Выбрать несколько данных.\n2. Получить одну строку.\n3. Вывести все строки\n")
        if sort == '1':
            while(True):
                try:
                    num = int(input("Введите число: "))
                    break
                except:
                    print("Введите число!")
            try:
                valuesev = extravalue()
                sevdata = SeveralData(table, num, column, valuesev)
                items = sevdata.fetchdata()
                for item in items:
                    print(item)
                break
            except:
                print(f"Ошибка! Условие '{valuesev}' не является соответствующим.\n")
            break
        elif sort == '2':
            try:
                valueone = extravalue()
                dataone = OneData(table, column, valueone)
                item = dataone.fetchdata()
                print(item)
                break
            except:
                print(f"Ошибка! Условие '{valueone}' не является соответствующим.\n")
            break

        elif sort == '3':
            try:
                valueall = extravalue()
                alldata = AllData(table, column, valueall)
                allitems = alldata.fetchdata()
                for item in allitems:
                    print(item)
                break
            except:
                print(f"Ошибка! Условие '{valueall}' не является соответствующим.\n")
            break
        else:
            print("Такой опции нет.")
        break

def sortdata():
    print("Какую таблицу фильтровать?\n1. staff_post\n2. staff\n3. education\n4. corpus")
    table = tablesoutput()
    corpstaff = AllData(table)
    data = corpstaff.fetchdata()
    print(f"Значения: {data}")

    while(True):
        y = input("\nСортировать с колонкой или без? ").lower()
        if y == "с колонкой" or y == "с":
            column = input("Введите название колонки: ")
            filtering(table, column)
            break
        elif y == "без колонки" or y == "без":
            filtering(table)
            break
        else: 
            print("Что делать? Введите слово \"с\" или \"без\"")


whattodo = input("Добро пожаловать на информационную систему Корпорации Нео.\nЧто вы хотите сделать?"\
                 "\n1. Авторизоваться\n2. Изменить данные\n3. Фильровать данные\n4. Удалить данные\n")
print("------------------------------------------------------------------------")
match whattodo:
    case "1":  
        authorize()
    case "2":
        changedata()
    case "3":
        sortdata()
    case "4":
        print("Из какой таблицы удалить данные?\n1. staff_post\n2. staff\n3. education\n4. corpus\n5. staff_in_corp")
        table = tablesoutput()
        corpstaff = AllData(table)
        data = corpstaff.fetchdata()
        print(f"Значения: {data}")
        while(True):
            idnum = int(input("\nВведите id (самая первая цифра из кортежей): "))
            if idnum > data.__len__():
                print("Такого id нет.")
            else:
                break
        deletecolumn(table, idnum)