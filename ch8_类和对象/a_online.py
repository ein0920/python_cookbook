
# calling_a_method_on_a_parent_class
if __name__ == '__main__':
    class A:
        def spam(self):
            print('A.spam')


    class B(A):
        def spam(self):
            print('B.spam')
            super().spam()  # Call parent spam()


    if __name__ == '__main__':
        b = B()
        b.spam()

if __name__ == '__main__':
    class A:
        def __init__(self):
            self.x = 0


    class B(A):
        def __init__(self):
            super().__init__()
            self.y = 1


    if __name__ == '__main__':
        b = B()
        print(b.x, b.y)

if __name__ == '__main__':
    class Proxy:
        def __init__(self, obj):
            self._obj = obj

        # Delegate attribute lookup to internal obj
        def __getattr__(self, name):
            return getattr(self._obj, name)

        # Delegate attribute assignment
        def __setattr__(self, name, value):
            if name.startswith('_'):
                super().__setattr__(name, value)  # Call original __setattr__
            else:
                setattr(self._obj, name, value)


    if __name__ == '__main__':
        class A:
            def __init__(self, x):
                self.x = x

            def spam(self):
                print('A.spam')


        a = A(42)
        p = Proxy(a)
        print(p.x)
        print(p.spam())
        p.x = 37
        print('Should be 37:', p.x)
        print('Should be 37:', a.x)


if __name__ == '__main__':
    # Tricky initialization problem involving multiple inheritance.
    # Does NOT use super()

    class Base:
        def __init__(self):
            print('Base.__init__')


    class A(Base):
        def __init__(self):
            Base.__init__(self)
            print('A.__init__')


    class B(Base):
        def __init__(self):
            Base.__init__(self)
            print('B.__init__')


    class C(A, B):
        def __init__(self):
            A.__init__(self)
            B.__init__(self)
            print('C.__init__')


    if __name__ == '__main__':
        # Please observe double call of Base.__init__
        c = C()

if __name__ == '__main__':
    # Tricky initialization problem involving multiple inheritance.
    # Uses super()

    class Base:
        def __init__(self):
            print('Base.__init__')


    class A(Base):
        def __init__(self):
            super().__init__()
            print('A.__init__')


    class B(Base):
        def __init__(self):
            super().__init__()
            print('B.__init__')


    class C(A, B):
        def __init__(self):
            super().__init__()  # Only one call to super() here
            print('C.__init__')


    if __name__ == '__main__':
        # Observe that each class initialized only once
        c = C()


#calling_a_method_on_an_object_given_the_name_as_a_string
if __name__ == '__main__':
    # Example of calling methods by name

    import math


    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return 'Point({!r:},{!r:})'.format(self.x, self.y)

        def distance(self, x, y):
            return math.hypot(self.x - x, self.y - y)


    p = Point(2, 3)

    # Method 1 : Use getattr
    d = getattr(p, 'distance')(0, 0)  # Calls p.distance(0, 0)
    print(d)

    # Method 2: Use methodcaller
    import operator

    d = operator.methodcaller('distance', 0, 0)(p)
    print(d)

    # Application in sorting
    points = [
        Point(1, 2),
        Point(3, 0),
        Point(10, -3),
        Point(-5, -7),
        Point(-1, 8),
        Point(3, 2)
    ]

    # Sort by distance from origin (0, 0)
    points.sort(key=operator.methodcaller('distance', 0, 0))
    for p in points:
        print(p)


# changing_the_string_representation_of_instances
if __name__ == '__main__':
    class Pair:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return 'Pair({0.x!r}, {0.y!r})'.format(self)

        def __str__(self):
            return '({0.x}, {0.y})'.format(self)

# creating_a_new_kind_of_class_or_instance_attribute
if __name__ == '__main__':
    # Descriptor attribute for an integer type-checked attribute
    class Integer:
        def __init__(self, name):
            self.name = name

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                return instance.__dict__[self.name]

        def __set__(self, instance, value):
            if not isinstance(value, int):
                raise TypeError('Expected an int')
            instance.__dict__[self.name] = value

        def __delete__(self, instance):
            del instance.__dict__[self.name]


    class Point:
        x = Integer('x')
        y = Integer('y')

        def __init__(self, x, y):
            self.x = x
            self.y = y


    if __name__ == '__main__':
        p = Point(2, 3)
        print(p.x)
        p.y = 5
        try:
            p.x = 2.3
        except TypeError as e:
            print(e)

if __name__ == '__main__':
    # Descriptor for a type-checked attribute
    class Typed:
        def __init__(self, name, expected_type):
            self.name = name
            self.expected_type = expected_type

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                return instance.__dict__[self.name]

        def __set__(self, instance, value):
            if not isinstance(value, self.expected_type):
                raise TypeError('Expected ' + str(self.expected_type))
            instance.__dict__[self.name] = value

        def __delete__(self, instance):
            del instance.__dict__[self.name]


    # Class decorator that applies it to selected attributes
    def typeassert(**kwargs):
        def decorate(cls):
            for name, expected_type in kwargs.items():
                # Attach a Typed descriptor to the class
                setattr(cls, name, Typed(name, expected_type))
            return cls

        return decorate


    # Example use
    @typeassert(name=str, shares=int, price=float)
    class Stock:
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price


    if __name__ == '__main__':
        s = Stock('ACME', 100, 490.1)
        print(s.name, s.shares, s.price)
        s.shares = 50
        try:
            s.shares = 'a lot'
        except TypeError as e:
            print(e)


# creating_an_instance_without_invoking_init
if __name__ == '__main__':
    from time import localtime


    class Date:
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day

        # Class method that bypasses __init__
        @classmethod
        def today(cls):
            d = cls.__new__(cls)
            t = localtime()
            d.year = t.tm_year
            d.month = t.tm_mon
            d.day = t.tm_mday
            return d


    d = Date.__new__(Date)
    print(d)
    print(hasattr(d, 'year'))

    data = {
        'year': 2012,
        'month': 8,
        'day': 29
    }

    d.__dict__.update(data)
    print(d.year)
    print(d.month)

    d = Date.today()
    print(d.year, d.month, d.day)


