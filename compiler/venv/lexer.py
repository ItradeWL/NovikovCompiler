from ply import lex

reserved = {                            #Зарезервированные слова
        'integer': 'INTEGER',
        'real': 'REAL',
        'string': 'STRING',

        'var': 'VAR',
        'function': 'FUNCTION',
        'begin': 'BEGIN',
        'end': 'END',

        'and':'AND',
        'or': 'OR',
        'not': 'NOT',

        'if': 'IF',
        'while': 'WHILE',
        'do': 'DO',
        'then': 'THEN',
        'else': 'ELSE',

        'return':'RETURN',
        'write':'WRITE',
        'break':'BREAK',
        'continue':'CONTINUE'
}

tokens = list(reserved.values()) + [
        'VARIABLE',  # ПЕРЕМЕННАЯ

        'NUMBER_INTEGER',  # INT ЧИСЛА
        'NUMBER_REAL',  # REAL ЧИСЛА

        'SUM',  # СЛОЖЕНИЕ
        'SUB',  # ВЫЧИТАНИЕ
        'MUL',  # УМНОЖЕНИЕ
        'DIV',  # ДЕЛЕНИЕ

        'EQUALLY', # РАВНО
        'MORE',  # БОЛЬШЕ
        'LESS',  # МЕНЬШЕ
        'ASSIGNMENT',  # ПРИСВАИВАНИЕ

        'COMMA',  # ЗАПЯТАЯ
        'COLON', # ДВОЕТОЧИЕ
        'SEMICOLON',  # ТОЧКА С ЗАПЯТОЙ
        'OPEN_PARENTHESIS', #ОТКРЫВАЮЩИЕСЯ СКОБКИ
        'CLOSE_PARENHESIS', #ЗАКРЫВАЮЩИЕСЯ СКОБКИ
        ]

t_NUMBER_INTEGER = r'\d+'
t_NUMBER_REAL = r'\d+\.\d+'

t_SUM = r'\+'
t_SUB = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'

t_EQUALLY = r'\='
t_MORE = r'\>'
t_LESS = r'\<'
t_ASSIGNMENT = r'\:='

t_COMMA = r'\,'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENHESIS = r'\)'

t_WRITE = r'write'
t_STRING = r'\"[^\'\n]*\"'

                #ДОПУСТИМЫЕ СИМВОЛЫ В НАЗВАНИИ ПЕРЕМЕННОЙ
def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'VARIABLE')
    return t

    # ИГНОРИРОВАНИЕ ПРОБЕЛОВ И ТАБУЛЯЦИИ
t_ignore = ' \t'


    #КОММЕНТИРОВАНИЕ КОДА В ВИДЕ /*...*/
def t_comment(t):
    r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    pass

                #СЧИТАТЬ СТРОКИ ПРОГРАММЫ
def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)

                #ОШИБКИ
def t_error(t):
    print ("Недопустимый символ '%s'" % t.value[0])
    #t.skip(1)

lex.lex()
