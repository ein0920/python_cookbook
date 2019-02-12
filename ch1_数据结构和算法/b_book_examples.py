
# 1、拆包，将序列分解长单独的变量
if __name__ == '__main__1':
    p = (4, 5)
    x, y = p

    x, y, z = p  # 这个功能就是unpack

    _, shares, price, _ = ['ACME', 50, 91.1, (2012, 12, 21)]


# 2、用*来拆包
if __name__ == '__main__2':

    record = (1,2,3,4,5,6,7)
    _, *middle, _ = record # 拆成list

    # Unpacking of tagged tuples of varying sizes

    records = [
        ('foo', 1, 2),
        ('bar', 'hello'),
        ('foo', 3, 4),
    ]


    def do_foo(x, y):
        print('foo', x, y)


    def do_bar(s):
        print('bar', s)


    for tag, *args in records:
        if tag == 'foo':
            do_foo(*args)
        elif tag == 'bar':
            do_bar(*args)
    # 这个类似于for 1, j in enumerate():
    # 因为enumerate返回这样一个东西[(0,some), (1,some2),...]


# 3、保留最后N个元素
if __name__ == '__main__':
    from collections import deque

    # 这个例子主要上使用deque，deque就是一个有最大长度的list，当有新的元素append是自动删去最老的记录，FIFO
    def search(lines, pattern, history=5):
        previous_lines = deque(maxlen=history)
        for line in lines:
            if pattern in line:
                yield line, previous_lines
            previous_lines.append(line)

    # Example use on a file
    if __name__ == '__main__':
        with open('somefile.txt') as f:  # open文件名称就是在同一目录下的文件
            for line, prevlines in search(f, 'python', 5):
                for pline in prevlines:
                    print(pline, end='')
                print(line, end='')
                print('-' * 20)

    # duque的一些方法
    q = deque(maxlen=3)
    q.append(1)
    q.append(2)
    q.append(3)

    q.append(4)
    q.appendleft(4)  # 在左边插入
    q.pop()  # 弹出右边第一个，
    q.popleft()  # 弹出左边第一个


# 4、找到最大或最小的N个元素
if __name__ == '__main__':
    import heapq

    nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
    print(heapq.nsmallest(3, nums))
    print(heapq.nlargest(3, nums))


    # 可以接受排序的函数
    portfolio = [
        {'name': 'IBM', 'shares': 100, 'price': 91.1},
        {'name': 'AAPL', 'shares': 50, 'price': 543.22},
        {'name': 'FB', 'shares': 200, 'price': 21.09},
        {'name': 'HPQ', 'shares': 35, 'price': 31.75},
        {'name': 'YHOO', 'shares': 45, 'price': 16.35},
        {'name': 'ACME', 'shares': 75, 'price': 115.65}
    ]

    cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
    expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])

    print(cheap)
    print(expensive)

    # 如果需要寻找的最大最小个数N相对于集合元素总数T来说很小，下面这些函数提供更好的性能，
    nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
    import heapq
    heap = list(nums)
    heapq.heapify(heap)  # 将最小几个数排序，复杂度上log(N)
    heap

    # 选取最大最小的数的效率分析
    # 1、如果选择最大最小，max和min上最快的
    # 2、如果N相对于T来说很小，那么用heapq.nsmallest
    # 3、如果N相对于T来说不小，那么先排序，用sorted(items)[:N]


# 5、实现优先级队列
if __name__ == '__main__':
    # 实现这样一个队列，以优先级对元素排序，每次pop都是
    import heapq
    class PriorityQueue:

        def __init__(self):
            self._queue = []
            self._index = 0

        def push(self, item, priority):
            heapq.heappush(self._queue, (-priority, self._index, item))
            self._index += 1

        def pop(self):
            return heapq.heappop(self._queue)[-1]


    class Item:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return 'Item({!r})'.format(self.name)


    q = PriorityQueue()
    q.push(Item('foo'), 1)
    q.push(Item('bar'), 5)
    q.push(Item('spam'), 4)
    q.push(Item('grok'), 1)

    # 一般对象比较
    a = Item('foo')
    b = Item('bar')
    a < b

    a = (1, Item('foo'))
    b = (5, Item('bar'))
    a < b
    c = (1, Item('grok'))
    a < c
    a == c

    a = (1, 0, Item('foo'))
    b = (5, 1, Item('bar'))
    c = (1, 2, Item('grok'))


