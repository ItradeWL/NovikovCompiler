from parserr import Node, cons
from symboltable import t_storage, array, functions

branch = cons
three_addr = {'main': []}
temporary_variable = 0 #СЧЁТЧИК ВРЕМЕННЫХ ПЕРЕМЕННЫХ
amount_if = 0 #СЧЁТЧИК IF


def control_visibility(branch, area): #ПРОВЕРКА НА ОБЛАСТЬ ВИДМИМОСТИ
    if area.startswith('if') or (branch.isnumeric()) or (check_float(branch)): #isnumeric - int
        return True                                                          #check_float - float

    if (branch in array.keys()):
        if (array[branch][2] == area): #ПРОВЕРКА НАХОДИТСЯ ЛИ ПЕРЕМЕННАЯ В ОБЛАСТЕ ВИДИМОСТИ
            return True

        else:
            print('SCOPE ERROR') #ОШИБКА, ЕСЛИ ПЕРЕМЕННАЯ НЕ НАХОДИТСЯ В ОБЛАСТИ ВИДИМОСТИ
            print(branch + ' ' + area)
            return False

    else:
        print('VARIABLE IS NOT CORRECT ' + branch + ' ' + area) #ПЕРЕМЕННАЯ В ЦЕЛОМ УКАЗАНА НЕ ВЕРНО
        return False

def general_detour(tree):

    if len(tree.section) == 3: # ПРОВЕРКА НАЛИЧИЯ VAR, FUNCTION и statement
        three_addr_detour(tree.section[0], 'main') #СНАЧАЛА ПРОИСХОДИТ ОБХОД VAR и statement, ПОСЛЕ FUNCTION
        three_addr_detour(tree.section[2], 'main') #main - НАЗВАНИЕ ОБЛАСТИ ВИДИМОСТИ
        for funct in tree.section[1].section:
            three_addr[funct.type] = []
            three_addr_detour(funct, funct.type)
    else:
        three_addr_detour(tree.section[0], 'main')
        three_addr_detour(tree.section[1], 'main')
    three_addr['main'].append('goto END')