# creating_cached_instances
if __name__ == '__main__':
    # Simple example

    class Spam:
        def __init__(self, name):
            self.name = name


    # Caching support
    import weakref

    _spam_cache = weakref.WeakValueDictionary()


    def get_spam(name):
        if name not in _spam_cache:
            s = Spam(name)
            _spam_cache[name] = s
        else:
            s = _spam_cache[name]
        return s


    if __name__ == '__main__':
        a = get_spam('foo')
        b = get_spam('bar')
        print('a is b:', a is b)
        c = get_spam('foo')
        print('a is c:', a is c)


if __name__ == '__main__':
    import weakref


    class CachedSpamManager:
        def __init__(self):
            self._cache = weakref.WeakValueDictionary()

        def get_spam(self, name):
            if name not in self._cache:
                s = Spam(name)
                self._cache[name] = s
            else:
                s = self._cache[name]
            return s


    class Spam:
        def __init__(self, name):
            self.name = name


    Spam.manager = CachedSpamManager()


    def get_spam(name):
        return Spam.manager.get_spam(name)


    if __name__ == '__main__':
        a = get_spam('foo')
        b = get_spam('bar')
        print('a is b:', a is b)
        c = get_spam('foo')
        print('a is c:', a is c)

if __name__ == '__main__':
    # Example involving new and some of its problems

    import weakref


    class Spam:
        _spam_cache = weakref.WeakValueDictionary()

        def __new__(cls, name):
            if name in cls._spam_cache:
                return cls._spam_cache[name]
            else:
                self = super().__new__(cls)
                cls._spam_cache[name] = self
                return self

        def __init__(self, name):
            print('Initializing Spam')
            self.name = name


    if __name__ == '__main__':
        print("This should print 'Initializing Spam' twice")
        s = Spam('Dave')
        t = Spam('Dave')
        print(s is t)


# creating_managed_attributes
if __name__ == '__main__':
    # Example of managed attributes via properties

    class Person:
        def __init__(self, first_name):
            self.first_name = first_name

        # Getter function
        @property
        def first_name(self):
            return self._first_name

        # Setter function
        @first_name.setter
        def first_name(self, value):
            if not isinstance(value, str):
                raise TypeError('Expected a string')
            self._first_name = value


    if __name__ == '__main__':
        a = Person('Guido')
        print(a.first_name)
        a.first_name = 'Dave'
        print(a.first_name)
        try:
            a.first_name = 42
        except TypeError as e:
            print(e)


# customized_formatting
if __name__ == '__main__':
    _formats = {
        'ymd': '{d.year}-{d.month}-{d.day}',
        'mdy': '{d.month}/{d.day}/{d.year}',
        'dmy': '{d.day}/{d.month}/{d.year}'
    }


    class Date:
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day

        def __format__(self, code):
            if code == '':
                code = 'ymd'
            fmt = _formats[code]
            return fmt.format(d=self)


# delegation_and_proxies
if __name__ == '__main__':
    class A:
        def spam(self, x):
            print('A.spam')

        def foo(self):
            print('A.foo')


    class B:
        def __init__(self):
            self._a = A()

        def bar(self):
            print('B.bar')

        # Expose all of the methods defined on class A
        def __getattr__(self, name):
            return getattr(self._a, name)


    if __name__ == '__main__':
        b = B()
        b.bar()
        b.spam(42)

if __name__ == '__main__':
    # A proxy class that wraps around another object, but
    # exposes its public attributes

    class Proxy:
        def __init__(self, obj):
            self._obj = obj

        # Delegate attribute lookup to internal obj
        def __getattr__(self, name):
            print('getattr:', name)
            return getattr(self._obj, name)

        # Delegate attribute assignment
        def __setattr__(self, name, value):
            if name.startswith('_'):
                super().__setattr__(name, value)
            else:
                print('setattr:', name, value)
                setattr(self._obj, name, value)

        # Delegate attribute deletion
        def __delattr__(self, name):
            if name.startswith('_'):
                super().__delattr__(name)
            else:
                print('delattr:', name)
                delattr(self._obj, name)


    if __name__ == '__main__':
        class Spam:
            def __init__(self, x):
                self.x = x

            def bar(self, y):
                print('Spam.bar:', self.x, y)


        # Create an instance
        s = Spam(2)

        # Create a proxy around it
        p = Proxy(s)

        # Access the proxy
        print(p.x)  # Outputs 2
        p.bar(3)  # Outputs "Spam.bar: 2 3"
        p.x = 37  # Changes s.x to 37

if __name__ == '__main__':
    class ListLike:
        def __init__(self):
            self._items = []

        def __getattr__(self, name):
            return getattr(self._items, name)

        # Added special methods to support certain list operations
        def __len__(self):
            return len(self._items)

        def __getitem__(self, index):
            return self._items[index]

        def __setitem__(self, index, value):
            self._items[index] = value

        def __delitem__(self, index):
            del self._items[index]


    if __name__ == '__main__':
        a = ListLike()
        a.append(2)
        a.insert(0, 1)
        a.sort()
        print(len(a))
        print(a[0])


if __name__ == '__main__':
    class A:
        def spam(self):
            print('A.spam')

        def foo(self):
            print('A.foo')


    class B:
        def __init__(self):
            self._a = A()

        def spam(self):
            print('B.spam')
            self._a.spam()  # Similar to super()

        def __getattr__(self, name):
            return getattr(self._a, name)


    if __name__ == '__main__':
        b = B()
        b.spam()
        b.foo()

# extending_a_property_in_a_subclass
if __name__ == '__main__':
    # Example of managed attributes via properties

    class Person:
        def __init__(self, name):
            self.name = name

        # Getter function
        @property
        def name(self):
            return self._name

        # Setter function
        @name.setter
        def name(self, value):
            if not isinstance(value, str):
                raise TypeError('Expected a string')
            self._name = value

        @name.deleter
        def name(self):
            raise AttributeError("Can't delete attribute")


    class SubPerson(Person):
        @property
        def name(self):
            print('Getting name')
            return super().name

        @name.setter
        def name(self, value):
            print('Setting name to', value)
            super(SubPerson, SubPerson).name.__set__(self, value)

        @name.deleter
        def name(self):
            print('Deleting name')
            super(SubPerson, SubPerson).name.__delete__(self)


    class SubPerson2(Person):
        @Person.name.setter
        def name(self, value):
            print('Setting name to', value)
            super(SubPerson2, SubPerson2).name.__set__(self, value)


    class SubPerson3(Person):
        # @property
        @Person.name.getter
        def name(self):
            print('Getting name')
            return super().name


    if __name__ == '__main__':
        a = Person('Guido')
        print(a.name)
        a.name = 'Dave'
        print(a.name)
        try:
            a.name = 42
        except TypeError as e:
            print(e)

