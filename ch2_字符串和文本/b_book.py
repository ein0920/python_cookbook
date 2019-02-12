
# 1、split
if __name__ == '__main__':
    import re

    line = 'asdf fjdk; afed, fjek,asdf,      foo'

    # (a) Splitting on space, comma, and semicolon
    parts = re.split(r'[;,\s]\s*', line)
    print(parts)

    # (b) Splitting with a capture group
    fields = re.split(r'(;|,|\s)\s*', line)
    print(fields)

    # (c) Rebuilding a string using fields above
    values = fields[::2]
    delimiters = fields[1::2]
    delimiters.append('')
    print('value =', values)
    print('delimiters =', delimiters)
    newline = ''.join(v + d for v, d in zip(values, delimiters))
    print('newline =', newline)

    # (d) Splitting using a non-capture group
    parts = re.split(r'(?:,|;|\s)\s*', line)
    print(parts)


# 2、startwith，返回TF，更加复杂的用法是正则表达式的^和$
if __name__ == '__main__':
    filename = 'spam.txt'
    filename.endswith('txt')


# 3、shell的通配符
if __name__ == '__main__':
    # example.py
    #
    # Example of using shell-wildcard style matching in list comprehensions

    from fnmatch import fnmatchcase as match

    addresses = [
        '5412 N CLARK ST',
        '1060 W ADDISON ST',
        '1039 W GRANVILLE AVE',
        '2122 N CLARK ST',
        '4802 N BROADWAY',
    ]

    a = [addr for addr in addresses if match(addr, '* ST')]
    print(a)

    b = [addr for addr in addresses if match(addr, '54[0-9][0-9] *CLARK*')]
    print(b)


# 正在表达式匹配，见tutorial
if __name__ == '__main__':
    pass


# 查找和替换文本
# searching_and_replacing_text
if __name__ == '__main__':
    import re

    # Some sample text
    text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'

    datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

    # (a) Simple substitution
    print(datepat.sub(r'\3-\1-\2', text))

    # (b) Replacement function
    from calendar import month_abbr


    def change_date(m):
        mon_name = month_abbr[int(m.group(1))]
        return '{} {} {}'.format(m.group(2), mon_name, m.group(3))


    print(datepat.sub(change_date, text))


# 简单的去掉字符strip
if __name__ == '__main__':
    # 空白的去除
    s = ' hello world \n'
    s.strip()
    s.lstrip()
    s.rstrip()

    # 字符去除
    t = '-------hello========'
    t.lstrip('-')
    t.rstrip('=')
    t.strip('-=')

    # 不会去除中间的
    s = ' hello   world   \n'
    s.strip()


# 文本的过滤和清理
if __name__ == '__main__':
    # A tricky string
    s = 'p\xfdt\u0125\xf6\xf1\x0cis\tawesome\r\n'
    print(s)

    # (a) Remapping whitespace
    remap = {
        ord('\t'): ' ',
        ord('\f'): ' ',
        ord('\r'): None  # Deleted
    }

    a = s.translate(remap)
    print('whitespace remapped:', a)

    # (b) Remove all combining characters/marks
    import unicodedata
    import sys

    cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                             if unicodedata.combining(chr(c)))

    b = unicodedata.normalize('NFD', a)
    c = b.translate(cmb_chrs)
    print('accents removed:', c)

    # (c) Accent removal using I/O decoding
    d = b.encode('ascii', 'ignore').decode('ascii')
    print('accents removed via I/O:', d)


# just，对齐
if __name__ == '__main__':
    text = 'hello world'
    text.ljust(20)
    text.rjust(20, '-')
    text.center(20, '*')

    format(text, '>20')  # 右对齐，挤到右边
    format(text, '^20')
    format(text, '=>20s')  #右对齐，填充=，作为字符串

    # format可用于其他类型的数据
    x = 1.2345
    format(x, '>10')
    format(x, '^10.2f')


