
# adding_or_changing_the_encoding_of_an_already_open_file
if __name__ == '__main__':
    # Example of adding a text encoding to existing file-like object

    import urllib.request
    import io

    u = urllib.request.urlopen('http://www.python.org')
    f = io.TextIOWrapper(u, encoding='utf-8')
    text = f.read()

    print(text)



# iterating_over_fixed-sized_records
if __name__ == '__main__':
    # Example of iterating of fixed-size records
    #
    # The file 'data.bin' contains 32-byte fixed size records
    # that consist of a 4-digit number followed by a 28-byte string.

    from functools import partial

    RECORD_SIZE = 32

    with open('data.bin', 'rb') as f:
        records = iter(partial(f.read, RECORD_SIZE), b'')
        for r in records:
            print(r)




# wrapping_an_existing_file_descriptor_as_a_file_object
if __name__ == '__main__':
    from socket import socket, AF_INET, SOCK_STREAM


    def echo_client(client_sock, addr):
        print("Got connection from", addr)

        # Make text-mode file wrappers for socket reading/writing
        client_in = open(client_sock.fileno(), 'rt', encoding='latin-1', closefd=False)
        client_out = open(client_sock.fileno(), 'wt', encoding='latin-1', closefd=False)

        # Echo lines back to the client using file I/O
        for line in client_in:
            client_out.write(line)
            client_out.flush()
        client_sock.close()


    def echo_server(address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(address)
        sock.listen(1)
        while True:
            client, addr = sock.accept()
            echo_client(client, addr)


    if __name__ == '__main__':
        print('Echo serving running on localhost:25000')
        echo_server(('', 25000))

# writing_bytes_to_a_text_file
if __name__ == '__main__':
    # Example of writing raw bytes on a file opened in text mode

    import sys

    # A byte string
    data = b'Hello World\n'

    # Write onto the buffer attribute (bypassing text encoding)
    sys.stdout.buffer.write(data)