if __name__ == '__main__':
    # Example of managed attributes via properties

    class String:
        def __init__(self, name):
            self.name = name

        def __get__(self, instance, cls):
            if instance is None:
                return self
            return instance.__dict__[self.name]

        def __set__(self, instance, value):
            if not isinstance(value, str):
                raise TypeError('Expected a string')
            instance.__dict__[self.name] = value


    class Person:
        name = String('name')

        def __init__(self, name):
            self.name = name


    class SubPerson(Person):
        @property
        def name(self):
            print('Getting name')
            return super().name

        @name.setter
        def name(self, value):
            print('Setting name to', value)
            super(SubPerson, SubPerson).name.__set__(self, value)

        @name.deleter
        def name(self):
            print('Deleting name')
            super(SubPerson, SubPerson).name.__delete__(self)


    if __name__ == '__main__':
        a = Person('Guido')
        print(a.name)
        a.name = 'Dave'
        print(a.name)
        try:
            a.name = 42
        except TypeError as e:
            print(e)

# extending_classes_with_mixins
if __name__ == '__main__':
    class LoggedMappingMixin:
        '''
        Add logging to get/set/delete operations for debugging.
        '''
        __slots__ = ()

        def __getitem__(self, key):
            print('Getting ' + str(key))
            return super().__getitem__(key)

        def __setitem__(self, key, value):
            print('Setting {} = {!r}'.format(key, value))
            return super().__setitem__(key, value)

        def __delitem__(self, key):
            print('Deleting ' + str(key))
            return super().__delitem__(key)


    class SetOnceMappingMixin:
        '''
        Only allow a key to be set once.
        '''
        __slots__ = ()

        def __setitem__(self, key, value):
            if key in self:
                raise KeyError(str(key) + ' already set')
            return super().__setitem__(key, value)


    class StringKeysMappingMixin:
        '''
        Restrict keys to strings only
        '''
        __slots__ = ()

        def __setitem__(self, key, value):
            if not isinstance(key, str):
                raise TypeError('keys must be strings')
            return super().__setitem__(key, value)


    # Examples

    print('# ---- LoggedDict Example')


    class LoggedDict(LoggedMappingMixin, dict):
        pass


    d = LoggedDict()
    d['x'] = 23
    print(d['x'])
    del d['x']

    print('# ---- SetOnceDefaultDict Example')

    from collections import defaultdict


    class SetOnceDefaultDict(SetOnceMappingMixin, defaultdict):
        pass


    d = SetOnceDefaultDict(list)
    d['x'].append(2)
    d['y'].append(3)
    d['x'].append(10)
    try:
        d['x'] = 23
    except KeyError as e:
        print(e)

    print('# ---- StringOrderedDict Example')
    from collections import OrderedDict


    class StringOrderedDict(StringKeysMappingMixin,
                            SetOnceMappingMixin,
                            OrderedDict):
        pass


    d = StringOrderedDict()
    d['x'] = 23
    try:
        d[42] = 10
    except TypeError as e:
        print(e)

    try:
        d['x'] = 42
    except KeyError as e:
        print(e)

if __name__ == '__main__':
    class RestrictKeysMixin:
        def __init__(self, *args, _restrict_key_type, **kwargs):
            self.__restrict_key_type = _restrict_key_type
            super().__init__(*args, **kwargs)

        def __setitem__(self, key, value):
            if not isinstance(key, self.__restrict_key_type):
                raise TypeError('Keys must be ' + str(self.__restrict_key_type))
            super().__setitem__(key, value)


    # Example

    class RDict(RestrictKeysMixin, dict):
        pass


    d = RDict(_restrict_key_type=str)
    e = RDict([('name', 'Dave'), ('n', 37)], _restrict_key_type=str)
    f = RDict(name='Dave', n=37, _restrict_key_type=str)
    print(f)
    try:
        f[42] = 10
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    # Class decorator alternative to mixins

    def LoggedMapping(cls):
        cls_getitem = cls.__getitem__
        cls_setitem = cls.__setitem__
        cls_delitem = cls.__delitem__

        def __getitem__(self, key):
            print('Getting %s' % key)
            return cls_getitem(self, key)

        def __setitem__(self, key, value):
            print('Setting %s = %r' % (key, value))
            return cls_setitem(self, key, value)

        def __delitem__(self, key):
            print('Deleting %s' % key)
            return cls_delitem(self, key)

        cls.__getitem__ = __getitem__
        cls.__setitem__ = __setitem__
        cls.__delitem__ = __delitem__
        return cls


    @LoggedMapping
    class LoggedDict(dict):
        pass


    d = LoggedDict()
    d['x'] = 23
    print(d['x'])
    del d['x']

# how_to_define_an_interface_or_abstract_base_class
if __name__ == '__main__':
    # Defining a simple abstract base class

    from abc import ABCMeta, abstractmethod


    class IStream(metaclass=ABCMeta):
        @abstractmethod
        def read(self, maxbytes=-1):
            pass

        @abstractmethod
        def write(self, data):
            pass


    # Example implementation
    class SocketStream(IStream):
        def read(self, maxbytes=-1):
            print('reading')

        def write(self, data):
            print('writing')


    # Example of type checking
    def serialize(obj, stream):
        if not isinstance(stream, IStream):
            raise TypeError('Expected an IStream')
        print('serializing')


    # Examples
    if __name__ == '__main__':
        # Attempt to instantiate ABC directly (doesn't work)
        try:
            a = IStream()
        except TypeError as e:
            print(e)

        # Instantiation of a concrete implementation
        a = SocketStream()
        a.read()
        a.write('data')

        # Passing to type-check function
        serialize(None, a)

        # Attempt to pass a file-like object to serialize (fails)
        import sys

        try:
            serialize(None, sys.stdout)
        except TypeError as e:
            print(e)

        # Register file streams and retry
        import io

        IStream.register(io.IOBase)

        serialize(None, sys.stdout)



