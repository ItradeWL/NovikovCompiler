from parserr import Node, cons

array = []
t_storage = {} #СЛОВАРЬ ВРЕМЕННЫХ ПЕРЕМЕННЫХ, ДЛЯ ПРОВЕРКИ ТИПА ВРЕМЕННОЙ ПЕРЕМЕННОЙ, ПРИ ВЫПОЛНЕНИИ ОПЕРАЦИЙ
functions = []
                #ОБХОД ДЕРЕВА ДЛЯ СОСТАВЛЕНИЯ ТАБЛИЦЫ СИМВОЛОВ
def detour(cons): #РЕКУРСИВНЫЙ ОБХОД ДЛЯ ЗАПИСИ ПЕРЕМЕННЫХ С ОБЛАСТЬЮ ВИДИМОСТИ И ИХ ТИПАМИ

    if (type(cons) != Node):
        return

    elif (cons.type == 'dec'):
        for i in cons.section[0].section:
            array.append((i, cons.section[1].section[0], 'main'))
        return

    elif (cons.type == 'FUNCTION'): #ЕСЛИ ВСТРЕЧАЕТСЯ, ТО ЗАПУСКАЕТСЯ ОБХОД function_traversal ДЛЯ КАЖДОЙ ФУНКЦИИ
        for j in cons.section:
            if (len(j.section) == 2):
                function_traversal(j, j.type)
                functions.append(j.type)
            elif (len(j.section) == 3):
                functions.append(j.type)
                for l in j.section:
                    function_traversal(l, j.type)

    else:
        for i in range(len(cons.section)):
            detour(cons.section[i])

def function_traversal(cons, fun): #ОБХОД КОНКРЕТНОЙ ФУНКЦИИ

    if (type(cons) != Node):
        return

    elif (cons.type == 'dec'):
        for i in cons.section[0].section:
            array.append((i, cons.section[1].section[0], fun))

    else:
        for i in range(len(cons.section)):
            function_traversal(cons.section[i], fun)

detour(cons)


def change_array(array): #ПРИВЕДЕНИЕ ТАБЛИЦЫ В ВИД СЛОВАРЯ
    variable_dictionarys = {} #СЛОВАРЬ С КЛЮЧОМ=НАЗВАНИЮ ПЕРЕМЕННОЙ, ХРАНИТ, ПОМИМО ТИПА И ОБЛАСТИ ВИДИМОСТИ, РЕГИСТРЫ ДЛЯ АССЕМБЛЕРА (s0.s1...)
    index = 0
    variable_dictionarya = {}
    track_visability='main'

    for i in array:
        variable_dictionarys[i[0]] = []
        variable_dictionarys[i[0]].append('s' + str(index))
        variable_dictionarys[i[0]].append(i[1])
        variable_dictionarys[i[0]].append(i[2])
        index = index + 1
    index = 0
    counter_for_functions=0

    for i in variable_dictionarys:
        variable_dictionarya[i[0]] = []
        if variable_dictionarys[i][2] != 'main':
            if track_visability != variable_dictionarys[i][2]:
                track_visability = variable_dictionarys[i][2]
                counter_for_functions=0
            track_visability = variable_dictionarys[i][2]
            variable_dictionarya[i[0]].append('a' + str(counter_for_functions))
            counter_for_functions=counter_for_functions+1
            variable_dictionarya[i[0]].append(variable_dictionarys[i][1])
            variable_dictionarya[i[0]].append(variable_dictionarys[i][2])

        else:
            if variable_dictionarys[i][1]=='integer' or variable_dictionarys[i][1]=='string':
                variable_dictionarya[i[0]].append('s' + str(index))

            else:
                variable_dictionarya[i[0]].append('f1' + str(index))
            index=index+1
            variable_dictionarya[i[0]].append(variable_dictionarys[i][1])
            variable_dictionarya[i[0]].append(variable_dictionarys[i][2])

    return variable_dictionarya

array = change_array(array)
for key in array:
    print(key + ' : ')
    for i in array[key]:
        print('\t' + str(i))