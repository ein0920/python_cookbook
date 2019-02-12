
# 1、手动访问迭代器的元素
if __name__ == '__main__':
    # 不用for如何访问迭代器的元素，next
    with open('ch4_迭代器和生成器/somefile.txt') as f:  # 这里的f也是一个迭代器，应用
        try:
            while True:
                line = next(f)
                print(line, end='')
        except StopIteration:  # 最后一次运行会抛出StopIteration异常
            pass

    items = [1,2,3]
    it = iter(items)  # 变成迭代器，迭代器会记得next了多少次
    next(it)
    next(it)
    next(it)
    next(it)


# 2、委托迭代
if __name__ == '__main__':
    class Node:
        def __init__(self, value):
            self._value = value
            self._children = []

        def __repr__(self):
            return 'Node({!r})'.format(self._value)

        def add_child(self, node):
            self._children.append(node)

        def __iter__(self):  # 要可以对实例使用for，就有有这个
            return iter(self._children)


    # Example
    if __name__ == '__main__':
        root = Node(0)
        child1 = Node(1)
        child2 = Node(2)
        root.add_child(child1)
        root.add_child(child2)
        for ch in root:
            print(ch)
        # Outputs: Node(1), Node(2)

        root._children


# 3、用生成器创建新的迭代模式
if __name__ == '__main__':
    # 这个一个典型的生成器：生成器是一个函数，里面必须能出现多个yield（多数情况用循环，循环体中有yield）
    def frange(start, stop, increment):
        x = start
        while x < stop:
            yield x
            x += increment

    for n in frange(0, 4, 0.5):
        print(n)

    # 一个非典型的生成器
    def gen1():
        yield 1
        yield 2
        yield 3
        yield 4

    gen1  # 这个一个函数名
    gen1()  # 这是一个生成器，这时候不会运行

    for elem in gen1():
        print(elem)

    '''
    只要出现yield的函数就是一个生成器，与普通的函数不同，生成器只会在效应迭代操作时才会生效
    '''

    # 例如
    def count_down(n):
        print('Starting to count from', n)
        while n > 0:
            yield n
            n -= 1
        print('Done!')

    c = count_down(3)  # 创建一个生成器generator，但是并没有运行
    c
    next(c)  # 第一次运行时生成器就相当于运行函数，到第一个yield处停止，返回yield的内容
    next(c)  # 第二次从第一个yield到第二个yield之间
    next(c)  # 这个时候n = 1
    next(c)  # 这个时候n=0，跳出循环，print('Done!')，由于没有下一个yield了，抛出StopIteration

    for cc in c:  # 跑完后c就失效了，不能在next或者for
        print(cc)


    c = count_down(3)  # 创建一个生成器generator，但是并没有运行
    for cc in c:  # 重置了才行
        print(cc)


# 4、实现迭代协议
if __name__ == '__main__':
    class Node:
        def __init__(self, value):
            self._value = value
            self._children = []

        def __repr__(self):
            return 'Node({!r})'.format(self._value)

        def add_child(self, node):
            self._children.append(node)

        def __iter__(self):
            return iter(self._children)

        def depth_first(self):  # 用生成器实现深度优先便利
            yield self
            for c in self:
                yield from c.depth_first()

    # Example
    if __name__ == '__main__':
        root = Node(0)
        child1 = Node(1)
        child2 = Node(2)
        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(Node(3))
        child1.add_child(Node(4))
        child2.add_child(Node(5))

        for ch in root.depth_first():
            print(ch)
        # Outputs: Node(0), Node(1), Node(3), Node(4), Node(2), Node(5)

if __name__ == '__main__':
    # Hard example of depth-first iteration using an iterator object

    class Node:
        def __init__(self, value):
            self._value = value
            self._children = []

        def __repr__(self):
            return 'Node(%r)' % self._value

        def add_child(self, other_node):
            self._children.append(other_node)

        def __iter__(self):
            return iter(self._children)

        def depth_first(self):
            return DepthFirstIterator(self)


    class DepthFirstIterator(object):
        '''
        Depth-first traversal
        '''

        def __init__(self, start_node):
            self._node = start_node
            self._children_iter = None
            self._child_iter = None

        def __iter__(self):
            return self

        def __next__(self):
            # Return myself if just started. Create an iterator for children
            if self._children_iter is None:
                self._children_iter = iter(self._node)
                return self._node

            # If processing a child, return its next item
            elif self._child_iter:
                try:
                    nextchild = next(self._child_iter)
                    return nextchild
                except StopIteration:
                    self._child_iter = None
                    return next(self)

            # Advance to the next child and start its iteration
            else:
                self._child_iter = next(self._children_iter).depth_first()
                return next(self)


    # Example
    if __name__ == '__main__':
        root = Node(0)
        child1 = Node(1)
        child2 = Node(2)
        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(Node(3))
        child1.add_child(Node(4))
        child2.add_child(Node(5))

        for ch in root.depth_first():
            print(ch)
        # Outputs: Node(0), Node(1), Node(3), Node(4), Node(2), Node(5)