if __name__ == '__main__':
    from abc import ABCMeta, abstractmethod


    class A(metaclass=ABCMeta):
        @property
        @abstractmethod
        def name(self):
            pass

        @name.setter
        @abstractmethod
        def name(self, value):
            pass

        @classmethod
        @abstractmethod
        def method1(cls):
            pass

        @staticmethod
        @abstractmethod
        def method2():
            pass

#how_to_define_more_than_one_constructor_in_a_class
if __name__ == '__main__':
    import time


    class Date:
        # Primary constructor
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day

        # Alternate constructor
        @classmethod
        def today(cls):
            t = time.localtime()
            return cls(t.tm_year, t.tm_mon, t.tm_mday)


    if __name__ == '__main__':
        a = Date(2012, 12, 21)
        b = Date.today()
        print(a.year, a.month, a.day)
        print(b.year, b.month, b.day)


        class NewDate(Date):
            pass


        c = Date.today()
        d = NewDate.today()
        print('Should be Date instance:', Date)
        print('Should be NewDate instance:', NewDate)

if __name__ == '__main__':
    import time


    class Date:
        # Primary constructor
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day

        # Alternate constructor
        @classmethod
        def today(cls):
            t = time.localtime()
            d = cls.__new__(cls)
            d.year = t.tm_year
            d.month = t.tm_mon
            d.day = t.tm_mday
            return d


    if __name__ == '__main__':
        a = Date(2012, 12, 21)
        b = Date.today()
        print(a.year, a.month, a.day)
        print(b.year, b.month, b.day)


        class NewDate(Date):
            pass


        c = Date.today()
        d = NewDate.today()
        print('Should be Date instance:', Date)
        print('Should be NewDate instance:', NewDate)

# how_to_encapsulate_names_in_a_class
if __name__ == '__main__':
    # Example of using __ method name to implement a
    # non-overrideable method

    class B:
        def __init__(self):
            self.__private = 0

        def __private_method(self):
            print('B.__private_method', self.__private)

        def public_method(self):
            self.__private_method()


    class C(B):
        def __init__(self):
            super().__init__()
            self.__private = 1  # Does not override B.__private

        # Does not override B.__private_method()
        def __private_method(self):
            print('C.__private_method')


    c = C()
    c.public_method()


# implementing_a_data_model_or_type_system
if __name__ == '__main__':
    # Base class. Uses a descriptor to set a value
    class Descriptor:
        def __init__(self, name=None, **opts):
            self.name = name
            self.__dict__.update(opts)

        def __set__(self, instance, value):
            instance.__dict__[self.name] = value


    # Descriptor for enforcing types
    class Typed(Descriptor):
        expected_type = type(None)

        def __set__(self, instance, value):
            if not isinstance(value, self.expected_type):
                raise TypeError('expected ' + str(self.expected_type))
            super().__set__(instance, value)


    # Descriptor for enforcing values
    class Unsigned(Descriptor):
        def __set__(self, instance, value):
            if value < 0:
                raise ValueError('Expected >= 0')
            super().__set__(instance, value)


    class MaxSized(Descriptor):
        def __init__(self, name=None, **opts):
            if 'size' not in opts:
                raise TypeError('missing size option')
            self.size = opts['size']
            super().__init__(name, **opts)

        def __set__(self, instance, value):
            if len(value) >= self.size:
                raise ValueError('size must be < ' + str(self.size))
            super().__set__(instance, value)


    class Integer(Typed):
        expected_type = int


    class UnsignedInteger(Integer, Unsigned):
        pass


    class Float(Typed):
        expected_type = float


    class UnsignedFloat(Float, Unsigned):
        pass


    class String(Typed):
        expected_type = str


    class SizedString(String, MaxSized):
        pass


    # Class decorator to apply constraints
    def check_attributes(**kwargs):
        def decorate(cls):
            for key, value in kwargs.items():
                if isinstance(value, Descriptor):
                    value.name = key
                    setattr(cls, key, value)
                else:
                    setattr(cls, key, value(key))
            return cls

        return decorate


    # A metaclass that applies checking
    class checkedmeta(type):
        def __new__(cls, clsname, bases, methods):
            # Attach attribute names to the descriptors
            for key, value in methods.items():
                if isinstance(value, Descriptor):
                    value.name = key
            return type.__new__(cls, clsname, bases, methods)


    # Testing code
    def test(s):
        print(s.name)
        s.shares = 75
        print(s.shares)
        try:
            s.shares = -10
        except ValueError as e:
            print(e)
        try:
            s.price = 'a lot'
        except TypeError as e:
            print(e)

        try:
            s.name = 'ABRACADABRA'
        except ValueError as e:
            print(e)


    # Various Examples:
    if __name__ == '__main__':
        print("# --- Class with descriptors")


        class Stock:
            # Specify constraints
            name = SizedString('name', size=8)
            shares = UnsignedInteger('shares')
            price = UnsignedFloat('price')

            def __init__(self, name, shares, price):
                self.name = name
                self.shares = shares
                self.price = price


        s = Stock('ACME', 50, 91.1)
        test(s)

        print("# --- Class with class decorator")


        @check_attributes(name=SizedString(size=8),
                          shares=UnsignedInteger,
                          price=UnsignedFloat)
        class Stock:
            def __init__(self, name, shares, price):
                self.name = name
                self.shares = shares
                self.price = price


        s = Stock('ACME', 50, 91.1)
        test(s)

        print("# --- Class with metaclass")


        class Stock(metaclass=checkedmeta):
            name = SizedString(size=8)
            shares = UnsignedInteger()
            price = UnsignedFloat()

            def __init__(self, name, shares, price):
                self.name = name
                self.shares = shares
                self.price = price


        s = Stock('ACME', 50, 91.1)
        test(s)