def three_addr_detour(branch, area):

    global temporary_variable, amount_if
    if (type(branch) != Node and (branch == 'break' or branch == 'continue')):
        three_addr[area].append(branch) # ЗАПИСЬ break или continue ПРИ ВСТРЕЧЕ ИХ В КОНЕЧНОМ ЛИСТЕ

    elif (type(branch) != Node):
        return

    elif (branch.type == 'WRITE'): #ЗАПИСЬ ПРИ ВСТРЕЧЕ PRINT
        three_addr[area].append('write ' + branch.section[0])

    elif (branch.type == 'if'): #ЗАПИСЬ ПРИ ВСТРЕЧЕ IF
        treatment_detour(branch.section[0], area) #ОБРАБОТКА ЛОГИЧЕСКОГО ВЫРАЖЕНИЯ
        if_area = 'if'+str(amount_if) #ПРОВЕРКА, КАКОЙ ПО СЧЁТУ ВСТРЕТИЛСЯ IF
        amount_if = amount_if + 1
        three_addr[if_area] = []
        three_addr[area].append('IF ' + 't' + str(temporary_variable - 1) + ' goto ' + if_area)
        three_addr_detour(branch.section[1], if_area) #ЗАПИСЬ СОДЕРЖИМОГО В ТЕЛЕ IF
        three_addr[if_area].append('goto after_if') #ВОЗВРАЩЕНИЕ НА СТРОКУ, КОТОРАЯ ИДЁТ ПОСЛЕ IF

    elif (branch.type == 'while'):  # ЗАПИСЬ ПРИ ВСТРЕЧЕ WHILE
        treatment_detour(branch.section[0], area)
        if_area = 'if' + str(amount_if)
        amount_if = amount_if + 1
        three_addr[if_area] = []
        three_addr[area].append('IF ' + 't' + str(temporary_variable - 1) + ' goto ' + if_area)
        three_addr_detour(branch.section[1], if_area)
        three_addr[if_area].append(
            'goto start_if')  # ВОЗВРАЩЕНИЕ НА СТРОКУ С WHILE, ДЛЯ ПРОВЕРКИ ВЫПОЛНИЛОСЬ ЛИ УСЛОВИЕ

    elif (branch.type == 'dec'):  #ЗАПИСЬ ПЕРЕМЕННЫХ ПРИ ВСТРЕЧЕ ИХ В КОНЕЧНОМ ЛИСТЕ В DEC
        for i in branch.section[0].section:
            three_addr[area].append(i)

    elif (branch.type == 'assign'): #ЗАПИСЬ ПРИ ВСТРЕЧЕ ПРИСВАИВАНИЯ С ПРОВЕРКОЙ НА ОБЛАСТЬ ВИДИМОСТИ И ТИП ПЕРЕМЕННОЙ
        if (type(branch.section[0]) == str and type(branch.section[1]) == str):
            if (not control_visibility(branch.section[0], area)):
                return
            three_addr[area].append(':= ' + branch.section[1] + ' ' + branch.section[0])

        else:
            three_addr_assign(branch, area)
            if (not control_visibility(branch.section[0], area)):
                return
            three_addr[area].append(':= '+'t'+str(temporary_variable-1)+ ' '+branch.section[0])

            t_storage['t'+str(temporary_variable-1)]=[]
            t_storage['t'+str(temporary_variable-1)].append(branch.section[0])

            temporary_variable = 0

    elif (branch.type == 'return'): #ЗАПИСЬ ПРИ ВСТРЕЧЕ RETUTN
        if (area == 'main'): #ПРОВЕРКА НАХОДИТСЯ ЛИ RETURN В ФУНКЦИИ
            print('ERROR: RETURN IS NOT IN FUNCTION')
        else:
            three_addr_assign(branch.section[0],area)
            three_addr[area].append('return ' + 't'+str(temporary_variable-1))

    else: #ЕСЛИ НИЧЕГО НЕ ВСТРЕТИЛОСЬ, ТО УХОД В ГЛУБИНУ ДЕРЕВА НА 1 УРОВЕНЬ И ПОВТОРЕНИЕ ВСЕГО, ЧТО ВЫШЕ
        for i in range(len(branch.section)):
            three_addr_detour(branch.section[i], area)

def three_addr_assign(branch, area): #ОБРАБОТКА ВЫРАЖЕНИЯ ПРИ ПРИСВАИВАНИИ
    global temporary_variable

    if type(branch) != Node:
        if (not control_visibility(branch, area)): # ПРОВЕРКА ОБЛАСТИ ВИДИМОСТИ
            return
        return branch #ВОЗВРАЩЕНИЕ САМОГО ЗНАЧЕНИЯ, ЕСЛИ ОТСУТСТВУЕТ ВЫРАЖЕНИЕ ПРИ ПРИСВАИВАНИИ

    elif(branch.type == '*' or branch.type == '/' or branch.type == '+' or branch.type == '-'):
        operation = branch.type #ВЫТАСКИВАЕМ САМУ ОПЕРАЦИЮ (+, -, /, *)
        argument1 = three_addr_assign(branch.section[0], area) #РЕКУРСИВНЫЙ ВЫЗОВ САМОГО СЕБЯ, ЧТОБЫ В ИТОГЕ ПРИЙТИ К type(branch) != Node
        argument2 = three_addr_assign(branch.section[1], area)

        if argument1 == None and argument2 == None: #ЕСЛИ ВСТРЕЧАЕТСЯ НЕ ПЕРЕМЕННАЯ, А ЗНАЧЕНИЕ, ТО ПЕРЕДЕЛЫВАЕМ ВО ВРЕМЕННУЮ ПЕРЕМЕННУЮ
            argument1 = 't' + str(temporary_variable - 2)
            t_storage['t'+str(temporary_variable-2)]=[]
            t_storage['t' + str(temporary_variable - 1)] = []
            t_storage['t'+str(temporary_variable-2)].append('t' + str(temporary_variable - 1))
            t_storage['t'+str(temporary_variable-1)].append('t' + str(temporary_variable - 2))

        if argument1 == None:
            argument1 = 't'+str(temporary_variable-1)
            t_storage['t'+str(temporary_variable-1)]=[]
            t_storage['t'+str(temporary_variable-1)].append(argument2)

        if argument2 == None:
            argument2 = 't'+str(temporary_variable-1)
            t_storage['t'+str(temporary_variable-1)].append(argument1)

        else:
            t_storage['t'+str(temporary_variable)] = []
            t_storage['t'+str(temporary_variable)].append(argument1)
        temp = 't'+str(temporary_variable)
        temporary_variable = temporary_variable+1
        three_addr[area].append(str(operation) + ' ' + str(argument1) + ' ' + str(argument2) + ' ' + str(temp))

    elif (branch.type in functions):
        string = 'Call ' + branch.type + ' '
        for arg in branch.section[0].section:
            string = string + arg + ' '
        temp = 't' + str(temporary_variable)
        temporary_variable = temporary_variable + 1
        string = string + temp
        three_addr[area].append(string)

    else:
        for i in range(len(branch.section)):
            three_addr_assign(branch.section[i], area)