# 反向迭代和__reversed__方法
if __name__ == '__main__':
    # 处理对象是确定长度的，如果没有__reversed__的话就使用__getitem__和__len__来实现


    # 或者将其转化成list


    # 定义__reversed__方法可以
    class Countdown:
        def __init__(self, start):
            self.start = start

        # Forward iterator
        def __iter__(self):  # 迭代魔术方法也可以是一个生成器
            n = self.start
            while n > 0:
                yield n
                n -= 1

        # Reverse iterator
        def __reversed__(self):
            n = 1
            while n <= self.start:
                yield n
                n += 1


    c = Countdown(5)
    print("Forward:")
    for x in c:
        print(x)

    print("Reverse:")
    for x in reversed(c):
        print(x)


# generators_with_state，带状态的生成器
if __name__ == '__main__':
    from collections import deque


    class linehistory:
        def __init__(self, lines, histlen=3):  # 将一个迭代对象输入
            self.lines = lines
            self.history = deque(maxlen=histlen)

        def __iter__(self):  # 直接用for，不用__next__，但是不能用next()
            for lineno, line in enumerate(self.lines, 1):  # enumerate(iter, 1)是从1开始的意思
                self.history.append((lineno, line))
                yield line

        def clear(self):
            self.history.clear()


    with open('ch4_迭代器和生成器/somefile.txt') as f:
        lines = linehistory(f)
        for line in lines:  # 调用__iter__方法
            if 'python' in line:
                for lineno, hline in lines.history:
                    print('{}:{}'.format(lineno, hline), end='')


    # 由于没有next方法，所以不能调用next，要变成iter
    f = open('ch4_迭代器和生成器/somefile.txt')
    lines = linehistory(f)
    next(lines)

    it = iter(lines)
    next(it)


# 对迭代器做切片处理
if __name__ == '__main__':
    def count(n):  # 这个一个无限的迭代器，没有固定长度
        while True:
            yield n
            n += 1


    c = count(0)
    c[10:20]

    # 用islice
    import itertools
    for x in itertools.islice(c, 10, 20):
        print(x)


# 跳过可迭代对象中的前一部分元素
if __name__ == '__main__':
    from itertools import islice
    items = ['a', 'b', 'c', 1, 4, 10, 15]

    for x in islice(items, 3, None):
        print(x)


    # 筛选开始的元素，最后那个带h的不删去
    from itertools import dropwhile

    with open('ch4_迭代器和生成器/somefile.txt') as f:
        for line in dropwhile(lambda line: line.startswith('h'), f):
            print(line, end='')

    # 注意一下区别，把最后一行也删去了
    with open('ch4_迭代器和生成器/somefile.txt') as f:
        lines = (line for line in f if not line.startswith('h'))
        for line in lines:
            print(line, end='')


# 迭代所有可能的组合或者排列
if __name__ == '__main__':
    # 返回所有排列
    items = ['a', 'b', 'c']
    from itertools import permutations
    for p in permutations(items):  # 接受一个元素集合，重排为所有可能的排列，返回元组的形式
        print(p)

    for p in permutations(items, 2):  # 较短的长度
        print(p)

    # 返回所有组合
    items = ['a', 'b', 'c']
    from itertools import combinations

    for p in combinations(items, 3):  # 接受一个元素集合，重排为所有可能的排列，返回元组的形式
        print(p)

    for p in combinations(items, 2):  # 较短的长度
        print(p)

    # 可以重复的组合
    items = ['a', 'b', 'c']
    from itertools import combinations_with_replacement
    for c in combinations_with_replacement(items, 3):
        print(c)