if __name__ == '__main__':
    # Base class. Uses a descriptor to set a value
    class Descriptor:
        def __init__(self, name=None, **opts):
            self.name = name
            self.__dict__.update(opts)

        def __set__(self, instance, value):
            instance.__dict__[self.name] = value


    def Typed(expected_type, cls=None):
        if cls is None:
            return lambda cls: Typed(expected_type, cls)

        super_set = cls.__set__

        def __set__(self, instance, value):
            if not isinstance(value, expected_type):
                raise TypeError('expected ' + str(expected_type))
            super_set(self, instance, value)

        cls.__set__ = __set__
        return cls


    def Unsigned(cls):
        super_set = cls.__set__

        def __set__(self, instance, value):
            if value < 0:
                raise ValueError('Expected >= 0')
            super_set(self, instance, value)

        cls.__set__ = __set__
        return cls


    def MaxSized(cls):
        super_init = cls.__init__

        def __init__(self, name=None, **opts):
            if 'size' not in opts:
                raise TypeError('missing size option')
            self.size = opts['size']
            super_init(self, name, **opts)

        cls.__init__ = __init__

        super_set = cls.__set__

        def __set__(self, instance, value):
            if len(value) >= self.size:
                raise ValueError('size must be < ' + str(self.size))
            super_set(self, instance, value)

        cls.__set__ = __set__
        return cls


    @Typed(int)
    class Integer(Descriptor):
        pass


    @Unsigned
    class UnsignedInteger(Integer):
        pass


    @Typed(float)
    class Float(Descriptor):
        pass


    @Unsigned
    class UnsignedFloat(Float):
        pass


    @Typed(str)
    class String(Descriptor):
        pass


    @MaxSized
    class SizedString(String):
        pass


    # Class decorator to apply constraints
    def check_attributes(**kwargs):
        def decorate(cls):
            for key, value in kwargs.items():
                if isinstance(value, Descriptor):
                    value.name = key
                    setattr(cls, key, value)
                else:
                    setattr(cls, key, value(key))
            return cls

        return decorate


    # A metaclass that applies checking
    class checkedmeta(type):
        def __new__(cls, clsname, bases, methods):
            # Attach attribute names to the descriptors
            for key, value in methods.items():
                if isinstance(value, Descriptor):
                    value.name = key
            return type.__new__(cls, clsname, bases, methods)


    # Testing code
    def test(s):
        print(s.name)
        s.shares = 75
        print(s.shares)
        try:
            s.shares = -10
        except ValueError as e:
            print(e)
        try:
            s.price = 'a lot'
        except TypeError as e:
            print(e)

        try:
            s.name = 'ABRACADABRA'
        except ValueError as e:
            print(e)


    # Various Examples:
    if __name__ == '__main__':
        print("# --- Class with descriptors")


        class Stock:
            # Specify constraints
            name = SizedString('name', size=8)
            shares = UnsignedInteger('shares')
            price = UnsignedFloat('price')

            def __init__(self, name, shares, price):
                self.name = name
                self.shares = shares
                self.price = price


        s = Stock('ACME', 50, 91.1)
        test(s)

        print("# --- Class with class decorator")


        @check_attributes(name=SizedString(size=8),
                          shares=UnsignedInteger,
                          price=UnsignedFloat)
        class Stock:
            def __init__(self, name, shares, price):
                self.name = name
                self.shares = shares
                self.price = price


        s = Stock('ACME', 50, 91.1)
        test(s)

        print("# --- Class with metaclass")


        class Stock(metaclass=checkedmeta):
            name = SizedString(size=8)
            shares = UnsignedInteger()
            price = UnsignedFloat()

            def __init__(self, name, shares, price):
                self.name = name
                self.shares = shares
                self.price = price


        s = Stock('ACME', 50, 91.1)
        test(s)


# implementing_custom_containers
if __name__ == '__main__':
    # Example of a custom container

    import collections
    import bisect


    class SortedItems(collections.Sequence):
        def __init__(self, initial=None):
            self._items = sorted(initial) if initial is not None else []

        # Required sequence methods
        def __getitem__(self, index):
            return self._items[index]

        def __len__(self):
            return len(self._items)

        # Method for adding an item in the right location
        def add(self, item):
            bisect.insort(self._items, item)


    if __name__ == '__main__':
        items = SortedItems([5, 1, 3])
        print(list(items))
        print(items[0])
        print(items[-1])
        items.add(2)
        print(list(items))
        items.add(-10)
        print(list(items))
        print(items[1:4])
        print(3 in items)
        print(len(items))
        for n in items:
            print(n)
if __name__ == '__main__':
    import collections


    class Items(collections.MutableSequence):
        def __init__(self, initial=None):
            self._items = list(initial) if initial is not None else []

        # Required sequence methods
        def __getitem__(self, index):
            print('Getting:', index)
            return self._items[index]

        def __setitem__(self, index, value):
            print('Setting:', index, value)
            self._items[index] = value

        def __delitem__(self, index):
            print('Deleting:', index)
            del self._items[index]

        def insert(self, index, value):
            print('Inserting:', index, value)
            self._items.insert(index, value)

        def __len__(self):
            print('Len')
            return len(self._items)


    if __name__ == '__main__':
        a = Items([1, 2, 3])
        print(len(a))
        a.append(4)
        a.append(2)
        print(a.count(2))
        a.remove(3)

# implementing_stateful_objects_or_state_machines
if __name__ == '__main__':
    class Connection:
        def __init__(self):
            self.new_state(ClosedConnection)

        def new_state(self, state):
            self.__class__ = state

        def read(self):
            raise NotImplementedError()

        def write(self, data):
            raise NotImplementedError()

        def open(self):
            raise NotImplementedError()

        def close(self):
            raise NotImplementedError()


    class ClosedConnection(Connection):
        def read(self):
            raise RuntimeError('Not open')

        def write(self, data):
            raise RuntimeError('Not open')

        def open(self):
            self.new_state(OpenConnection)

        def close(self):
            raise RuntimeError('Already closed')


    class OpenConnection(Connection):
        def read(self):
            print('reading')

        def write(self, data):
            print('writing')

        def open(self):
            raise RuntimeError('Already open')

        def close(self):
            self.new_state(ClosedConnection)


    # Example
    if __name__ == '__main__':
        c = Connection()
        print(c)
        try:
            c.read()
        except RuntimeError as e:
            print(e)

        c.open()
        print(c)
        c.read()
        c.close()
        print(c)