# 6、在字典中将键映射到多个值上
if __name__ == '__main__':
    # 字典上一种关联容器，每个键都能映射到单独的值上，如果向让键映射到多个值上，需要将多个值保存在列表或者集合中
    # 可以这样建立
    d = {
        'a': [1,2,3],
        'b': [4,5]
    }

    e = {
        'a': {1,2,3},
        'b': {4,5}
    }  # 选用集合的是想消除元素，而且不在意顺序

    # 不过，有专门结构
    from collections import defaultdict
    d = defaultdict(list)
    d['a'].append(1)
    d['a'].append(2)
    d['b'].append(4)
    d['a']
    d['c']  # 调用的时候自动创建了'a'表项

    d = defaultdict(set)
    d['a'].add(1)
    d['a'].add(2)
    d['b'].add(4)

    # 对于defaultdict，需要注意的是，它会自动创建字典表项以待稍后的访问，如果不想要，可以有普通字典的setdefault
    d = {}
    d.setdefault('a', []).append(1) # 如果有'a'的话就调用d['a']，如果没有就创建，并把后面的值赋予这个键
    d.setdefault('a', []).append(2)
    d.setdefault('b', []).append(4)


# 7、有序字典
if __name__ == '__main__':
    # 一般字典的键之间是没有顺序，就是for的时候顺序和生成顺序不同
    from collections import OrderedDict
    d = OrderedDict()
    d = {}
    d['foo'] = 1
    d['bar'] = 2
    d['spam'] = 3
    d['grok'] = 4

    for key in d:
        print(key, d[key])


# 8、字典有关的计算问题
if __name__ == '__main__':
    # example.py
    #
    # Example of calculating with dictionaries

    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    # 这种tuple对可以用来比较，也可以用来min，max
    min_price = min(zip(prices.values(), prices.keys()))
    max_price = max(zip(prices.values(), prices.keys()))

    print('min price:', min_price)
    print('max price:', max_price)

    print('sorted prices:')
    prices_sorted = sorted(zip(prices.values(), prices.keys()))
    for price, name in prices_sorted:
        print('    ', name, price)


    # zip创建的迭代器只能只用一次
    prices_and_names = zip(prices.values(), prices.keys())
    print(min(prices_and_names))  # ok
    print(max(prices_and_names))  # ValueError: max() arg is an empty sequence

    # 同样也可以在字典里面处理
    min(prices)  # 对键排序

    # 可以对值排序，不过得不到对应关系
    min(prices.values())

    # 可以得到最大最小对应的键，对应关系可以多一重处理
    min(prices, key=lambda k: prices[k])
    min_value = prices[min(prices, key=lambda k: prices[k])]


# 9、在两个字典中寻找相同
if __name__ == '__main__':
    a = {
        'x': 1,
        'y': 2,
        'z': 3
    }

    b = {
        'w': 10,
        'x': 11,
        'y': 2
    }

    print('Common keys:', a.keys() & b.keys())
    print('Keys in a not in b:', a.keys() - b.keys())
    print('(key,value) pairs in common:', a.items() & b.items())  # .item就是变成一个tuple对的list

    # 字典推导式
    c = {key:a[key] for key in a.keys() - {'z', 'w'}}  # 键是采用集合的方式，可以采用集合操作，


# 10、从序列中移除重复项且保持元素间顺序不变
if __name__ == '__main__':

    # yield的需要在for或者while里面，同时在def里面
    # 元素是hashable
    def dedupe(items):
        seen = set()
        for item in items:
            if item not in seen:
                yield item
                seen.add(item)


    if __name__ == '__main__':
        a = [1, 5, 2, 1, 9, 1, 5, 10]
        print(a)
        print(list(dedupe(a)))


    # example2.py
    #
    # Remove duplicate entries from a sequence while keeping order

    def dedupe(items, key=None):
        seen = set()
        for item in items:
            val = item if key is None else key(item)
            if val not in seen:
                yield item
                seen.add(val)


    if __name__ == '__main__':
        a = [
            {'x': 2, 'y': 3},
            {'x': 1, 'y': 4},
            {'x': 2, 'y': 3},
            {'x': 2, 'y': 3},
            {'x': 10, 'y': 15}
        ]
        print(a)
        print(list(dedupe(a, key=lambda a: (a['x'], a['y']))))  # key是转化成hashable的对象


