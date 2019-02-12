
# 读写文本数据 txt
if __name__ == '__main__':
    # 1、整个txt读作一个string，f.read()
    with open('ch5_文件与IO/sample.txt', 'rt') as f:  # open的文件地址上直接在project下面找，用'somefile.txt'是错的
        data = f.read()  # 整个txt读作一个string

    # 2、f是个可迭代的对象
    rst = []
    with open('ch5_文件与IO/sample.txt', 'rt') as f:
        for line in f:
            rst.append(line)

    # 3、f.readline()  # 相当于next
    with open('ch5_文件与IO/sample.txt', 'rt') as f:
        a = f.readline()
        b = f.readline()
        c = f.readline()
        # 每次读取第一行，分别返回给a,b,c，以pop的形式，读取完就不再f中了

    with open('ch5_文件与IO/sample.txt', 'rt') as f:
        a = f.readline(3) #
        b = f.readline(3)
        # 每次读取前三个字符，分别返回给a,b

    # 4、readlines()  读成list
    with open('ch5_文件与IO/sample.txt', 'rt') as f:
        a = f.readlines()
        # 读出所有行，每一个作为list的一个元素，返回一个list

    # 5、写入操作，覆盖
    with open('ch5_文件与IO/sample.txt', 'wt') as f:
        f.write('hahaha')  # 覆盖了所有内容

    # 追加到后面，用at模式
    with open('ch5_文件与IO/sample.txt', 'at') as f:
        f.write('hahaha')  # 加到最后一行

    # 这样也可以写入
    with open('ch5_文件与IO/sample.txt', 'wt') as f:
        print('=== Keeping the Last N Items\n', file=f)

    # 可以指定编码方式
    with open('ch5_文件与IO/sample.txt', 'wt', encoding='latin-1') as f:
        pass

    # 上面的上下文管理，就是运行完with下面的语句后就自动关闭。等价于下面的语句
    f = open('ch5_文件与IO/sample.txt', 'wt')
    data = f.read()
    f.close()

    # 指定换行标志
    with open('ch5_文件与IO/sample.txt', 'wt') as f:
        pass