if __name__ == '__main__':
    class Connection:
        def __init__(self):
            self.new_state(ClosedConnectionState)

        def new_state(self, newstate):
            self._state = newstate

        # Delegate to the state class
        def read(self):
            return self._state.read(self)

        def write(self, data):
            return self._state.write(self, data)

        def open(self):
            return self._state.open(self)

        def close(self):
            return self._state.close(self)


    # Connection state base class
    class ConnectionState:
        @staticmethod
        def read(conn):
            raise NotImplementedError()

        @staticmethod
        def write(conn, data):
            raise NotImplementedError()

        @staticmethod
        def open(conn):
            raise NotImplementedError()

        @staticmethod
        def close(conn):
            raise NotImplementedError()


    # Implementation of different states
    class ClosedConnectionState(ConnectionState):
        @staticmethod
        def read(conn):
            raise RuntimeError('Not open')

        @staticmethod
        def write(conn, data):
            raise RuntimeError('Not open')

        @staticmethod
        def open(conn):
            conn.new_state(OpenConnectionState)

        @staticmethod
        def close(conn):
            raise RuntimeError('Already closed')


    class OpenConnectionState(ConnectionState):
        @staticmethod
        def read(conn):
            print('reading')

        @staticmethod
        def write(conn, data):
            print('writing')

        @staticmethod
        def open(conn):
            raise RuntimeError('Already open')

        @staticmethod
        def close(conn):
            conn.new_state(ClosedConnectionState)


    # Example
    if __name__ == '__main__':
        c = Connection()
        print(c)
        try:
            c.read()
        except RuntimeError as e:
            print(e)

        c.open()
        print(c)
        c.read()
        c.close()
        print(c)

# implementing_the_visitor_pattern
if __name__ == '__main__':
    # Example of the visitor pattern

    # --- The following classes represent nodes in an expression tree
    class Node:
        pass


    class UnaryOperator(Node):
        def __init__(self, operand):
            self.operand = operand


    class BinaryOperator(Node):
        def __init__(self, left, right):
            self.left = left
            self.right = right


    class Add(BinaryOperator):
        pass


    class Sub(BinaryOperator):
        pass


    class Mul(BinaryOperator):
        pass


    class Div(BinaryOperator):
        pass


    class Negate(UnaryOperator):
        pass


    class Number(Node):
        def __init__(self, value):
            self.value = value


    # --- The visitor base class

    class NodeVisitor:
        def visit(self, node):
            methname = 'visit_' + type(node).__name__
            meth = getattr(self, methname, None)
            if meth is None:
                meth = self.generic_visit
            return meth(node)

        def generic_visit(self, node):
            raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))


    # --- Example 1:  An expression evaluator

    class Evaluator(NodeVisitor):
        def visit_Number(self, node):
            return node.value

        def visit_Add(self, node):
            return self.visit(node.left) + self.visit(node.right)

        def visit_Sub(self, node):
            return self.visit(node.left) - self.visit(node.right)

        def visit_Mul(self, node):
            return self.visit(node.left) * self.visit(node.right)

        def visit_Div(self, node):
            return self.visit(node.left) / self.visit(node.right)

        def visit_Negate(self, node):
            return -node.operand


    # --- Example 2: Generate stack instructions

    class StackCode(NodeVisitor):
        def generate_code(self, node):
            self.instructions = []
            self.visit(node)
            return self.instructions

        def visit_Number(self, node):
            self.instructions.append(('PUSH', node.value))

        def binop(self, node, instruction):
            self.visit(node.left)
            self.visit(node.right)
            self.instructions.append((instruction,))

        def visit_Add(self, node):
            self.binop(node, 'ADD')

        def visit_Sub(self, node):
            self.binop(node, 'SUB')

        def visit_Mul(self, node):
            self.binop(node, 'MUL')

        def visit_Div(self, node):
            self.binop(node, 'DIV')

        def unaryop(self, node, instruction):
            self.visit(node.operand)
            self.instructions.append((instruction,))

        def visit_Negate(self, node):
            self.unaryop(node, 'NEG')


    # --- Example of the above classes in action

    # Representation of 1 + 2 * (3 - 4) / 5
    t1 = Sub(Number(3), Number(4))
    t2 = Mul(Number(2), t1)
    t3 = Div(t2, Number(5))
    t4 = Add(Number(1), t3)

    e = Evaluator()
    print('Should get 0.6 :', e.visit(t4))

    s = StackCode()
    code = s.generate_code(t4)
    for c in code:
        print(c)

# implementing_the_visitor_pattern_without_recursion
if __name__ == '__main__':
    # Example:  Recursive implementation

    from node import Node, NodeVisitor


    class UnaryOperator(Node):
        def __init__(self, operand):
            self.operand = operand


    class BinaryOperator(Node):
        def __init__(self, left, right):
            self.left = left
            self.right = right


    class Add(BinaryOperator):
        pass


    class Sub(BinaryOperator):
        pass


    class Mul(BinaryOperator):
        pass


    class Div(BinaryOperator):
        pass


    class Negate(UnaryOperator):
        pass


    class Number(Node):
        def __init__(self, value):
            self.value = value


    # A sample visitor class that evaluates expressions
    class Evaluator(NodeVisitor):
        def visit_Number(self, node):
            return node.value

        def visit_Add(self, node):
            return self.visit(node.left) + self.visit(node.right)

        def visit_Sub(self, node):
            return self.visit(node.left) - self.visit(node.right)

        def visit_Mul(self, node):
            return self.visit(node.left) * self.visit(node.right)

        def visit_Div(self, node):
            return self.visit(node.left) / self.visit(node.right)

        def visit_Negate(self, node):
            return -self.visit(node.operand)


    if __name__ == '__main__':
        # 1 + 2*(3-4) / 5
        t1 = Sub(Number(3), Number(4))
        t2 = Mul(Number(2), t1)
        t3 = Div(t2, Number(5))
        t4 = Add(Number(1), t3)

        # Evaluate it
        e = Evaluator()
        print(e.visit(t4))  # Outputs 0.6

        # Blow it up

        a = Number(0)
        for n in range(1, 100000):
            a = Add(a, Number(n))

        try:
            print(e.visit(a))
        except RuntimeError as e:
            print(e)

