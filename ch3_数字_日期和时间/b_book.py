
# 1、取整
if __name__ == '__main__':
    round(1.23, 1)  # 一位小数
    round(-1.27, 1)  # 一位小数

    round(1.5, )
    round(2.5)  # 取整到最近的偶数

    round(1234.5, -2)  # 负数是取整到十位

    # 在数值输出的时候注意不要混淆格式化和取整
    x = 1.2345
    format(x, '.2f')  # 没必要对x取整

    # 也不要采取取整的方式修正精度上的问题
    a = 2.1
    b = 4.2
    c = a + b

    c = round(c, 2)


# 2、执行精确的小数计算
if __name__ == '__main__':
    # 浮点数天生没法精确表达所有十进制小数位，
    a = 2.1
    b = 4.2
    c = a + b

    (a + b) == 6.3  # 傻逼了吧，不要轻易 == 一个数，
    '''
    这是由于底层CPU运算单元和IEEE754浮点数算数标准的一种特性，
    python的浮点数保存的数据是原始表示形式，
    '''

    from decimal import Decimal
    a = Decimal('4.2')
    b = Decimal('2.1')
    (a + b) == 6.3
    (a + b) == Decimal('6.3')

    # 限定精确度的环境
    from decimal import localcontext
    a = Decimal('1.3')
    b = Decimal('1.7')
    print(a / b)

    with localcontext() as ctx:
        ctx.prec = 3
        print(a / b)

    with localcontext() as ctx:
        ctx.prec = 50
        print(a / b)

    # python在处理超大数字的时候，相减抵消会出现问题
    nums = [1.23e+18, 1, -1.23e+18]
    sum(nums)

    import math
    math.fsum(nums)


# 数值的格式化输出
if __name__ == '__main__':
    x = 1234.45678

    format(x, '0.2f')
    f'{x:0.2f}'
    '{:0.2f}'.format(x)
    format(x, '.2f')
    f'{x:.2f}'
    format(x, '10.2f')
    f'{x:0.2f}'

    format(x, '>10.1f')  # 格式分成两块识别，>10 右对齐，.1f 保留以为小数的浮点数。同理，<左对齐 ^居中
    f'{x:>10.1f}'

    format(x, '0,.1f')  # 0 自然长度  , 带逗号

    format(x, 'e')  # 科学记数法


# 二进制、八进制和十六进制
if __name__ == '__main__':
    x = 1234

    bin(x)  # 二进制开头了0b
    oct(x)  # 八进制开头了0o
    hex(x)  # 十六进制开头了0x

    format(x, 'b')
    format(x, 'o')
    format(x, 'x')


# 复数运算
if __name__ == '__main__':
    a = complex(2, 4)
    b = 3 - 5j

    a.real
    a.imag

    # numpy的array可以直接使用复数


# 无穷大和NaN
if __name__ == '__main__':
    a = float('inf')  # python本身定义的
    b = float('-inf')
    c = float('nan')

    import math
    math.isinf(a)
    math.isinf(b)
    math.isnan(c)

    # python本身对nan采取传播而不是忽视的态度
    c + 10
    sum([1,2,3,c,5])


# 分数的计算
if __name__ == '__main__':
    from fractions import Fraction
    a = Fraction(5,4)
    b = Fraction(7, 16)
    print(a + b)


# numpy的一些简单规则
if __name__ == '__main__':
    # numpy适合于密集的计算任务，比list快很多。
    import numpy as np
    ax = np.array([1,2,3,4])
    ay = np.array([5,6,7,8])

    # +-*/基本四则运算是对应元素
    ax * 2
    ax + 10
    ax * ay
    ax += 10

    # 标量函数也是对每个元素
    np.sqrt(ax)
    np.cos(ax)

    # numpy的索引

    # numpy.where


# numpy的线性代数运算
if __name__ == '__main__':
    import numpy as np
    m = np.matrix([[1,-2,3], [0,4,5], [7,8,-9]])  # 最好有matrix类，不要用array类
    m.T
    m.I  # 求逆

    v = np.matrix([[2], [3], [4]])  # 列向量



    arr = np.array([[1,-2,3], [0,4,5], [7,8,-9]])
    arr.T