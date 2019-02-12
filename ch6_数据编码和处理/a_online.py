







# parsing_xml_documents_with_namespaces
if __name__ == '__main__':
    # example.py
    #
    # Example of XML namespace handling

    from xml.etree.ElementTree import parse


    class XMLNamespaces:
        def __init__(self, **kwargs):
            self.namespaces = {}
            for name, uri in kwargs.items():
                self.register(name, uri)

        def register(self, name, uri):
            self.namespaces[name] = '{' + uri + '}'

        def __call__(self, path):
            return path.format_map(self.namespaces)


    doc = parse('sample.xml')
    ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')

    e = doc.find(ns('content/{html}html'))
    print(e)

    text = doc.findtext(ns('content/{html}html/{html}head/{html}title'))
    print(text)


# reading_and_writing_binary_arrays_of_structures
if __name__ == '__main__':
    from struct import Struct


    def read_records(format, f):
        record_struct = Struct(format)
        chunks = iter(lambda: f.read(record_struct.size), b'')
        return (record_struct.unpack(chunk) for chunk in chunks)


    # Example
    if __name__ == '__main__':
        with open('data.b', 'rb') as f:
            for rec in read_records('<idd', f):
                # Process rec
                print(rec)

if __name__ == '__main__':
    from struct import Struct


    def unpack_records(format, data):
        record_struct = Struct(format)
        return (record_struct.unpack_from(data, offset)
                for offset in range(0, len(data), record_struct.size))


    # Example
    if __name__ == '__main__':
        with open('data.b', 'rb') as f:
            data = f.read()
            for rec in unpack_records('<idd', data):
                # Process record
                print(rec)

if __name__ == '__main__':
    from struct import Struct


    def write_records(records, format, f):
        '''
        Write a sequence of tuples to a binary file of structures.
        '''
        record_struct = Struct(format)
        for r in records:
            f.write(record_struct.pack(*r))


    # Example
    if __name__ == '__main__':
        records = [(1, 2.3, 4.5),
                   (6, 7.8, 9.0),
                   (12, 13.4, 56.7)]

        with open('data.b', 'wb') as f:
            write_records(records, '<idd', f)





# reading_nested_and_variable_sized_binary_structures
if __name__ == '__main__':
    import struct


    class StructField:
        def __init__(self, format, offset):
            self.format = format
            self.offset = offset

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                r = struct.unpack_from(self.format,
                                       instance._buffer, self.offset)
                return r[0] if len(r) == 1 else r


    class Structure:
        def __init__(self, bytedata):
            self._buffer = memoryview(bytedata)


    if __name__ == '__main__':
        class PolyHeader(Structure):
            file_code = StructField('<i', 0)
            min_x = StructField('<d', 4)
            min_y = StructField('<d', 12)
            max_x = StructField('<d', 20)
            max_y = StructField('<d', 28)
            num_polys = StructField('<i', 36)


        f = open('polys.bin', 'rb')
        data = f.read()

        phead = PolyHeader(data)
        print(phead.file_code == 0x1234)
        print('min_x=', phead.min_x)
        print('max_x=', phead.max_x)
        print('min_y=', phead.min_y)
        print('max_y=', phead.max_y)
        print('num_polys=', phead.num_polys)

if __name__ == '__main__':
    # Example 2: Introduction of a metaclass

    import struct


    class StructField:
        def __init__(self, format, offset):
            self.format = format
            self.offset = offset

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                r = struct.unpack_from(self.format,
                                       instance._buffer, self.offset)
                return r[0] if len(r) == 1 else r


    class StructureMeta(type):
        '''
        Metaclass that automatically creates StructField descriptors
        '''

        def __init__(self, clsname, bases, clsdict):
            fields = getattr(self, '_fields_', [])
            byte_order = ''
            offset = 0
            for format, fieldname in fields:
                if format.startswith(('<', '>', '!', '@')):
                    byte_order = format[0]
                    format = format[1:]
                format = byte_order + format
                setattr(self, fieldname, StructField(format, offset))
                offset += struct.calcsize(format)
            setattr(self, 'struct_size', offset)


    class Structure(metaclass=StructureMeta):
        def __init__(self, bytedata):
            self._buffer = memoryview(bytedata)

        @classmethod
        def from_file(cls, f):
            return cls(f.read(cls.struct_size))


    if __name__ == '__main__':
        class PolyHeader(Structure):
            _fields_ = [
                ('<i', 'file_code'),
                ('d', 'min_x'),
                ('d', 'min_y'),
                ('d', 'max_x'),
                ('d', 'max_y'),
                ('i', 'num_polys')
            ]


        f = open('polys.bin', 'rb')
        phead = PolyHeader.from_file(f)
        print(phead.file_code == 0x1234)
        print('min_x=', phead.min_x)
        print('max_x=', phead.max_x)
        print('min_y=', phead.min_y)
        print('max_y=', phead.max_y)
        print('num_polys=', phead.num_polys)