if __name__ == '__main__':
    # Example:  Non-recursive implementation using yield

    from node import Node, NodeVisitor


    class UnaryOperator(Node):
        def __init__(self, operand):
            self.operand = operand


    class BinaryOperator(Node):
        def __init__(self, left, right):
            self.left = left
            self.right = right


    class Add(BinaryOperator):
        pass


    class Sub(BinaryOperator):
        pass


    class Mul(BinaryOperator):
        pass


    class Div(BinaryOperator):
        pass


    class Negate(UnaryOperator):
        pass


    class Number(Node):
        def __init__(self, value):
            self.value = value


    class Evaluator(NodeVisitor):
        def visit_Number(self, node):
            return node.value

        def visit_Add(self, node):
            yield (yield node.left) + (yield node.right)

        def visit_Sub(self, node):
            yield (yield node.left) - (yield node.right)

        def visit_Mul(self, node):
            yield (yield node.left) * (yield node.right)

        def visit_Div(self, node):
            yield (yield node.left) / (yield node.right)

        def visit_Negate(self, node):
            yield -(yield node.operand)


    if __name__ == '__main__':
        # 1 + 2*(3-4) / 5
        t1 = Sub(Number(3), Number(4))
        t2 = Mul(Number(2), t1)
        t3 = Div(t2, Number(5))
        t4 = Add(Number(1), t3)

        # Evaluate it
        e = Evaluator()
        print(e.visit(t4))  # Outputs 0.6

        # Blow it up

        a = Number(0)
        for n in range(1, 100000):
            a = Add(a, Number(n))

        try:
            print(e.visit(a))
        except RuntimeError as e:
            print(e)

if __name__ == '__main__':
    # Example:  Modified non-recursive implementation using
    # a special Visit() class to signal what should be visited next

    import types


    class Node:
        pass


    class Visit:
        def __init__(self, node):
            self.node = node


    class NodeVisitor:
        def visit(self, node):
            stack = [Visit(node)]
            last_result = None
            while stack:
                try:
                    last = stack[-1]
                    if isinstance(last, types.GeneratorType):
                        stack.append(last.send(last_result))
                        last_result = None
                    elif isinstance(last, Visit):
                        stack.append(self._visit(stack.pop().node))
                    else:
                        last_result = stack.pop()
                except StopIteration:
                    stack.pop()
            return last_result

        def _visit(self, node):
            methname = 'visit_' + type(node).__name__
            meth = getattr(self, methname, None)
            if meth is None:
                meth = self.generic_visit
            return meth(node)

        def generic_visit(self, node):
            raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))


    class UnaryOperator(Node):
        def __init__(self, operand):
            self.operand = operand


    class BinaryOperator(Node):
        def __init__(self, left, right):
            self.left = left
            self.right = right


    class Add(BinaryOperator):
        pass


    class Sub(BinaryOperator):
        pass


    class Mul(BinaryOperator):
        pass


    class Div(BinaryOperator):
        pass


    class Negate(UnaryOperator):
        pass


    class Number(Node):
        def __init__(self, value):
            self.value = value


    class Evaluator(NodeVisitor):
        def visit_Number(self, node):
            return node.value

        def visit_Add(self, node):
            yield (yield Visit(node.left)) + (yield Visit(node.right))

        def visit_Sub(self, node):
            yield (yield Visit(node.left)) - (yield Visit(node.right))

        def visit_Mul(self, node):
            yield (yield Visit(node.left)) * (yield Visit(node.right))

        def visit_Div(self, node):
            yield (yield Visit(node.left)) / (yield Visit(node.right))

        def visit_Negate(self, node):
            yield -(yield Visit(node.operand))


    if __name__ == '__main__':
        # 1 + 2*(3-4) / 5
        t1 = Sub(Number(3), Number(4))
        t2 = Mul(Number(2), t1)
        t3 = Div(t2, Number(5))
        t4 = Add(Number(1), t3)

        # Evaluate it
        e = Evaluator()
        print(e.visit(t4))  # Outputs 0.6

        # Blow it up

        a = Number(0)
        for n in range(1, 100000):
            a = Add(a, Number(n))

        try:
            print(e.visit(a))
        except RuntimeError as e:
            print(e)

# lazily_computed_attributes
if __name__ == '__main__':
    class lazyproperty:
        def __init__(self, func):
            self.func = func

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                value = self.func(instance)
                setattr(instance, self.func.__name__, value)
                return value


    if __name__ == '__main__':
        import math


        class Circle:
            def __init__(self, radius):
                self.radius = radius

            @lazyproperty
            def area(self):
                print('Computing area')
                return math.pi * self.radius ** 2

            @lazyproperty
            def perimeter(self):
                print('Computing perimeter')
                return 2 * math.pi * self.radius

if __name__ == '__main__':
    def lazyproperty(func):
        name = '_lazy_' + func.__name__

        @property
        def lazy(self):
            if hasattr(self, name):
                return getattr(self, name)
            else:
                value = func(self)
                setattr(self, name, value)
                return value

        return lazy


    if __name__ == '__main__':
        import math


        class Circle:
            def __init__(self, radius):
                self.radius = radius

            @lazyproperty
            def area(self):
                print('Computing area')
                return math.pi * self.radius ** 2

            @lazyproperty
            def perimeter(self):
                print('Computing perimeter')
                return 2 * math.pi * self.radius


# making_classes_support_comparison_operations
if __name__ == '__main__':
    from functools import total_ordering


    class Room:
        def __init__(self, name, length, width):
            self.name = name
            self.length = length
            self.width = width
            self.square_feet = self.length * self.width


    @total_ordering
    class House:
        def __init__(self, name, style):
            self.name = name
            self.style = style
            self.rooms = list()

        @property
        def living_space_footage(self):
            return sum(r.square_feet for r in self.rooms)

        def add_room(self, room):
            self.rooms.append(room)

        def __str__(self):
            return '{}: {} square foot {}'.format(self.name,
                                                  self.living_space_footage,
                                                  self.style)

        def __eq__(self, other):
            return self.living_space_footage == other.living_space_footage

        def __lt__(self, other):
            return self.living_space_footage < other.living_space_footage

            # Build a few houses, and add rooms to them.


    h1 = House('h1', 'Cape')
    h1.add_room(Room('Master Bedroom', 14, 21))
    h1.add_room(Room('Living Room', 18, 20))
    h1.add_room(Room('Kitchen', 12, 16))
    h1.add_room(Room('Office', 12, 12))

    h2 = House('h2', 'Ranch')
    h2.add_room(Room('Master Bedroom', 14, 21))
    h2.add_room(Room('Living Room', 18, 20))
    h2.add_room(Room('Kitchen', 12, 16))

    h3 = House('h3', 'Split')
    h3.add_room(Room('Master Bedroom', 14, 21))
    h3.add_room(Room('Living Room', 18, 20))
    h3.add_room(Room('Office', 12, 16))
    h3.add_room(Room('Kitchen', 15, 17))
    houses = [h1, h2, h3]

    print("Is h1 bigger than h2?", h1 > h2)  # prints True
    print("Is h2 smaller than h3?", h2 < h3)  # prints True
    print("Is h2 greater than or equal to h1?", h2 >= h1)  # prints False
    print("Which one is biggest?", max(houses))  # prints 'h3: 1101 square foot Split'
    print("Which is smallest?", min(houses))  # prints 'h2: 846 square foot Ranch'


