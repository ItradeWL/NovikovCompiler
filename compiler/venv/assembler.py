from parserr import Node, cons
from symboltable import t_storage, array, functions
from threeaddresscode import three_addr, check_float

f_list={}
def assembler(three_addr, array):

    check_while = False  # МЕТКА, ЧТОБЫ L0 ПРИ WHILE НЕ УВЕЛИЧИВАЛАСЬ ПОСЛЕ КАЖДОЙ ПРОВЕРКИ

    amount_skip = 0  # СЧЁТЧИК SKIP

    amount_if = 0 #СЧЁТЧИК IF

    amount_string = 0 #СЧЁТЧИК STRING

    data = ''

    f = open('product.s', 'w')
    data = data + '.data\n\ttrue: .byte 1\n\tfalse: .byte 0\n'
    f.write('.text\n')

    for i in range (len(t_storage)):

        if t_storage['t'+str(i)][0].isnumeric():
            t_storage['t'+str(i)]=[]
            t_storage['t' + str(i)] = 'integer'
            array['t' + str(i)] = []
            array['t' + str(i)] = 'integer'

        elif t_storage['t' + str(i)][0] in array and array[t_storage['t' + str(i)][0]][1] == 'real':
            t_storage['t' + str(i)] = []
            t_storage['t' + str(i)] = 'real'
            f_list['f' + str(i)] = []
            f_list['f' + str(i)].append('real')
            array['t' + str(i)] = []
            array['t' + str(i)] = 'real'

        elif t_storage['t'+str(i)][0] in array and array[t_storage['t'+str(i)][0]][1]=='integer':
            t_storage['t' + str(i)] = []
            t_storage['t' + str(i)] = 'integer'
            array['t' + str(i)] = []
            array['t' + str(i)] = 'integer'

        elif check_float(t_storage['t' + str(i)][0]):
            t_storage['t' + str(i)] = []
            t_storage['t' + str(i)] = 'real'
            f_list['f' + str(i)] = []
            f_list['f' + str(i)].append('real')
            array['t' + str(i)] = []
            array['t' + str(i)] = 'real'

        else:
            t_storage['t' + str(i)] = []
            t_storage['t' + str(i)] = 'integer'
            array['t' + str(i)] = []
            array['t' + str(i)] = 'integer'

    for force in (array):

        if force==('t0') :
            break
        t_storage[force]=[]
        t_storage[force].append(force)

    for mark in three_addr: #ОБХОД ПО МЕТКАМ MAIN, IF...
        f.write(mark + ':\n') #ЗАПИСЬ ТОГО, НА ЧТО НАТКНУЛСЯ

        for command in three_addr[mark]:
            array_variables_operations = command.split(' ') #РАЗДЕЛЕНИЕ СРОКИ С ОПЕРАЦИЕЙ И ПЕРЕМЕННОЙ В ТРЁХАДРЕСНОМ КОДЕ, ДЛЯ УДОБНОГО ОБРАЩЕНИЯ

            if ( array_variables_operations[0] == ':=' ): #ПОСТРОЧНО ОБХОДИТ ТРЁХАДРЕССНЫЙ КОД И ЕСЛИ ВСТРЕЧАЕТ ПРИСВАИВАНИЕ, ТО ПЕРЕВОДИТ ЕГО НА MIPS

                if array_variables_operations[1].isnumeric() and (array[array_variables_operations[2]][1] == 'integer' or t_storage[array_variables_operations[2]][0]=='i'):

                    if (array_variables_operations[2] in t_storage.keys() and t_storage[array_variables_operations[2]][0]!=array_variables_operations[2]):
                        f.write('\tli $' + array_variables_operations[2] + ', ' + array_variables_operations[1] + '\n')

                    else:
                        f.write('\tli $' + array[array_variables_operations[2]][0] + ', ' + array_variables_operations[1] + '\n')

                elif array_variables_operations[1].startswith('\"') and array_variables_operations[1].endswith('\"') and (array[array_variables_operations[2]][1] == 'string'):
                    data = data + '\t' + array_variables_operations[2] + ': .asciiz ' + array_variables_operations[1] +'\n'

                elif(array_variables_operations[1] in array.keys() ):

                    if (array_variables_operations[1] in t_storage.keys() and t_storage[array_variables_operations[1]][0]!=array_variables_operations[1]):

                        if (array_variables_operations[2] in t_storage.keys() and t_storage[array_variables_operations[2]][0]!=array_variables_operations[2]):

                            if t_storage[array_variables_operations[1]][0]=='r':

                                f.write('\tmov.s $f' +  array_variables_operations[2][1:] + ', $f' + array_variables_operations[1][1:] + '\n')

                            else:
                                f.write('\tmove $' + array_variables_operations[2] + ', $f' + array_variables_operations[1] + '\n')

                        elif array_variables_operations[2] in array.keys():

                            if t_storage[array_variables_operations[1]][0] == 'r':

                                f.write('\tmov.s $' + array[array_variables_operations[2]][0] + ', $f' + array_variables_operations[1][1:] + '\n')

                            else:
                                f.write('\tmove $' + array[array_variables_operations[2]][0] + ', $' + array_variables_operations[1] + '\n')

                    elif (array_variables_operations[1] in array.keys()):

                        if (array_variables_operations[2] in array.keys()):

                            if array[array_variables_operations[2]][1] =='real':
                                f.write('\tmov.s $' + array[array_variables_operations[2]][0] + ', $' + array[array_variables_operations[1]][0] + '\n')

                            else:
                                f.write('\tmove $' + array[array_variables_operations[2]][0] + ', $' + array[array_variables_operations[1]][0] + '\n')

                elif (check_float(array_variables_operations[1]) and (array[array_variables_operations[2]][1] == 'real' or t_storage[array_variables_operations[2]][0]=='r')):
                    data=data + '\tfraction'+ array_variables_operations[1] +': .float '+array_variables_operations[1]+'\n'

                    if (array_variables_operations[2] in t_storage.keys() and t_storage[array_variables_operations[2]][0]!=array_variables_operations[2]):
                        f.write('\tla $' + array_variables_operations[2] + ', fraction' + array_variables_operations[1] + '\n')

                    else:
                        f.write('\tli.s $' + array[array_variables_operations[2]][0] + ', ' + array_variables_operations[1] + '\n')

                else:

                    if (array_variables_operations[2] in array.keys()):
                        f.write('\tmove $' + array_variables_operations[2] + ', $' + array_variables_operations[1] + '\n')

                    elif (array_variables_operations[2] in array.keys()):
                        f.write('\tmove $' + array[array_variables_operations[2]][0] + ', $' + array_variables_operations[1] +'\n')

                    else:
                        f.write('\tmove $' + array_variables_operations[2] + ', $' + array_variables_operations[1] + '\n')

            elif (array_variables_operations[0] == '-'): #ОБХОД ДЛЯ ВЫЧИТАНИЯ

                if not(check_float(array_variables_operations[1]) or check_float(array_variables_operations[2])):

                        if(array_variables_operations[1].isnumeric() or array[array_variables_operations[1]][1]=='integer' or t_storage[array_variables_operations[1]][0]=='i') and (array_variables_operations[2].isnumeric() or array[array_variables_operations[2]][1]=='integer' or  t_storage[array_variables_operations[1]][0]=='i'):

                            if array_variables_operations[1].isnumeric():
                                f.write('\tli $t0, '+ array_variables_operations[1] + '\n')
                                argument1 = '$t0'

                                if array_variables_operations[2].isnumeric():
                                    f.write('\tli $t1, '+ array_variables_operations[2]+ '\n')
                                    argument2 = '$t1'
                                    f.write('\tsubu $'+ array_variables_operations[3] +', '+ argument1 + ', ' + argument2 + '\n')

                                elif(array_variables_operations[2] in array and array[array_variables_operations[2]][1]=='integer'):
                                    argument2 = '$'+array[array_variables_operations[2]][0]
                                    f.write('\tsubu $'+ array_variables_operations[3] +', ' + argument1 + ', ' + argument2 + '\n')

                                elif(t_storage[array_variables_operations[2]][0]=='i'):
                                    argument2 = '$'+array_variables_operations[2]
                                    f.write('\tsubu $' + array_variables_operations[3] + ', ' + argument1 + ', ' + argument2 + '\n')

                            elif((array_variables_operations[1] in array and array[array_variables_operations[1]][1]=='integer')or ( t_storage[array_variables_operations[1]][0]=='i' and array_variables_operations[1] in t_storage)):

                                if (array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'integer'):
                                    argument1 = '$' + array[array_variables_operations[1]][0]

                                else:
                                    argument1 = '$' + array_variables_operations[1]

                                if array_variables_operations[2].isnumeric():
                                    f.write('\tli $t1, '+ array_variables_operations[2]+ '\n')
                                    argument2 = '$t1'
                                    f.write('\tsubu $' + array_variables_operations[3] + ', ' + argument1 + ', ' + argument2 + '\n')

                                elif (array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'integer'):
                                    argument2 = '$' + array[array_variables_operations[2]][0]
                                    f.write('\tsubu $' + array_variables_operations[3] + ', ' + argument1 + ', ' + argument2 + '\n')

                                elif (t_storage[array_variables_operations[2]][0] == 'i' and array_variables_operations[2] in t_storage):
                                    argument2 = '$' + array_variables_operations[2]
                                    f.write('\tsubu $' + array_variables_operations[3] + ', ' + argument1 + ', ' + argument2 + '\n')

                        elif ((array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'real') or (
                                t_storage[array_variables_operations[1]][0] == 'r' and array_variables_operations[1] in t_storage)):

                            if (array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'real'):
                                argument1 = '$' + array[array_variables_operations[1]][0]

                            else:
                                argument1 = '$f' + array_variables_operations[1][1:]

                            if check_float(array_variables_operations[2]):
                                f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                                argument2 = '$f1'
                                f.write('\tsub.s $f' + array_variables_operations[3][1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                            elif (array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'real'):
                                argument2 = '$' + array[array_variables_operations[2]][0]
                                f.write('\tsub.s $f' + array_variables_operations[3][1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                            elif (t_storage[array_variables_operations[2]][0] == 'r' and array_variables_operations[2] in t_storage):
                                argument2 = '$f' + array_variables_operations[2][1:]
                                f.write('\tsub.s $f' + array_variables_operations[3][1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                        else:
                            print('ERROR WRONG TYPE')
                            return

                elif check_float(array_variables_operations[1]):

                    f.write('\tli.s $f0, ' + array_variables_operations[1] + '\n')
                    argument1 = '$f0'

                    if check_float(array_variables_operations[2]):
                        f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                        argument2 = '$f1'
                        f.write('\tsub.s $f'+ array_variables_operations[3][1:] +', ' + argument1 + ', ' + argument2 + '\n')

                    elif ((array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'real') or (t_storage[array_variables_operations[2]][0]=='r' and array_variables_operations[2] in t_storage)):

                        if (array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'real'):
                            argument2 = '$' + array[array_variables_operations[2]][0]

                        else:
                            argument2 = '$f' + array_variables_operations[2][1:]
                        f.write('\tsub.s $' + array_variables_operations[3][1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    else:
                        print('ERROR WRONG TYPE')
                        return

                else:
                    print('ERROR WRONG TYPE')
                    return


            elif (array_variables_operations[0] == '+'): # ОБХОД ДЛЯ СЛОЖЕНИЯ

                if not(check_float(array_variables_operations[1]) and check_float(array_variables_operations[2])):

                        if(array_variables_operations[1].isnumeric() or array[array_variables_operations[1]][1]=='integer' or t_storage[array_variables_operations[1]][0]=='i') and (array_variables_operations[2].isnumeric() or array[array_variables_operations[2]][1]=='integer' or t_storage[array_variables_operations[2]][0]=='i'):

                            if array_variables_operations[1].isnumeric():
                                f.write('\tli $t0, '+ array_variables_operations[1] + '\n')
                                argument1 = '$t0'

                                if array_variables_operations[2].isnumeric():
                                    f.write('\tli $t1, '+ array_variables_operations[2]+ '\n')
                                    argument2 = '$t1'
                                    f.write('\taddu $'+ array_variables_operations[3] +', '+ argument1 + ', ' + argument2 + '\n')

                                elif(array_variables_operations[2] in array and array[array_variables_operations[2]][1]=='integer'):
                                    argument2 = '$'+array[array_variables_operations[2]][0]
                                    f.write('\taddu $'+ array_variables_operations[3] +', ' + argument1 + ', ' + argument2 + '\n')

                                elif(t_storage[array_variables_operations[2]][0]=='i'):
                                    argument2 = '$'+array_variables_operations[2]
                                    f.write('\taddu $' + array_variables_operations[3] + ', ' + argument1 + ', ' + argument2 + '\n')

                            elif((array_variables_operations[1] in array and array[array_variables_operations[1]][1]=='integer' )or( t_storage[array_variables_operations[1]][0]=='i' and array_variables_operations[1] in t_storage)):

                                if (array_variables_operations[1] in array and array[array_variables_operations[1]][1]=='integer' ):
                                    argument1 = '$' + array[array_variables_operations[1]][0]

                                else:
                                    argument1 = '$' + array_variables_operations[1]

                                if array_variables_operations[2].isnumeric():
                                    f.write('\tli $t1, '+ array_variables_operations[2]+ '\n')
                                    argument2 = '$t1'
                                    f.write('\taddu $' + array_variables_operations[3] + ', ' + argument1 + ', ' + argument2 + '\n')

                                elif (array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'integer'):
                                    argument2 = '$' + array[array_variables_operations[2]][0]
                                    f.write('\taddu $' + array_variables_operations[3] + ', ' + argument1 + ', ' + argument2 + '\n')

                                elif( t_storage[array_variables_operations[2]][0]=='i' and array_variables_operations[2] in t_storage):
                                    argument2 = '$' + array_variables_operations[2]
                                    f.write('\taddu $' + array_variables_operations[3] + ', ' + argument1 + ', ' + argument2 + '\n')

                        elif ((array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'real') or (
                                t_storage[array_variables_operations[1]][0] == 'r' and array_variables_operations[1] in t_storage)):

                            if (array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'real'):
                                argument1 = '$' + array[array_variables_operations[1]][0]

                            else:
                                argument1 = '$f' + array_variables_operations[1][1:]

                            if check_float(array_variables_operations[2]):
                                f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                                argument2 = '$f1'
                                f.write('\tadd.s $f' + array_variables_operations[3][1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                            elif (array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'real'):
                                argument2 = '$' + array[array_variables_operations[2]][0]
                                f.write('\tadd.s $f' + array_variables_operations[3][1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                            elif (t_storage[array_variables_operations[2]][0] == 'r' and array_variables_operations[2] in t_storage):
                                argument2 = '$f' + array_variables_operations[2][1:]
                                f.write('\tadd.s $f' + array_variables_operations[3][1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                        else:
                            print('ERROR WRONG TYPE')
                            return

                elif check_float(array_variables_operations[1]):

                    f.write('\tli.s $f0, ' + array_variables_operations[1] + '\n')
                    argument1 = '$f0'

                    if check_float(array_variables_operations[2]):
                        f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                        argument2 = '$f1'
                        f.write('\tadd.s $f'+ array_variables_operations[3][1:] +', ' + argument1 + ', ' + argument2 + '\n')

                    elif ((array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'real') or ( t_storage[array_variables_operations[1]][0]=='r' and array_variables_operations[1] in t_storage)):

                        if (array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'real'):
                            argument2 = '$' + array[array_variables_operations[2]][0]

                        elif (t_storage[array_variables_operations[1]][0]=='r' and array_variables_operations[1] in t_storage):
                            argument2 = '$' + array_variables_operations[2]
                        f.write('\tadd.s $f' + array_variables_operations[3][1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    else:
                        print('ERROR WRONG TYPE')
                        return

                else:
                    print('ERROR WRONG TYPE')
                    return

            elif (array_variables_operations[0] == '*'): #ОБХОД ДЛЯ УМНОЖЕНИЯ

                if not (check_float(array_variables_operations[1]) or check_float(array_variables_operations[2])):

                    if (array_variables_operations[1].isnumeric() or array[array_variables_operations[1]][
                        1] == 'integer' or t_storage[array_variables_operations[1]][0] == 'i') and (
                            array_variables_operations[2].isnumeric() or array[array_variables_operations[2]][
                        1] == 'integer' or t_storage[array_variables_operations[2]][0] == 'i'):

                        if array_variables_operations[1].isnumeric():
                            f.write('\tli $t0, ' + array_variables_operations[1] + '\n')
                            argument1 = '$t0'

                            if array_variables_operations[2].isnumeric():
                                f.write('\tli $t1, ' + array_variables_operations[2] + '\n')
                                argument2 = '$t1'
                                f.write('\tmult ' + argument1 + ', ' + argument2 + '\n')

                            elif (array_variables_operations[2] in array and array[array_variables_operations[2]][
                                1] == 'integer'):
                                argument2 = '$' + array[array_variables_operations[2]][0]
                                f.write('\tmult ' + argument1 + ', ' + argument2 + '\n')

                            elif (t_storage[array_variables_operations[2]][0] == 'i'):
                                argument2 = '$' + array_variables_operations[2]
                                f.write('\tmult ' + argument1 + ', ' + argument2 + '\n')

                        elif ((array_variables_operations[1] in array and array[array_variables_operations[1]][
                            1] == 'integer') or (
                                      t_storage[array_variables_operations[1]][0] == 'i' and array_variables_operations[
                                  1] in t_storage)):

                            if (array_variables_operations[1] in array and array[array_variables_operations[1]][
                                1] == 'integer'):
                                argument1 = '$' + array[array_variables_operations[1]][0]

                            else:
                                argument1 = '$' + array_variables_operations[1]

                            if array_variables_operations[2].isnumeric():
                                f.write('\tli $t1, ' + array_variables_operations[2] + '\n')
                                argument2 = '$t1'
                                f.write('\tmult ' + argument1 + ', ' + argument2 + '\n')

                            elif (array_variables_operations[2] in array and array[array_variables_operations[2]][
                                1] == 'integer'):

                                argument2 = '$' + array[array_variables_operations[2]][0]
                                f.write('\tmult ' + argument1 + ', ' + argument2 + '\n')

                            elif (t_storage[array_variables_operations[2]][0] == 'i' and array_variables_operations[
                                2] in t_storage):
                                argument2 = '$' + array_variables_operations[2]
                                f.write('\tmult ' + argument1 + ', ' + argument2 + '\n')
                            f.write('\tmflo $' + array_variables_operations[3] + '\n')

                    elif ((array_variables_operations[1] in array and array[array_variables_operations[1]][
                        1] == 'real') or (
                                  t_storage[array_variables_operations[1]][0] == 'r' and array_variables_operations[
                              1] in t_storage)):

                        if (array_variables_operations[1] in array and array[array_variables_operations[1]][
                            1] == 'real'):
                            argument1 = '$' + array[array_variables_operations[1]][0]

                        else:
                            number = array_variables_operations[1][1:]
                            argument1 = '$f' + str(number)

                        if check_float(array_variables_operations[2]):
                            f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                            argument2 = '$f1'
                            f.write('\tmul.s $f' + array_variables_operations[3][
                                                   1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                        elif (array_variables_operations[2] in array and array[array_variables_operations[2]][
                            1] == 'real'):
                            argument2 = '$' + array[array_variables_operations[2]][0]
                            number = array_variables_operations[3][1:]

                            f.write('\tmul.s $f' + str(number) + ', ' + argument1 + ', ' + argument2 + '\n')

                        elif (t_storage[array_variables_operations[2]][0] == 'r' and array_variables_operations[
                            2] in t_storage):
                            number = array_variables_operations[2][1:]
                            argument2 = '$f' + str(number)
                            f.write('\tmul.s $f' + array_variables_operations[3][
                                                   1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                        else:
                            print('ERROR WRONG TYPE')
                            return

                elif check_float(array_variables_operations[1]):

                    f.write('\tli.s $f0, ' + array_variables_operations[1] + '\n')
                    argument1 = '$f0'

                    if check_float(array_variables_operations[2]):
                        f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                        argument2 = '$f1'
                        f.write('\tmul.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    elif (array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'real'):
                        argument2 = '$' + array[array_variables_operations[2]][0]
                        f.write('\tmul.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    elif (t_storage[array_variables_operations[2]][0] == 'r' and array_variables_operations[
                        2] in t_storage):
                        number = array_variables_operations[2][1:]
                        argument2 = '$f' + str(number)
                        f.write('\tmul.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    else:
                        print('ERROR WRONG TYPE')
                        return

            elif (array_variables_operations[0] == '/'): #ОБХОД ДЛЯ ДЕЛЕНИЯ

                if not (check_float(array_variables_operations[1]) or check_float(array_variables_operations[2])):

                    if (array_variables_operations[1].isnumeric() or array[array_variables_operations[1]][
                        1] == 'integer' or t_storage[array_variables_operations[1]][0] == 'i') and (
                            array_variables_operations[2].isnumeric() or array[array_variables_operations[2]][
                        1] == 'integer' or t_storage[array_variables_operations[1]][0] == 'i'):

                        if array_variables_operations[1].isnumeric():
                            f.write('\tli $t0, ' + array_variables_operations[1] + '\n')
                            argument1 = '$t0'

                            if array_variables_operations[2].isnumeric():
                                f.write('\tli $t1, ' + array_variables_operations[2] + '\n')
                                argument2 = '$t1'
                                f.write('\tdiv ' + argument1 + ', ' + argument2 + '\n')

                            elif (array_variables_operations[2] in array and array[array_variables_operations[2]][
                                1] == 'integer'):
                                argument2 = '$' + array[array_variables_operations[2]][0]
                                f.write('\tdiv ' + argument1 + ', ' + argument2 + '\n')

                            elif (t_storage[array_variables_operations[2]][0] == 'i'):
                                argument2 = '$' + array_variables_operations[2]
                                f.write('\tdiv ' + argument1 + ', ' + argument2 + '\n')

                        elif ((array_variables_operations[1] in array and array[array_variables_operations[1]][
                            1] == 'integer') or (
                                      t_storage[array_variables_operations[1]][0] == 'i' and array_variables_operations[
                                  1] in t_storage)):

                            if (array_variables_operations[1] in array and array[array_variables_operations[1]][
                                1] == 'integer'):
                                argument1 = '$' + array[array_variables_operations[1]][0]

                            else:
                                argument1 = '$' + array_variables_operations[1]

                            if array_variables_operations[2].isnumeric():
                                f.write('\tli $t1, ' + array_variables_operations[2] + '\n')
                                argument2 = '$t1'
                                f.write('\tdiv ' + argument1 + ', ' + argument2 + '\n')

                            elif (array_variables_operations[2] in array and array[array_variables_operations[2]][
                                1] == 'integer'):
                                argument2 = '$' + array[array_variables_operations[2]][0]
                                f.write('\tdiv ' + argument1 + ', ' + argument2 + '\n')

                            elif (t_storage[array_variables_operations[2]][0] == 'i' and array_variables_operations[
                                2] in t_storage):
                                argument2 = '$' + array_variables_operations[2]
                                f.write('\tdiv ' + argument1 + ', ' + argument2 + '\n')
                        f.write('\tmflo $' + array_variables_operations[3] + '\n')

                    elif ((array_variables_operations[1] in array and array[array_variables_operations[1]][
                        1] == 'real') or (
                                  t_storage[array_variables_operations[1]][0] == 'r' and array_variables_operations[
                              1] in t_storage)):

                        if (array_variables_operations[1] in array and array[array_variables_operations[1]][
                            1] == 'real'):
                            argument1 = '$' + array[array_variables_operations[1]][0]

                        else:
                            argument1 = '$f' + array_variables_operations[1][1:]

                        if check_float(array_variables_operations[2]):
                            f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                            argument2 = '$f1'
                            f.write('\tdiv.s $f' + array_variables_operations[3][
                                                   1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                        elif (array_variables_operations[2] in array and array[array_variables_operations[2]][
                            1] == 'real'):
                            argument2 = '$' + array[array_variables_operations[2]][0]
                            f.write('\tdiv.s $f' + array_variables_operations[3][
                                                   1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                        elif (t_storage[array_variables_operations[2]][0] == 'r' and array_variables_operations[
                            2] in t_storage):
                            argument2 = '$f' + array_variables_operations[2][1:]
                            f.write('\tdiv.s $f' + array_variables_operations[3][
                                                   1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    else:
                        print('ERROR WRONG TYPE')
                        return


                elif check_float(array_variables_operations[1]):

                    f.write('\tli.s $f0, ' + array_variables_operations[1] + '\n')
                    argument1 = '$f0'

                    if check_float(array_variables_operations[2]):
                        f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                        argument2 = '$f1'
                        f.write('\tdiv.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    elif (array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'real'):
                        argument2 = '$' + array[array_variables_operations[2]][0]
                        f.write('\tdiv.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    elif (t_storage[array_variables_operations[2]][0] == 'r' and array_variables_operations[
                        2] in t_storage):
                        argument2 = '$f' + array_variables_operations[2][1:]
                        f.write('\tdiv.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    else:
                        print('ERROR WRONG TYPE')
                        return

                elif ((array_variables_operations[1] in array and array[array_variables_operations[1]][
                    1] == 'real') or (t_storage[array_variables_operations[1]][0] == 'r' and array_variables_operations[
                    1] in t_storage)):
                    if (array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'real'):
                        argument1 = '$' + array[array_variables_operations[1]][0]

                    else:
                        argument1 = '$f' + array_variables_operations[1][1:]

                    if check_float(array_variables_operations[2]):
                        f.write('\tli.s $f1, ' + array_variables_operations[2] + '\n')
                        argument2 = '$f1'
                        f.write('\tdiv.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    elif (array_variables_operations[2] in array and array[array_variables_operations[2]][1] == 'real'):
                        argument2 = '$' + array[array_variables_operations[2]][0]
                        f.write('\tdiv.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                    elif (t_storage[array_variables_operations[2]][0] == 'r' and array_variables_operations[
                        2] in t_storage):
                        argument2 = '$f' + array_variables_operations[2][1:]
                        f.write('\tdiv.s $f' + array_variables_operations[3][
                                               1:] + ', ' + argument1 + ', ' + argument2 + '\n')

                else:
                    print('ERROR WRONG TYPE')
                    return

            elif (array_variables_operations[0] == '<' or array_variables_operations[0] == '>'
                    or array_variables_operations[0] == '='): #ОБХОД ДЛЯ БОЛЬШЕ, МЕНЬШЕ, РАВНО

                if check_while == False:
                    L = 'L' + str(amount_if)
                    amount_if = amount_if + 1
                    check_while = True
                    f.write(L + ':\n')

                if array_variables_operations[0] == '<':
                    f.write('\tla $' + array_variables_operations[3] + ', false\n')
                    f.write('\tbge $' + array[array_variables_operations[1]][0] + ', $' + array[array_variables_operations[2]][0] + ', SKIP'+str(amount_skip) + '\n')
                    f.write('\tla $' + array_variables_operations[3] + ', true\n')
                    f.write('SKIP'+str(amount_skip) + ':\n')
                    amount_skip = amount_skip + 1

                elif array_variables_operations[0] == '>':
                    f.write('\tla $' + array_variables_operations[3] + ', false\n')
                    f.write('\tble $' + array[array_variables_operations[1]][0] + ', $' + array[array_variables_operations[2]][0] + ', SKIP'+str(amount_skip) + '\n')
                    f.write('\tla $' + array_variables_operations[3] + ', true\n')
                    f.write('SKIP'+str(amount_skip) + ':\n')
                    amount_skip = amount_skip + 1

                elif array_variables_operations[0] == '=':
                    f.write('\tla $' + array_variables_operations[3] + ', false\n')
                    f.write('\tbne $' + array[array_variables_operations[1]][0] + ', $' + array[array_variables_operations[2]][0] + ', SKIP'+str(amount_skip) + '\n')
                    f.write('\tla $' + array_variables_operations[3] + ', true\n')
                    f.write('SKIP'+str(amount_skip) + ':\n')
                    amount_skip = amount_skip + 1

            elif (array_variables_operations[0] == 'and' or array_variables_operations[0] == 'or'):
                f.write('\t' + array_variables_operations[0] + ' $' + array_variables_operations[3] + ', $' + array_variables_operations[1] + ', $' + array_variables_operations[2] + '\n')

            elif (array_variables_operations[0] == 'not'):
                index = array_variables_operations[2][1:]
                index = int(index) + 1
                temp = 't' + str(index)
                f.write('\tla $' + temp + ' false\n')
                f.write('\tnor $' + array_variables_operations[2] + ', $' + array_variables_operations[1] + ', $' + temp + '\n')

            elif (array_variables_operations[0] == 'IF'):
                check_while = False
                index = array_variables_operations[1][1:]
                index = int(index) + 1
                temp = 't' + str(index)
                f.write('\tla $' + temp + ', true\n')
                f.write('\tbeq $' + temp + ', $' + array_variables_operations[1] + ', ' + array_variables_operations[3] + '\n')
                f.write('L' + str(amount_if) + ':\n')
                amount_if = amount_if + 1

            elif (array_variables_operations[0] == 'goto'):

                if (array_variables_operations[1] == 'after_if'):
                    f.write('\tj L' + str(amount_if - 1) + '\n')

                elif (array_variables_operations[1] == 'start_if'):
                    f.write('\tj L' + str(amount_if - 2) + '\n')

                else:
                    f.write('\tj ' + array_variables_operations[1] + '\n')

            elif (array_variables_operations[0] == 'break'):
                f.write('\tj L' + str(amount_if - 3) + '\n')

            elif (array_variables_operations[0] == 'continue'):
                f.write('\tj L' + str(amount_if - 4) + '\n')

            elif (array_variables_operations[0] == 'return'):
                f.write('\tmove $t9, $' + array_variables_operations[1] + '\n' )
                f.write('\tjr $ra\n')

            elif (array_variables_operations[0] == 'Call'):
                args = array_variables_operations[2:len(array_variables_operations)-1]
                for i in range(len(args)):
                    f.write('\tmove $a' + str(i) + ', $' + array[args[i]][0] + '\n')
                f.write('\tjal ' + array_variables_operations[1] + '\n')
                f.write('\tmove $' + array_variables_operations[len(array_variables_operations)-1] + ', $t9\n')

            elif (array_variables_operations[0] == 'write'):

                if (array_variables_operations[1].startswith('\"') and array_variables_operations[1].endswith('\"')):
                    data=data +'\tstring'+str(amount_string) + ': .asciiz '+array_variables_operations[1]+'\n'
                    amount_string = amount_string+1
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, '+'string'+str(amount_string-1)+'\n')
                    f.write('\tsyscall\n')

                elif (array_variables_operations[1].isnumeric()):
                    f.write('\tli $v0, 1\n')
                    f.write('\tla $a0, '+array_variables_operations[1] + '\n')
                    f.write('\tsyscall\n')
                    data = data + '\tstrZero' + r': .asciiz "\n"'  + '\n'
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, ' + 'strZero' + '\n')
                    f.write('\tsyscall\n')

                elif (check_float(array_variables_operations[1])):
                    data=data+'\tfraction'+ array_variables_operations[1] +': .float '+array_variables_operations[1]+'\n'
                    f.write('\tli $v0, 2\n')
                    f.write('\tli.s $f12, ' + array_variables_operations[1] + '\n')
                    f.write('\tsyscall\n')

                elif (array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'string'):
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, ' + array_variables_operations[1] + '\n')
                    f.write('\tsyscall\n')

                elif (array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'integer'):
                    f.write('\tli $v0, 1\n')
                    f.write('\tla $a0, ' + '($' + array[array_variables_operations[1]][0] + ')\n')
                    f.write('\tsyscall\n')
                    data = data + '\tstrZero' + r': .asciiz "\n"' + " " + '\n'
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, ' + 'strZero' + '\n')
                    f.write('\tsyscall\n')

                elif (array_variables_operations[1] in array and array[array_variables_operations[1]][1] == 'real'):
                    f.write('\tli $v0, 2\n')
                    f.write('\tmov.s $f12, $' + array[array_variables_operations[1]][0] + '\n')
                    f.write('\tsyscall\n')


    f.write('END:\n')
    f.write(data)
    f.close()

assembler(three_addr, array)