# 连接join，比+连接更快
if __name__ == '__main__':
    def sample():
        yield "Is"  # 有yield的函数就是一个生成器，一个生成器一般要轮过多个yield的表达式，所以一个会有for
        yield "Chicago"
        yield "Not"
        yield "Chicago?"


    # (a) Simple join operator
    text = ''.join(sample())
    print(text)

    # (b) Redirection of parts to I/O
    import sys

    for part in sample():
        sys.stdout.write(part)
    sys.stdout.write('\n')  # 这个是在console输出的

    # (c) Combination of parts into buffers and larger I/O operations
    def combine(source, maxsize):  # 将source分块作为生成器的元素输出
        parts = []
        size = 0
        for part in source:
            parts.append(part)
            size += len(part)
            if size > maxsize:
                yield ''.join(parts)
                parts = []
                size = 0
        yield ''.join(parts)

    for part in combine(sample(), 32768):
        sys.stdout.write(part)
    sys.stdout.write('\n')


# variable_interpolation_in_strings，f字符串那个的处理
if __name__ == '__main__':
    # 第一个就是format方法
    s = '{name} has {n} message.'
    s.format(name='john', n=8)

    # format_map和vars()连用
    name = 'Guido'
    n = 90
    s.format_map(vars())


    # vars()可以用于类实例上
    class Info():
        def __init__(self, name, n):
            self.name = name
            self.n = n

    a = Info('Guido', 89)
    s.format_map(vars(a))  # vars(a)返回实例a内部的属性

    # format和format_map的缺点是无法优雅处理缺失值
    s.format(name='Guido')


    # 这个时候可以这样用，定义一个带有__missing__方法的字典类
    class safesub(dict):
        def __missing__(self, key):
            return '{%s}' % key

    s = '{name} has {n} messages.'

    # (a) Simple substitution
    name = 'Guido'
    n = 37

    print(s.format_map(vars()))

    # (b) Safe substitution with missing values
    del n
    print(s.format_map(safesub(vars())))

    # (c) Safe substitution + frame hack
    n = 37
    import sys

    # 下面这个就是对format的拓展，能够优雅应对缺失值的情形
    def sub(text):
        return text.format_map(safesub(sys._getframe(1).f_locals))

    print(sub('Hello {name}'))
    print(sub('{name} has {n} messages'))
    print(sub('Your favorite color is {color}'))


# 以固定的列来重新格式化长文本
if __name__ == '__main__':
    # A long string
    s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
    the eyes, not around the eyes, don't look around the eyes, \
    look into my eyes, you're under."

    import textwrap

    print(textwrap.fill(s, 70))  # 每行显示70字符
    print(textwrap.fill(s, 40))  # 每行显示40字符

    print(textwrap.fill(s, 40, initial_indent='    '))  # 首行开头有
    print(textwrap.fill(s, 40, subsequent_indent='    '))  # 下面每行空出来

    import os
    os.get_terminal_size().columns


# 文本分词  @todo
if __name__ == '__main__':
    text = 'foo = 23 + 42 * 10'
    tokens = [('NAME', 'foo'), ('EQ', '='), ('NUM', '23'), ('PLUS', '+'),
              ('NUM', '42'), ('TIMES', '*'), ('NUM', '10')]

    import re
    from collections import namedtuple

    NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
    NUM = r'(?P<NUM>\d+)'
    PLUS = r'(?P<PLUS>\+)'
    TIMES = r'(?P<TIMES>\*)'
    EQ = r'(?P<EQ>=)'
    WS = r'(?P<WS>\s+)'

    master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))
    Token = namedtuple('Token', ['type', 'value'])


    def generate_tokens(pat, text):
        scanner = pat.scanner(text)
        for m in iter(scanner.match, None):
            yield Token(m.lastgroup, m.group())


    for tok in generate_tokens(master_pat, 'foo = 42'):
        print(tok)