# enumerate
if __name__ == '__main__':
    # 可以接受其他参数
    my_list = ['a', 'b', 'c']
    for idx, val in enumerate(my_list, 2):
        print(idx, val)

    # Example of iterating over lines of a file with an extra lineno attribute
    def parse_data(filename):
        with open(filename, 'rt') as f:
            for lineno, line in enumerate(f, 1):
                fields = line.split()
                try:
                    count = int(fields[1])
                except ValueError as e:
                    print('Line {}: Parse error: {}'.format(lineno, e))

    parse_data('ch4_迭代器和生成器/sample.dat')

    # enumerate本身返回一个元组，如果被分解对象也是元组的话，
    data = [(1,2), (3,4), (5,6), (7,8),]
    # 要这样
    for n , (x, y) in enumerate(data):
        pass
    # 不能这样
    for n , x, y in enumerate(data):
        pass


# 同时迭代多个序列，zip，返回迭代器
if __name__ == '__main__':
    xpts = [1,4,6,43,4]
    ypts = [234,324,5345,6345]
    for x, y in zip(xpts, ypts):  # 以短的为准
        print(x,y)

    from itertools import zip_longest
    for x, y in zip_longest(xpts, ypts):  # 以长的为准
        print(x,y)

    for x, y in zip_longest(xpts, ypts,fillvalue=0):  # 以长的为准，填充
        print(x,y)

    # 可以多于2个zip
    a = [1,2,3]
    b = [10,11,12]
    c = ['x', 'y', 'c']
    for i in zip(a,b,c):
        print(i)


# chain，多个连接器在一起
if __name__ == '__main__':
    # Example of iterating over two sequences as one

    from itertools import chain

    a = [1, 2, 3, 4]
    b = ['x', 'y', 'z']
    for x in chain(a, b):  # 比a+b高效
        print(x)


# 管道pipe，数据量太大，无法完全加载到内存中，但是要进行相同的处理，将每个字元素组到一个generator中
# creating_data_processing_pipelines
if __name__ == '__main__':
    import os
    import fnmatch
    import gzip
    import bz2
    import re


    # 将所有的文件做成一个iter，而不是一个list，很长的list可以用这种处理，
    def gen_find(filepat, top):
        '''
        Find all filenames in a directory tree that match a shell wildcard pattern
        '''
        for path, dirlist, filelist in os.walk(top):
            for name in fnmatch.filter(filelist, filepat):
                yield os.path.join(path, name)


    # 打开文件，因为打开的文件返回的就是一个iter
    def gen_opener(filenames):
        '''
        Open a sequence of filenames one at a time producing a file object.
        The file is closed immediately when proceeding to the next iteration.
        '''
        for filename in filenames:
            if filename.endswith('.gz'):
                f = gzip.open(filename, 'rt')
            elif filename.endswith('.bz2'):
                f = bz2.open(filename, 'rt')
            else:
                f = open(filename, 'rt')
            yield f
            f.close()


    def gen_concatenate(iterators):
        '''
        每一行的iter
        '''
        for it in iterators:
            for i in it:
                yield i


    def gen_grep(pattern, lines):
        '''
        Look for a regex pattern in a sequence of lines
        '''
        pat = re.compile(pattern)
        for line in lines:
            if pat.search(line):
                yield line


    if __name__ == '__main__':

        # Example 1
        lognames = gen_find('access-log*', 'ch4_迭代器和生成器/www')
        files = gen_opener(lognames)
        lines = gen_concatenate(files)
        pylines = gen_grep('(?i)python', lines)
        for line in pylines:
            print(line)

        # Example 2
        lognames = gen_find('access-log*', 'www')
        files = gen_opener(lognames)
        lines = gen_concatenate(files)
        pylines = gen_grep('(?i)python', lines)
        bytecolumn = (line.rsplit(None, 1)[1] for line in pylines)
        bytes = (int(x) for x in bytecolumn if x != '-')
        print('Total', sum(bytes))


# 扁平化，
if __name__ == '__main__':
    # Example of flattening a nested sequence using subgenerators

    from collections import Iterable  # 可迭代对象

    def flatten(items, ignore_types=(str, bytes)):
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from flatten(x)  # 迭代器用于递归的语句，
            else:
                yield x

    def flattern(sample):
        if isinstance(sample, list):
            result = []
            for item in sample:
                result += flattern(item)
        else:
            return [sample]

        return result

    inputList = [1, [2, [3, [8888,666], [4, 6, [45, 78, [99]], [45,67,89,[999,[4543,90]]]]], 45]]
    flattern(inputList)




    items = [1, 2, [3, 4, [5, 6], 7], 8]

    # Produces 1 2 3 4 5 6 7 8
    for x in flatten(items):
        print(x)

    items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
    for x in flatten(items):
        print(x)