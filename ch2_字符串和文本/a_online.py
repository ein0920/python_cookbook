

# matching_and_searching_for_text_patterns_using_regular_expressions
if __name__ == '__main__':
    # example.py
    #
    # Examples of simple regular expression matching

    import re

    # Some sample text
    text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'

    # (a) Find all matching dates
    datepat = re.compile(r'\d+/\d+/\d+')
    print(datepat.findall(text))

    # (b) Find all matching dates with capture groups
    datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
    for month, day, year in datepat.findall(text):
        print('{}-{}-{}'.format(year, month, day))

    # (c) Iterative search
    for m in datepat.finditer(text):
        print(m.groups())



# normalizing_unicode_text_to_a_standard_representation
if __name__ == '__main__':
    # example.py
    #
    # Example of unicode normalization

    # Two strings
    s1 = 'Spicy Jalape\u00f1o'
    s2 = 'Spicy Jalapen\u0303o'

    # (a) Print them out (usually looks identical)
    print(s1)
    print(s2)

    # (b) Examine equality and length
    print('s1 == s2', s1 == s2)
    print(len(s1), len(s2))

    # (c) Normalize and try the same experiment
    import unicodedata

    n_s1 = unicodedata.normalize('NFC', s1)
    n_s2 = unicodedata.normalize('NFC', s2)

    print('n_s1 == n_s2', n_s1 == n_s2)
    print(len(n_s1), len(n_s2))

    # (d) Example of normalizing to a decomposed form and stripping accents
    t1 = unicodedata.normalize('NFD', s1)
    print(''.join(c for c in t1 if not unicodedata.combining(c)))




# specifying_a_regular_expression_for_the_shortest_match
if __name__ == '__main__':
    # example.py
    #
    # Example of a regular expression that finds shortest matches

    import re

    # Sample text
    text = 'Computer says "no." Phone says "yes."'

    # (a) Regex that finds quoted strings - longest match
    str_pat = re.compile(r'\"(.*)\"')
    print(str_pat.findall(text))

    # (b) Regex that finds quoted strings - shortest match
    str_pat = re.compile(r'\"(.*?)\"')
    print(str_pat.findall(text))





# tokenizing_text
if __name__ == '__main__':


    master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))




# writing_a_regular_expression_for_multiline_patterns
if __name__ == '__main__':
    # example.py
    #
    # Regular expression that matches multiline patterns

    import re

    text = '''/* this is a
                  multiline comment */
    '''

    comment = re.compile(r'/\*((?:.|\n)*?)\*/')
    print(comment.findall(text))




if __name__ == '__main__':
    # plyexample.py
    #
    # Example of parsing with PLY

    from ply.lex import lex
    from ply.yacc import yacc

    # Token list
    tokens = ['NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN']

    # Ignored characters

    t_ignore = ' \t\n'

    # Token specifications (as regexs)
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'


    # Token processing functions
    def t_NUM(t):
        r'\d+'
        t.value = int(t.value)
        return t


    # Error handler
    def t_error(t):
        print('Bad character: {!r}'.format(t.value[0]))
        t.skip(1)


    # Build the lexer
    lexer = lex()


    # Grammar rules and handler functions
    def p_expr(p):
        '''
        expr : expr PLUS term
             | expr MINUS term
        '''
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]


    def p_expr_term(p):
        '''
        expr : term
        '''
        p[0] = p[1]


    def p_term(p):
        '''
        term : term TIMES factor
             | term DIVIDE factor
        '''
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]


    def p_term_factor(p):
        '''
        term : factor
        '''
        p[0] = p[1]


    def p_factor(p):
        '''
        factor : NUM
        '''
        p[0] = p[1]


    def p_factor_group(p):
        '''
        factor : LPAREN expr RPAREN
        '''
        p[0] = p[2]


    def p_error(p):
        print('Syntax error')


    parser = yacc()

    if __name__ == '__main__':
        print(parser.parse('2'))
        print(parser.parse('2+3'))
        print(parser.parse('2+(3+4)*5'))