# 11、对切片进行命名
if __name__ == '__main__':
    items = [0,1,2,3,4,5,6]
    a = slice(2,4)
    items[2:4]
    items[a]


# 12、通过公共键对字典列表排序
if __name__ == '__main__':

    rows = [
        {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
        {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
        {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
        {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
    ]

    from operator import itemgetter

    rows_by_fname = sorted(rows, key=itemgetter('fname'))
    rows_by_uid = sorted(rows, key=itemgetter('uid'))

    from pprint import pprint

    print("Sorted by fname:")
    pprint(rows_by_fname)  # pprint提供了打印出任何python数据结构类和方法

    print("Sorted by uid:")
    pprint(rows_by_uid)

    rows_by_lfname = sorted(rows, key=itemgetter('lname', 'fname'))
    print("Sorted by lname,fname:")
    pprint(rows_by_lfname)

    # 相当于这个函数，但是效率更高
    rows_by_fname = sorted(rows, key=lambda r: r['fname'])


# 13、对不原生支持比较操作的对象排序
if __name__ == '__main__':
    from operator import attrgetter

    class User:
        def __init__(self, user_id):
            self.user_id = user_id

        def __repr__(self):
            return 'User({})'.format(self.user_id)

    # Example
    users = [User(23), User(3), User(99)]  # User实例不原生支持排序的对象，但是里面的property支持
    print(users)
    users[0].user_id

    # Sort it by user-id
    print(sorted(users, key=attrgetter('user_id')))


# 14、找出序列中出现最多的元素
if __name__ == '__main__':
    words = [
        'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
        'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
        'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
        'my', 'eyes', "you're", 'under'
    ]

    from collections import Counter

    # Counter的作用的计算每个序列的元素的出现次数，相当于词频统计
    word_counts = Counter(words)
    top_three = word_counts.most_common(3)
    print(top_three)
    # outputs [('eyes', 8), ('the', 5), ('look', 4)]

    # Example of merging in more words

    morewords = ['why', 'are', 'you', 'not', 'looking', 'in', 'my', 'eyes']
    word_counts.update(morewords)
    print(word_counts.most_common(3))


# 15、根据字段将记录分组，pandas的groupby就是源于这个
if __name__ == '__main__':
    rows = [
        {'address': '5412 N CLARK', 'date': '07/01/2012'},
        {'address': '5148 N CLARK', 'date': '07/04/2012'},
        {'address': '5800 E 58TH', 'date': '07/02/2012'},
        {'address': '2122 N CLARK', 'date': '07/03/2012'},
        {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
        {'address': '1060 W ADDISON', 'date': '07/02/2012'},
        {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
        {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
    ]

    from itertools import groupby

    rows.sort(key=lambda r: r['date'])
    for date, items in groupby(rows, key=lambda r: r['date']):
        print(date)
        for i in items:
            print('    ', i)

    grouped = groupby(rows, key=lambda r: r['date'])


    # Example of building a multidict
    from collections import defaultdict

    rows_by_date = defaultdict(list)
    for row in rows:
        rows_by_date[row['date']].append(row)

    for r in rows_by_date['07/01/2012']:
        print(r)


# 16、筛选序列中的元素
if __name__ == '__main__':
    # 列表推导式，也可以用()生成生成器，大序列的时候不用占用内存
    mylist = [1, 4, -5, 10, -7, 2, 3, -1]

    # All positive values
    pos = [n for n in mylist if n > 0]
    print(pos)

    # All negative values
    neg = [n for n in mylist if n < 0]
    print(neg)

    # Negative values clipped to 0
    neg_clip = [n if n > 0 else 0 for n in mylist]
    print(neg_clip)

    # Positive values clipped to 0
    pos_clip = [n if n < 0 else 0 for n in mylist]
    print(pos_clip)


    # Compressing这个内置工具

    addresses = [
        '5412 N CLARK',
        '5148 N CLARK',
        '5800 E 58TH',
        '2122 N CLARK',
        '5645 N RAVENSWOOD',
        '1060 W ADDISON',
        '4801 N BROADWAY',
        '1039 W GRANVILLE',
    ]

    counts = [0, 3, 10, 4, 1, 7, 6, 1]

    from itertools import compress

    more5 = [n > 5 for n in counts]
    a = list(compress(addresses, more5))  # addresses是目标列表，more5是布尔列表，一样长，将more5中的True对应多拿下来
    print(a)


# 17、从字典中提取子集，字典推导式效率更高
if __name__ == '__main__':
    from pprint import pprint

    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    # Make a dictionary of all prices over 200
    p1 = {key: value for key, value in prices.items() if value > 200}  # 推导式和if结合

    print("All prices over 200")
    pprint(p1)

    # Make a dictionary of tech stocks
    tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
    p2 = {key: value for key, value in prices.items() if key in tech_names}

    print("All techs")
    pprint(p2)


# 18、将名称映射到tuple中，namedtuple
if __name__ == '__main__':





    from collections import namedtuple

    Stock = namedtuple('Stock', ['name', 'shares', 'price'])


    def compute_cost(records):
        total = 0.0
        for rec in records:
            s = Stock(*rec)
            total += s.shares * s.price
        return total


    # Some Data
    records = [
        ('GOOG', 100, 490.1),
        ('ACME', 100, 123.45),
        ('IBM', 50, 91.15)
    ]

    print(compute_cost(records))


# 19、同时对数据做转换和换算，sum(a**2 for a in list)生成器
if __name__ == '_main__':
    import os

    files = os.listdir(os.path.expanduser('~'))
    if any(name.endswith('.py') for name in files):
        print('There be python!')
    else:
        print('Sorry, no python.')

    # Output a tuple as CSV
    s = ('ACME', 50, 123.45)
    print(','.join(str(x) for x in s))

    # Data reduction across fields of a data structure
    portfolio = [
        {'name': 'GOOG', 'shares': 50},
        {'name': 'YHOO', 'shares': 75},
        {'name': 'AOL', 'shares': 20},
        {'name': 'SCOX', 'shares': 65}
    ]
    min_shares = min(s['shares'] for s in portfolio)
    print(min_shares)


# 20将多个映射合并和单个映射，多个dict形式上合成一个
if __name__ == '__main__':
    a = {'x': 1, 'z': 3}
    b = {'y': 2, 'z': 4}

    # (a) Simple example of combining
    from collections import ChainMap

    c = ChainMap(a, b)
    print(c['x'])  # Outputs 1  (from a)
    print(c['y'])  # Outputs 2  (from b)
    print(c['z'])  # Outputs 3  (from a)

    # Output some common values
    print('len(c):', len(c))
    print('c.keys():', list(c.keys()))
    print('c.values():', list(c.values()))

    # 修改ChainMap的值，就是修改底层的值，c只是一个连接
    c['z'] = 10
    c['w'] = 40
    del c['x']
    print("a:", a)

    # Example of stacking mappings (like scopes)
    values = ChainMap()
    values['x'] = 1

    # Add a new mapping
    values = values.new_child()
    values['x'] = 2

    # Add a new mapping
    values = values.new_child()
    values['x'] = 3

    print(values)
    print(values['x'])

    # Discard last mapping
    values = values.parents
    print(values)
    print(values['x'])

    # Discard last mapping
    values = values.parents
    print(values)
    print(values['x'])


# ----------------------------------------------------------------------------------------------------------------------
# key参数
if __name__ == '__main__':
    '''key参数就是一个函数，对每一个元素执行一次操作，将返回的结果排序，可用于sorted，min，max'''
    rows = [
        {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
        {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
        {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
        {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
    ]
    rows_by_fname = sorted(rows, key=lambda r: r['fname'])