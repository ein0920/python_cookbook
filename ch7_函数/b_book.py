
# 编写可接受任意数量参数的函数 *args，一般在参数中都是*的形态，
if __name__ == '__main__':
    # Examples of *args and **kwargs functions
    #
    def avg(first, *rest):
        return (first + sum(rest)) / (1 + len(rest))


    print(avg(1, 2))
    print(avg(1, 2, 3, 4))

    import html


    def make_element(name, value, **attrs):
        keyvals = [' %s="%s"' % item for item in attrs.items()]
        attr_str = ''.join(keyvals)
        element = '<{name}{attrs}>{value}</{name}>'.format(
            name=name,
            attrs=attr_str,
            value=html.escape(value))
        return element


    # Example
    # Creates '<item size="large" quantity="6">Albatross</item>'
    print(make_element('item', 'Albatross', size='large', quantity=6))
    print(make_element('p', '<spam>'))

    # 这样也是可以，注意和线面的区别
    def a(x, *args, y):
        pass


# 希望函数使用的时候某些参数只通过关键字的形式输入，
if __name__ == '__main__':
    # 注意是*，而不是*args
    def recv_1(maxsize, *, block):  # block只能block=True给出，*相当于是个分隔符
        print(maxsize, block)
        pass

    recv_1(1024,True)  # TypeError
    recv_1(1024, block=True)  # OK


    # A simple keyword-only argument
    def recv(maxsize, *, block=True):
        print(maxsize, block)


    recv(8192, block=False)  # Works
    try:
        recv(8192, False)  # Fails
    except TypeError as e:
        print(e)


    # Adding keyword-only args to *args functions
    def minimum(*values, clip=None):
        m = min(values)
        if clip is not None:
            m = clip if clip > m else m
        return m


    print(minimum(1, 5, 2, -5, 10))
    print(minimum(1, 5, 2, -5, 10, clip=0))
