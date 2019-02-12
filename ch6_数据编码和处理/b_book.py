
# 读写csv数据
if __name__ == '__main__':
    # 这个模块读出来的是字符串
    import csv

    # (a) 可以用next访问

    print('Reading as tuples:')
    # f = open('ch6_数据编码和处理/stocks.csv')
    with open('ch6_数据编码和处理/stocks.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            # process row
            print('    ', row)

    # (b) Reading as namedtuples

    print('Reading as namedtuples')
    from collections import namedtuple

    with open('ch6_数据编码和处理/stocks.csv') as f:
        f_csv = csv.reader(f)
        Row = namedtuple('Row', next(f_csv))
        for r in f_csv:
            row = Row(*r)  # 拆开tuple r成为可以作为参数输入的
            # Process row
            print('    ', row)
            row.Symbol


    # (c) Reading as dictionaries

    print('Reading as dicts')
    with open('ch6_数据编码和处理/stocks.csv') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            # process row
            print('    ', row)
            row['Symbol']  # orderdict的访问

    # (d) Reading into tuples with type conversion

    print('Reading into named tuples with type conversion')

    col_types = [str, float, str, str, float, int]
    with open('ch6_数据编码和处理/stocks.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            # Apply conversions to the row items
            row = tuple(convert(value) for convert, value in zip(col_types, row))
            print(row)

    # (e) Converting selected dict fields

    print('Reading as dicts with type conversion')

    field_types = [('Price', float),
                   ('Change', float),
                   ('Volume', int)]

    with open('ch6_数据编码和处理/stocks.csv') as f:
        for row in csv.DictReader(f):
            row.update((key, conversion(row[key]))
                       for key, conversion in field_types)
            print(row)

    # 写入
    headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
    rows = [['AA', '39.48', '6/11/2007', '9:36am', '-0.18', '181800'],
     ['AIG', '71.38', '6/11/2007', '9:36am', '-0.15', '195500'],
     ['AXP', '62.58', '6/11/2007', '9:36am', '-0.46', '935000'],
     ['BA', '98.31', '6/11/2007', '9:36am', '+0.12', '104800'],
     ['C', '53.08', '6/11/2007', '9:36am', '-0.25', '360900'],
     ['CAT', '78.29', '6/11/2007', '9:36am', '-0.23', '225400']]
    with open('ch6_数据编码和处理/stocks_1.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
        # 写入dict
        # f_csv = csv.DictWriter(f, headers)
        # f_csv.writerows(rows)

        # 指定分隔符
        # f_csv = csv.reader(f, delimiter='\t')


# reading_and_writing_json_data
if __name__ == '__main__':
    import json

    # 变成json型字符串
    data = {'name':'ACME', 'shares':100, 'price':542.23}
    json_str = json.dumps(data)  # 不是dump，dump是写入json文件
    # json字符串变成对象
    data1 = json.loads(json_str)

    # (a) Turning JSON into an OrderedDict
    s = '{"name": "ACME", "shares": 50, "price": 490.1}'
    from collections import OrderedDict

    data = json.loads(s, object_pairs_hook=OrderedDict)  # 变成OrderedDict
    print(data)

    # 写入json文件
    data = {'name': 'ACME', 'shares': 100, 'price': 542.23}
    with open('ch6_数据编码和处理/data.json', 'w') as f:
        json.dump(data, f)

    with open('ch6_数据编码和处理/data.json', 'w') as f:
        data = json.load(f)

    # json编码支持有None，bool， int，flat和str。还在字典，列表和原则，和python很像，



    # json字典转变成python对象
    import json
    class JSONObject:
        def __init__(self, d):
            self.__dict__ = d

    s = '{"name": "ACME", "shares": 50, "price": 490.1}'
    data = json.loads(s, object_hook=JSONObject)
    print(data.name)
    print(data.shares)
    print(data.price)

    # 输出漂亮一点
    data = {'name':'ACME', 'shares':100, 'price':542.23}
    print(json.dumps(data, indent=2))  # 左边的空格数
    print(json.dumps(data, sort_keys=True))  # 排序

    # 类实例一般无法变成json，要用以下方法
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def serialize_instance(obj):
        d = {'__classname__': type(obj).__name__}
        d.update(vars(obj))
        return d

    p = Point(3, 4)
    s = json.dumps(p, default=serialize_instance)
    print(s)

    # 解析json中的实例
    classes = {
        'Point': Point
    }


    def unserialize_object(d):
        clsname = d.pop('__classname__', None)
        if clsname:
            cls = classes[clsname]
            obj = cls.__new__(cls)
            for key, value in d.items():
                setattr(obj, key, value)
            return obj
        else:
            return d


    a = json.loads(s, object_hook=unserialize_object)
    print(a)
    print(a.x)
    print(a.y)


# 解析简单的xml文档，parse完之后直接iterfind或者findtext找标签
if __name__ == '__main__':
    from urllib.request import urlopen
    from xml.etree.ElementTree import parse

    # Download the RSS feed and parse it
    u = urlopen('http://planet.python.org/rss20.xml')
    doc = parse(u)

    # Extract and output tags of interest
    for item in doc.iterfind('channel/item'):
        title = item.findtext('title')
        date = item.findtext('pubDate')
        link = item.findtext('link')

        print(title)
        print(date)
        print(link)
        print()


# 4、incremental_parsing_of_huge_xml_files
if __name__ == '__main__':
    # 就是做成iter
    from xml.etree.ElementTree import iterparse

    filename = 'ch6_数据编码和处理/potholes.xml'
    path = 'row/row'
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # Skip the root element
    next(doc)

    tag_stack = []
    elem_stack = []

    event, elem = next(doc)


    def parse_and_remove(filename, path):
        path_parts = path.split('/')
        doc = iterparse(filename, ('start', 'end'))  # 每次读一行，区分标签是开始还是结尾
        # Skip the root element
        next(doc)

        tag_stack = []
        elem_stack = []
        for event, elem in doc:
            if event == 'start':
                tag_stack.append(elem.tag)
                elem_stack.append(elem)
            elif event == 'end':
                if tag_stack == path_parts:
                    yield elem
                    elem_stack[-2].remove(elem)
                try:
                    tag_stack.pop()
                    elem_stack.pop()
                except IndexError:
                    pass


    # Find zip code with most potholes

    from collections import Counter

    potholes_by_zip = Counter()

    data = parse_and_remove('ch6_数据编码和处理/potholes.xml', 'row/row')
    for pothole in data:
        potholes_by_zip[pothole.findtext('zip')] += 1

    for zipcode, num in potholes_by_zip.most_common():
        print(zipcode, num)

    # 下面这个是很耗内存的，因为要把整个xml文档读入内存，iterparse只读一行，所以不能多行分析，不能像parse那样层级分析
    from xml.etree.ElementTree import parse

    potholes_by_zip = Counter()

    doc = parse('ch6_数据编码和处理/potholes.xml')
    for pothole in doc.iterfind('row/row'):  # 'row/row'是层级的关系，
        potholes_by_zip[pothole.findtext('zip')] += 1

    for zipcode, num in potholes_by_zip.most_common():
        print(zipcode, num)


# 将字典转换成xml
if __name__ == '__main__':
    from xml.etree.ElementTree import Element

    def dict_to_xml(tag, d):
        elem = Element(tag)
        for key, val in d.items():
            child = Element(key)
            child.text = str(val)
            elem.append(child)
        return elem

    s = {'name':'GOOG', 'shares':100, 'price':490.1}
    e = dict_to_xml('stock', s)

    from xml.etree.ElementTree import tostring
    tostring(e)

    # 其实自己拼字符串也可以，但是如果包含特殊字符经常会注意不到而出问题


# 解析，修改和重写xml，getroot是拿根节点
if __name__ == '__main__':
    from xml.etree.ElementTree import parse, Element

    doc = parse('ch6_数据编码和处理/pred.xml')
    root = doc.getroot()

    # Remove a few elements
    root.remove(root.find('sri'))
    root.remove(root.find('cr'))

    # Insert a new element after <nm>...</nm>
    nm_index = root.getchildren().index(root.find('nm'))

    e = Element('spam')
    e.text = 'This is a test'
    root.insert(nm_index + 1, e)

    # Write back to a file
    doc.write('ch6_数据编码和处理/newpred.xml', xml_declaration=True)

