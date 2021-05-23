import ply.yacc as yacc
from lexer import tokens

class Node:
    def section_string(self):
        st = []
        for part in self.section:
            st.append( str( part ) )
        return "\n".join(st)   #возвращает и убирает символы из section

    def __repr__(self):
        return self.type + ":\n\t" + self.section_string().replace("\n", "\n\t")

    def append_descendant(self, section): #вставляет потомков
        self.section += section
        return self

    def __init__(self, type, section):
        self.type = type
        self.section = section
                        #ПОСТРОЕНИЕ ДЕРЕВА ИСХОДЯ ИЗ КС-ГРАММАТИКИ
def p_program(p):
    '''program : VAR dec_list BEGIN statement_list END
            | VAR dec_list function_list BEGIN statement_list END'''
    if len(p) == 6:
        p[0] = Node('program', [p[2], p[4]])

    else:
        p[0] = Node('program', [p[2], p[3], p[5]])

def p_def_list(p):
    '''function_list : function
               | function_list SEMICOLON function'''

    if len(p) == 2:
        p[0] = Node('FUNCTION', [p[1]])

    else:
        p[0] = p[1].append_descendant([p[3]])

def p_def(p):
    '''function : FUNCTION VARIABLE OPEN_PARENTHESIS dec_list CLOSE_PARENHESIS BEGIN statement_list_function END
            | FUNCTION VARIABLE OPEN_PARENTHESIS dec_list CLOSE_PARENHESIS BEGIN VAR dec_list statement_list_function END'''

    if len(p) == 9:
        p[0] = Node(p[2], [p[4], p[7]])

    else:
        p[0] = Node(p[2], [p[4], p[8], p[9]])

def p_statement_for_def_build(p):
    '''statement_for_function_build : VARIABLE OPEN_PARENTHESIS arguments CLOSE_PARENHESIS'''

    p[0] = Node(p[1], [p[3]])

def p_arguments(p):
    '''arguments : argument
            | arguments SEMICOLON argument'''

    if len(p) == 2:
        p[0] = Node('arguments', [p[1]])

    else:
        p[0] = p[1].append_descendant([p[3]])


def p_arg(p):
    '''argument : VARIABLE
            | NUMBER_INTEGER
            | NUMBER_REAL
            | OPEN_PARENTHESIS expression CLOSE_PARENHESIS'''

    if len(p) == 2:
        p[0] = p[1]

    else:
        p[0] = p[2]

def p_dec_list(p):
    '''dec_list : dec
               | dec_list SEMICOLON dec'''

    if len(p) == 2:
        p[0] = Node('VAR', [p[1]])

    else:
        p[0] = p[1].append_descendant([p[3]])

def p_dec(p):
    '''dec : variable_list COLON type'''

    p[0] = Node('dec', [p[1], p[3]])

def p_type(p):
    '''type : INTEGER
            | REAL
            | STRING'''

    p[0] = Node('type', [p[1]])

def p_variable_list(p):
    '''variable_list : VARIABLE
                | variable_list COMMA VARIABLE'''

    if len(p) == 2:
        p[0] = Node('variable', [p[1]])

    else:
        p[0] = p[1].append_descendant([p[3]])

def p_statement_list(p):
    '''statement_list : statement
                | statement_list SEMICOLON statement'''

    if len(p) == 2:
        p[0] = Node('statement', [p[1]])

    else:
        p[0] = p[1].append_descendant([p[3]])

def p_statement(p):
    '''statement : assign
            | write
            | while
            | if'''

    if len(p) == 2:
        p[0] = p[1]

def p_statement_list_if(p):
    '''statement_list_if : statement_for_if
                | statement_list_if SEMICOLON statement_for_if'''

    if len(p) == 2:
        p[0] = Node('statement', [p[1]])

    else:
        p[0] = p[1].append_descendant([p[3]])

def p_statement_for_if(p):
    '''statement_for_if : assign
            | write
            | while
            | if
            | CONTINUE
            | BREAK'''

    if len(p) == 2:
        p[0] = p[1]

def p_statement_list_def(p):
    '''statement_list_function : statement_for_function
                | statement_list_function SEMICOLON statement_for_function'''

    if len(p) == 2:
        p[0] = Node('statement', [p[1]])

    else:
        p[0] = p[1].append_descendant([p[3]])

def p_statement_for_def(p):
    '''statement_for_function : assign
            | write
            | while
            | if
            | return'''

    if len(p) == 2:
        p[0] = p[1]

def p_return(p):
    '''return : RETURN expression'''
    p[0] = Node(p[1], [p[2]])

def p_assign(p):
    '''assign : VARIABLE ASSIGNMENT expression
                | VARIABLE ASSIGNMENT STRING'''
    p[0] = Node('assign', [p[1], p[3]])

def p_expression(p):
    '''expression : addsub
            | expression SUM addsub
            | expression SUB addsub'''

    if len(p) == 2:
        p[0] = p[1]

    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_addsub(p):
    '''addsub : multiplayer
            | addsub MUL multiplayer
            | addsub DIV multiplayer'''

    if len(p) == 2:
        p[0] = p[1]

    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_multiplayer(p):
    '''multiplayer : statement_for_function_build
            | VARIABLE
            | NUMBER_INTEGER
            | NUMBER_REAL
            | OPEN_PARENTHESIS expression CLOSE_PARENHESIS'''

    if len(p) == 2:
        p[0] = p[1]

    else: p[0] = p[2]

def p_write(p):
    '''write : WRITE OPEN_PARENTHESIS expression CLOSE_PARENHESIS
                | WRITE OPEN_PARENTHESIS STRING CLOSE_PARENHESIS'''
    p[0] = Node('WRITE', [p[3]])

def p_while(p):
    '''while : WHILE bool_expression DO BEGIN statement_list END'''
    p[0] = Node('while', [p[2], p[5]])

def p_if(p):
    '''if : IF bool_expression THEN BEGIN statement_list_if END ELSE BEGIN statement_list_if END
            | IF bool_expression THEN BEGIN statement_list_if END'''

    if len(p) == 11:
        p[0] = Node('if', [p[2], p[5], p[9]])

    else:
        p[0] = Node('if', [p[2], p[5]])

def p_bool_expression(p):
    '''bool_expression : bool_expression OR bool_expression_addsub
                | bool_expression_addsub
                | NOT bool_expression
                | bool'''

    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])

    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])

    else:
        p[0] = p[1]

def p_bool_expression_addsub(p):
    '''bool_expression_addsub : bool_expression_addsub AND bool
                | bool'''

    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])

    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])

    else:
        p[0] = p[1]

def p_bool(p):
    '''bool : OPEN_PARENTHESIS expression EQUALLY expression CLOSE_PARENHESIS
            | OPEN_PARENTHESIS expression MORE expression CLOSE_PARENHESIS
            | OPEN_PARENTHESIS expression LESS expression CLOSE_PARENHESIS'''
    p[0] = Node(p[3], [p[2], p[4]])

def p_error(p):
    print ('Unexpressionected token:', p)

f = open('program.txt', 'r')
text_input = f.read()


parser = yacc.yacc()
cons = parser.parse(text_input)
print(cons)



