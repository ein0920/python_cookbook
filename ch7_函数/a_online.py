
# accessing_variables_defined_inside_a_closure
if __name__ == '__main__':
    # Example of accessing variables inside a closure

    def sample():
        n = 0

        # Closure function
        def func():
            print('n=', n)

        # Accessor methods for n
        def get_n():
            return n

        def set_n(value):
            nonlocal n
            n = value

        # Attach as function attributes
        func.get_n = get_n
        func.set_n = set_n
        return func


    if __name__ == '__main__':
        f = sample()
        f()
        n = 0
        f.set_n(10)
        f()
        print(f.get_n())

if __name__ == '__main__':
    # Example of faking classes with a closure

    import sys


    class ClosureInstance:
        def __init__(self, locals=None):
            if locals is None:
                locals = sys._getframe(1).f_locals

            # Update instance dictionary with callables
            self.__dict__.update((key, value) for key, value in locals.items()
                                 if callable(value))

        # Redirect special methods
        def __len__(self):
            return self.__dict__['__len__']()


    # Example use
    def Stack():
        items = []

        def push(item):
            items.append(item)

        def pop():
            return items.pop()

        def __len__():
            return len(items)

        return ClosureInstance()


    if __name__ == '__main__':
        s = Stack()
        print(s)
        s.push(10)
        s.push(20)
        s.push('Hello')
        print(len(s))
        print(s.pop())
        print(s.pop())
        print(s.pop())


if __name__ == '__main__':
    # Example of a normal class

    # Example use
    class Stack2:
        def __init__(self):
            self.items = []

        def push(self, item):
            self.items.append(item)

        def pop(self):
            return self.items.pop()

        def __len__(self):
            return len(self.items)


    if __name__ == '__main__':
        import example2
        from timeit import timeit

        print('Using a class')
        s = Stack2()
        print(timeit('s.push(1); s.pop()', 'from __main__ import s'))

        print('Using a closure')
        s = example2.Stack()
        print(timeit('s.push(1); s.pop()', 'from __main__ import s'))

# carrying_extra_state_with_callback_functions
if __name__ == '__main__':
    # This example is about the problem of carrying extra state around
    # through callback functions.   To test the examples, this very
    # simple code emulates the typical control of a callback.

    def apply_async(func, args, *, callback):
        # Compute the result
        result = func(*args)

        # Invoke the callback with the result
        callback(result)


    # A simple function for testing
    def add(x, y):
        return x + y


    # (a) A simple callback example

    print('# --- Simple Example')


    def print_result(result):
        print("Got:", result)


    apply_async(add, (2, 3), callback=print_result)
    apply_async(add, ('hello', 'world'), callback=print_result)

    # (b) Using a bound method

    print('# --- Using a bound-method')


    class ResultHandler:
        def __init__(self):
            self.sequence = 0

        def handler(self, result):
            self.sequence += 1
            print('[{}] Got: {}'.format(self.sequence, result))


    r = ResultHandler()
    apply_async(add, (2, 3), callback=r.handler)
    apply_async(add, ('hello', 'world'), callback=r.handler)

    # (c) Using a closure

    print('# --- Using a closure')


    def make_handler():
        sequence = 0

        def handler(result):
            nonlocal sequence
            sequence += 1
            print('[{}] Got: {}'.format(sequence, result))

        return handler


    handler = make_handler()
    apply_async(add, (2, 3), callback=handler)
    apply_async(add, ('hello', 'world'), callback=handler)

    # (d) Using a coroutine

    print('# --- Using a coroutine')


    def make_handler():
        sequence = 0
        while True:
            result = yield
            sequence += 1
            print('[{}] Got: {}'.format(sequence, result))


    handler = make_handler()
    next(handler)  # Advance to the yield

    apply_async(add, (2, 3), callback=handler.send)
    apply_async(add, ('hello', 'world'), callback=handler.send)

    # (e) Partial function application

    print('# --- Using partial')


    class SequenceNo:
        def __init__(self):
            self.sequence = 0


    def handler(result, seq):
        seq.sequence += 1
        print('[{}] Got: {}'.format(seq.sequence, result))


    seq = SequenceNo()
    from functools import partial

    apply_async(add, (2, 3), callback=partial(handler, seq=seq))
    apply_async(add, ('hello', 'world'), callback=partial(handler, seq=seq))