def treatment_detour(branch, area):
    global temporary_variable

    if type(branch) != Node:
        if (not control_visibility(branch, area)):
            return
        return branch

    elif(branch.type == 'and' or branch.type == 'or'): #ДЛЯ ЛОГИЧЕСИХ ОПЕРАЦИЙ С ДВУМЯ ПЕРЕМЕННЫМИ
        operation = branch.type
        argument1 = treatment_detour(branch.section[0], area)
        argument2 = treatment_detour(branch.section[1], area)

        if argument1 == None and argument2 == None:
            argument1 = 't' + str(temporary_variable - 2)
            argument2 = 't' + str(temporary_variable - 1)

        if argument1 == None:
            argument1 = 't'+str(temporary_variable-1)
            t_storage['t' + str(temporary_variable - 1)].append(argument2)

        if argument2 == None:
            argument2 = 't'+str(temporary_variable-1)
            t_storage['t' + str(temporary_variable - 1)].append(argument1)
        temp = 't'+str(temporary_variable)

        if not(temp in t_storage):
            t_storage[temp]=[]
            t_storage['t' + str(temporary_variable)].append(argument1)
        temporary_variable = temporary_variable+1
        three_addr[area].append(str(operation) + ' ' + str(argument1) + ' ' + str(argument2) + ' ' + str(temp))

    elif (branch.type == 'not'): #ДЛЯ ЛОГИЧЕСКОЙ ОПЕРАЦИИ С ОДНОЙ ПЕРЕМЕННОЙ
        operation = branch.type
        treatment_detour(branch.section[0], area)
        arg = 't'+str(temporary_variable-1)
        temp = 't' + str(temporary_variable)
        temporary_variable = temporary_variable + 1
        three_addr[area].append(str(operation) + ' ' + str(arg) + ' ' + str(temp))

    elif (branch.type == '>' or branch.type == '<' or branch.type == '='): #ДЛЯ ОПЕРАЦИЙ БОЛЬШЕ, МЕНЬШЕ, РАВНО
        operation = branch.type
        argument1 = three_addr_assign(branch.section[0], area)
        argument2 = three_addr_assign(branch.section[1], area)
        temp = 't' + str(temporary_variable)

        t_storage[temp]=[]
        t_storage[temp].append(argument1)
        temporary_variable = temporary_variable + 1
        three_addr[area].append(str(operation) + ' ' + str(argument1) + ' ' + str(argument2) + ' ' + str(temp))

    else:
        for i in range(len(branch.section)):
            treatment_detour(branch.section[i], area)

def check_float(string): #ПРОВРЕРКА ТИПА ПЕРЕМЕННОЙ
    try:
        float(string)
        if (string.isnumeric()):
            return False
        return True
    except ValueError:
        return False

general_detour(branch) #ВЫВОД РЕЗУЛЬТАТА
for key in three_addr:
    print(key + ' : ')
    for i in three_addr[key]:
        print('\t' + str(i))