if __name__ == '__main__':
    # Example 3: Nested structure support

    import struct


    class StructField:
        '''
        Descriptor representing a simple structure field
        '''

        def __init__(self, format, offset):
            self.format = format
            self.offset = offset

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                r = struct.unpack_from(self.format,
                                       instance._buffer, self.offset)
                return r[0] if len(r) == 1 else r


    class NestedStruct:
        '''
        Descriptor representing a nested structure
        '''

        def __init__(self, name, struct_type, offset):
            self.name = name
            self.struct_type = struct_type
            self.offset = offset

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                data = instance._buffer[self.offset:
                                        self.offset + self.struct_type.struct_size]
                result = self.struct_type(data)
                setattr(instance, self.name, result)
                return result


    class StructureMeta(type):
        '''
        Metaclass that automatically creates StructField descriptors
        '''

        def __init__(self, clsname, bases, clsdict):
            fields = getattr(self, '_fields_', [])
            byte_order = ''
            offset = 0
            for format, fieldname in fields:
                if isinstance(format, StructureMeta):
                    setattr(self, fieldname, NestedStruct(fieldname, format, offset))
                    offset += format.struct_size
                else:
                    if format.startswith(('<', '>', '!', '@')):
                        byte_order = format[0]
                        format = format[1:]
                    format = byte_order + format
                    setattr(self, fieldname, StructField(format, offset))
                    offset += struct.calcsize(format)
            setattr(self, 'struct_size', offset)


    class Structure(metaclass=StructureMeta):
        def __init__(self, bytedata):
            self._buffer = memoryview(bytedata)

        @classmethod
        def from_file(cls, f):
            return cls(f.read(cls.struct_size))


    if __name__ == '__main__':
        class Point(Structure):
            _fields_ = [
                ('<d', 'x'),
                ('d', 'y')
            ]


        class PolyHeader(Structure):
            _fields_ = [
                ('<i', 'file_code'),
                (Point, 'min'),
                (Point, 'max'),
                ('i', 'num_polys')
            ]


        f = open('polys.bin', 'rb')
        phead = PolyHeader.from_file(f)
        print(phead.file_code == 0x1234)
        print('min.x=', phead.min.x)
        print('max.x=', phead.max.x)
        print('min.y=', phead.min.y)
        print('max.y=', phead.max.y)
        print('num_polys=', phead.num_polys)

if __name__ == '__main__':
    # Example 4: Variable sized chunks

    import struct


    class StructField:
        '''
        Descriptor representing a simple structure field
        '''

        def __init__(self, format, offset):
            self.format = format
            self.offset = offset

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                r = struct.unpack_from(self.format,
                                       instance._buffer, self.offset)
                return r[0] if len(r) == 1 else r


    class NestedStruct:
        '''
        Descriptor representing a nested structure
        '''

        def __init__(self, name, struct_type, offset):
            self.name = name
            self.struct_type = struct_type
            self.offset = offset

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                data = instance._buffer[self.offset:
                                        self.offset + self.struct_type.struct_size]
                result = self.struct_type(data)
                setattr(instance, self.name, result)
                return result


    class StructureMeta(type):
        '''
        Metaclass that automatically creates StructField descriptors
        '''

        def __init__(self, clsname, bases, clsdict):
            fields = getattr(self, '_fields_', [])
            byte_order = ''
            offset = 0
            for format, fieldname in fields:
                if isinstance(format, StructureMeta):
                    setattr(self, fieldname, NestedStruct(fieldname, format, offset))
                    offset += format.struct_size
                else:
                    if format.startswith(('<', '>', '!', '@')):
                        byte_order = format[0]
                        format = format[1:]
                    format = byte_order + format
                    setattr(self, fieldname, StructField(format, offset))
                    offset += struct.calcsize(format)
            setattr(self, 'struct_size', offset)


    class Structure(metaclass=StructureMeta):
        def __init__(self, bytedata):
            self._buffer = memoryview(bytedata)

        @classmethod
        def from_file(cls, f):
            return cls(f.read(cls.struct_size))


    class SizedRecord:
        def __init__(self, bytedata):
            self._buffer = memoryview(bytedata)

        @classmethod
        def from_file(cls, f, size_fmt, includes_size=True):
            sz_nbytes = struct.calcsize(size_fmt)
            sz_bytes = f.read(sz_nbytes)
            sz, = struct.unpack(size_fmt, sz_bytes)
            buf = f.read(sz - includes_size * sz_nbytes)
            return cls(buf)

        def iter_as(self, code):
            if isinstance(code, str):
                s = struct.Struct(code)
                for off in range(0, len(self._buffer), s.size):
                    yield s.unpack_from(self._buffer, off)
            elif isinstance(code, StructureMeta):
                size = code.struct_size
                for off in range(0, len(self._buffer), size):
                    data = self._buffer[off:off + size]
                    yield code(data)


    if __name__ == '__main__':
        class Point(Structure):
            _fields_ = [
                ('<d', 'x'),
                ('d', 'y')
            ]


        class PolyHeader(Structure):
            _fields_ = [
                ('<i', 'file_code'),
                (Point, 'min'),
                (Point, 'max'),
                ('i', 'num_polys')
            ]


        def read_polys(filename):
            polys = []
            with open(filename, 'rb') as f:
                phead = PolyHeader.from_file(f)
                for n in range(phead.num_polys):
                    rec = SizedRecord.from_file(f, '<i')
                    poly = [(p.x, p.y)
                            for p in rec.iter_as(Point)]
                    polys.append(poly)
            return polys


        polys = read_polys('polys.bin')
        print(polys)

if __name__ == '__main__':
    import struct
    import itertools

    polys = [
        [(1.0, 2.5), (3.5, 4.0), (2.5, 1.5)],
        [(7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0)],
        [(3.4, 6.3), (1.2, 0.5), (4.6, 9.2)],
    ]


    def write_polys(filename, polys):
        # Determine bounding box
        flattened = list(itertools.chain(*polys))
        min_x = min(x for x, y in flattened)
        max_x = max(x for x, y in flattened)
        min_y = min(y for x, y in flattened)
        max_y = max(y for x, y in flattened)

        with open(filename, 'wb') as f:
            f.write(struct.pack('<iddddi',
                                0x1234,
                                min_x, min_y,
                                max_x, max_y,
                                len(polys)))

            for poly in polys:
                size = len(poly) * struct.calcsize('<dd')
                f.write(struct.pack('<i', size + 4))
                for pt in poly:
                    f.write(struct.pack('<dd', *pt))


    # Call it with our polygon data
    write_polys('polys.bin', polys)