#functions_with_default_arguments
if __name__ == '__main__':
    # Examples of a function with default arguments

    # (a) Dangers of using a mutable default argument

    def spam(b=[]):
        return b


    a = spam()
    print(a)
    a.append(1)
    a.append(2)
    b = spam()
    print(b)  # Carefully observe result
    print('-' * 10)


    # (b) Better alternative for mutable defaults
    def spam(b=None):
        if b is None:
            b = []
        return b


    a = spam()
    print(a)
    a.append(1)
    a.append(2)
    b = spam()
    print(b)
    print('-' * 10)

    # (c) Example of testing if an argument was supplied or not

    _no_value = object()


    def spam(b=_no_value):
        if b is _no_value:
            print("No b value supplied")
        else:
            print("b=", b)


    spam()
    spam(None)
    spam(0)
    spam([])

# inlining_callback_functions
if __name__ == '__main__':
    # Example of implementing an inlined-callback function

    # Sample function to illustrate callback control flow

    def apply_async(func, args, *, callback):
        # Compute the result
        result = func(*args)

        # Invoke the callback with the result
        callback(result)


    # Inlined callback implementation
    from queue import Queue
    from functools import wraps


    class Async:
        def __init__(self, func, args):
            self.func = func
            self.args = args


    def inlined_async(func):
        @wraps(func)
        def wrapper(*args):
            f = func(*args)
            result_queue = Queue()
            result_queue.put(None)
            while True:
                result = result_queue.get()
                try:
                    a = f.send(result)
                    apply_async(a.func, a.args, callback=result_queue.put)
                except StopIteration:
                    break

        return wrapper


    # Sample use
    def add(x, y):
        return x + y


    @inlined_async
    def test():
        r = yield Async(add, (2, 3))
        print(r)
        r = yield Async(add, ('hello', 'world'))
        print(r)
        for n in range(10):
            r = yield Async(add, (n, n))
            print(r)
        print('Goodbye')


    if __name__ == '__main__':
        # Simple test
        print('# --- Simple test')
        test()

        print('# --- Multiprocessing test')
        import multiprocessing

        pool = multiprocessing.Pool()
        apply_async = pool.apply_async
        test()

# making_an_n-argument_callable_work_as_a_callable_with_fewer_arguments
if __name__ == '__main__':
    # Example of using partial() with sorting a list of (x,y) coordinates

    import functools

    points = [(1, 2), (3, 4), (5, 6), (7, 7)]

    import math


    def distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.hypot(x2 - x1, y2 - y1)


    pt = (4, 3)
    points.sort(key=functools.partial(distance, pt))
    print(points)

if __name__ == '__main__':
    # Using partial to supply extra arguments to a callback function

    import functools


    def output_result(result, log=None):
        if log is not None:
            log.debug('Got: %r', result)


    # A sample function
    def add(x, y):
        return x + y


    if __name__ == '__main__':
        import logging
        from multiprocessing import Pool
        from functools import partial

        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger('test')

        p = Pool()
        p.apply_async(add, (3, 4), callback=functools.partial(output_result, log=log))
        p.close()
        p.join()

if __name__ == '__main__':
    # Using partial to supply extra arguments to a class constructor
    from socketserver import StreamRequestHandler, TCPServer


    class EchoHandler(StreamRequestHandler):
        # ack is added keyword-only argument. *args, **kwargs are
        # any normal parameters supplied (which are passed on)
        def __init__(self, *args, ack, **kwargs):
            self.ack = ack
            super().__init__(*args, **kwargs)

        def handle(self):
            for line in self.rfile:
                self.wfile.write(self.ack + line)


    if __name__ == '__main__':
        from functools import partial

        serv = TCPServer(('', 15000), partial(EchoHandler, ack=b'RECEIVED:'))
        print('Echo server running on port 15000')
        serv.serve_forever()