# 编一个简单的递归下降解析器
if __name__ == '__main__':
    # example.py
    #
    # An example of writing a simple recursive descent parser

    import re
    import collections

    # Token specification
    NUM = r'(?P<NUM>\d+)'
    PLUS = r'(?P<PLUS>\+)'
    MINUS = r'(?P<MINUS>-)'
    TIMES = r'(?P<TIMES>\*)'
    DIVIDE = r'(?P<DIVIDE>/)'
    LPAREN = r'(?P<LPAREN>\()'
    RPAREN = r'(?P<RPAREN>\))'
    WS = r'(?P<WS>\s+)'

    master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES,
                                      DIVIDE, LPAREN, RPAREN, WS]))

    # Tokenizer
    Token = collections.namedtuple('Token', ['type', 'value'])


    def generate_tokens(text):
        scanner = master_pat.scanner(text)
        for m in iter(scanner.match, None):
            tok = Token(m.lastgroup, m.group())
            if tok.type != 'WS':
                yield tok


    # Parser
    class ExpressionEvaluator:
        '''
        Implementation of a recursive descent parser.   Each method
        implements a single grammar rule.  Use the ._accept() method
        to test and accept the current lookahead token.  Use the ._expect()
        method to exactly match and discard the next token on on the input
        (or raise a SyntaxError if it doesn't match).
        '''

        def parse(self, text):
            self.tokens = generate_tokens(text)
            self.tok = None  # Last symbol consumed
            self.nexttok = None  # Next symbol tokenized
            self._advance()  # Load first lookahead token
            return self.expr()

        def _advance(self):
            'Advance one token ahead'
            self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

        def _accept(self, toktype):
            'Test and consume the next token if it matches toktype'
            if self.nexttok and self.nexttok.type == toktype:
                self._advance()
                return True
            else:
                return False

        def _expect(self, toktype):
            'Consume next token if it matches toktype or raise SyntaxError'
            if not self._accept(toktype):
                raise SyntaxError('Expected ' + toktype)

        # Grammar rules follow

        def expr(self):
            "expression ::= term { ('+'|'-') term }*"

            exprval = self.term()
            while self._accept('PLUS') or self._accept('MINUS'):
                op = self.tok.type
                right = self.term()
                if op == 'PLUS':
                    exprval += right
                elif op == 'MINUS':
                    exprval -= right
            return exprval

        def term(self):
            "term ::= factor { ('*'|'/') factor }*"

            termval = self.factor()
            while self._accept('TIMES') or self._accept('DIVIDE'):
                op = self.tok.type
                right = self.factor()
                if op == 'TIMES':
                    termval *= right
                elif op == 'DIVIDE':
                    termval /= right
            return termval

        def factor(self):
            "factor ::= NUM | ( expr )"

            if self._accept('NUM'):
                return int(self.tok.value)
            elif self._accept('LPAREN'):
                exprval = self.expr()
                self._expect('RPAREN')
                return exprval
            else:
                raise SyntaxError('Expected NUMBER or LPAREN')


    if __name__ == '__main__':
        e = ExpressionEvaluator()
        print(e.parse('2'))
        print(e.parse('2 + 3'))
        print(e.parse('2 + 3 * 4'))
        print(e.parse('2 + (3 + 4) * 5'))


    # Example of building trees

    class ExpressionTreeBuilder(ExpressionEvaluator):
        def expr(self):
            "expression ::= term { ('+'|'-') term }"

            exprval = self.term()
            while self._accept('PLUS') or self._accept('MINUS'):
                op = self.tok.type
                right = self.term()
                if op == 'PLUS':
                    exprval = ('+', exprval, right)
                elif op == 'MINUS':
                    exprval = ('-', exprval, right)
            return exprval

        def term(self):
            "term ::= factor { ('*'|'/') factor }"

            termval = self.factor()
            while self._accept('TIMES') or self._accept('DIVIDE'):
                op = self.tok.type
                right = self.factor()
                if op == 'TIMES':
                    termval = ('*', termval, right)
                elif op == 'DIVIDE':
                    termval = ('/', termval, right)
            return termval

        def factor(self):
            'factor ::= NUM | ( expr )'

            if self._accept('NUM'):
                return int(self.tok.value)
            elif self._accept('LPAREN'):
                exprval = self.expr()
                self._expect('RPAREN')
                return exprval
            else:
                raise SyntaxError('Expected NUMBER or LPAREN')


    if __name__ == '__main__':
        e = ExpressionTreeBuilder()
        print(e.parse('2 + 3'))
        print(e.parse('2 + 3 * 4'))
        print(e.parse('2 + (3 + 4) * 5'))
        print(e.parse('2 + 3 + 4'))