# making_objects_support_the_context_manager_protocol
if __name__ == '__main__':
    from socket import socket, AF_INET, SOCK_STREAM


    class LazyConnection:
        def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
            self.address = address
            self.family = AF_INET
            self.type = SOCK_STREAM
            self.sock = None

        def __enter__(self):
            if self.sock is not None:
                raise RuntimeError('Already connected')
            self.sock = socket(self.family, self.type)
            self.sock.connect(self.address)
            return self.sock

        def __exit__(self, exc_ty, exc_val, tb):
            self.sock.close()
            self.sock = None


    if __name__ == '__main__':
        from functools import partial

        c = LazyConnection(('www.python.org', 80))
        # Connection closed
        with c as s:
            # c.__enter__() executes: connection open
            s.send(b'GET /index.html HTTP/1.0\r\n')
            s.send(b'Host: www.python.org\r\n')
            s.send(b'\r\n')
            resp = b''.join(iter(partial(s.recv, 8192), b''))
            # c.__exit__() executes: connection closed

        print('Got %d bytes' % len(resp))

if __name__ == '__main__':
    from socket import socket, AF_INET, SOCK_STREAM


    class LazyConnection:
        def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
            self.address = address
            self.family = AF_INET
            self.type = SOCK_STREAM
            self.connections = []

        def __enter__(self):
            sock = socket(self.family, self.type)
            sock.connect(self.address)
            self.connections.append(sock)
            return sock

        def __exit__(self, exc_ty, exc_val, tb):
            self.connections.pop().close()


    if __name__ == '__main__':
        # Example use
        from functools import partial

        conn = LazyConnection(('www.python.org', 80))
        with conn as s:
            s.send(b'GET /index.html HTTP/1.0\r\n')
            s.send(b'Host: www.python.org\r\n')
            s.send(b'\r\n')
            resp = b''.join(iter(partial(s.recv, 8192), b''))

        print('Got %d bytes' % len(resp))

        with conn as s1, conn as s2:
            s1.send(b'GET /downloads HTTP/1.0\r\n')
            s2.send(b'GET /index.html HTTP/1.0\r\n')
            s1.send(b'Host: www.python.org\r\n')
            s2.send(b'Host: www.python.org\r\n')
            s1.send(b'\r\n')
            s2.send(b'\r\n')
            resp1 = b''.join(iter(partial(s1.recv, 8192), b''))
            resp2 = b''.join(iter(partial(s2.recv, 8192), b''))

        print('resp1 got %d bytes' % len(resp1))
        print('resp2 got %d bytes' % len(resp2))

# managing_memory_in_cyclic_data_structures
if __name__ == '__main__':
    import weakref


    class Node:
        def __init__(self, value):
            self.value = value
            self._parent = None
            self.children = []

        def __repr__(self):
            return 'Node({!r:})'.format(self.value)

        # property that manages the parent as a weak-reference
        @property
        def parent(self):
            return self._parent if self._parent is None else self._parent()

        @parent.setter
        def parent(self, node):
            self._parent = weakref.ref(node)

        def add_child(self, child):
            self.children.append(child)
            child.parent = self


    if __name__ == '__main__':
        root = Node('parent')
        c1 = Node('c1')
        c2 = Node('c2')
        root.add_child(c1)
        root.add_child(c2)

        print(c1.parent)
        del root
        print(c1.parent)


# simplified_initialization_of_data_structures
if __name__ == '__main__':
    class Structure:
        # Class variable that specifies expected fields
        _fields = []

        def __init__(self, *args):
            if len(args) != len(self._fields):
                raise TypeError('Expected {} arguments'.format(len(self._fields)))

            # Set the arguments
            for name, value in zip(self._fields, args):
                setattr(self, name, value)


    # Example class definitions
    if __name__ == '__main__':
        class Stock(Structure):
            _fields = ['name', 'shares', 'price']


        class Point(Structure):
            _fields = ['x', 'y']


        class Circle(Structure):
            _fields = ['radius']

            def area(self):
                return math.pi * self.radius ** 2

    if __name__ == '__main__':
        s = Stock('ACME', 50, 91.1)
        print(s.name, s.shares, s.price)

        p = Point(2, 3)
        print(p.x, p.y)

        c = Circle(4.5)
        print(c.radius)

        try:
            s2 = Stock('ACME', 50)
        except TypeError as e:
            print(e)

if __name__ == '__main__':
    class Structure:
        _fields = []

        def __init__(self, *args, **kwargs):
            if len(args) > len(self._fields):
                raise TypeError('Expected {} arguments'.format(len(self._fields)))

            # Set all of the positional arguments
            for name, value in zip(self._fields, args):
                setattr(self, name, value)

            # Set the remaining keyword arguments
            for name in self._fields[len(args):]:
                setattr(self, name, kwargs.pop(name))

            # Check for any remaining unknown arguments
            if kwargs:
                raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))


    # Example use
    if __name__ == '__main__':
        class Stock(Structure):
            _fields = ['name', 'shares', 'price']


        s1 = Stock('ACME', 50, 91.1)
        s2 = Stock('ACME', 50, price=91.1)
        s3 = Stock('ACME', shares=50, price=91.1)

if __name__ == '__main__':
    class Structure:
        # Class variable that specifies expected fields
        _fields = []

        def __init__(self, *args, **kwargs):
            if len(args) != len(self._fields):
                raise TypeError('Expected {} arguments'.format(len(self._fields)))

            # Set the arguments
            for name, value in zip(self._fields, args):
                setattr(self, name, value)

            # Set the additional arguments (if any)
            extra_args = kwargs.keys() - self._fields
            for name in extra_args:
                setattr(self, name, kwargs.pop(name))
            if kwargs:
                raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))


    # Example use
    if __name__ == '__main__':
        class Stock(Structure):
            _fields = ['name', 'shares', 'price']


        s1 = Stock('ACME', 50, 91.1)
        s2 = Stock('ACME', 50, 91.1, date='8/2/2012')

