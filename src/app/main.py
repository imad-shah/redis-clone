import threading
import time
from typing import Any
import socket # noqa: F401

class Value:

    def __init__ (self, val, exp=None, curr=None):
        self.val = val
        self.exp = exp
        self.curr = curr
        
def current_milli_time():
    return round(time.time() * 1000)

def parse_resp(data):
    """Parse RESP format data."""
    data = data.decode()
    if not data:
        return None, None
    # Handle array format (*2\r\n$4\r\nECHO\r\n$6\r\norange\r\n)
    if data[0] == '*':
        # Split into lines
        parts = data.split('\r\n')
        # First line contains number of arguments (*2)
        num_args = int(parts[0][1:])
        
        args = []
        i = 1
        for _ in range(num_args):
            # Skip the length indicator ($4)
            str_len = int(parts[i][1:])
            # Get the actual string value
            args.append(parts[i + 1])
            i += 2
            
        return args[0], ' '.join(args[1:]) if len(args) > 1 else ''
    
    return None, None

def pong(data, conn, cache):
    conn.send(b"+PONG\r\n")

def echo(data, conn, cache):
    # Format response in RESP format for bulk strings
    response = f"${len(data)}\r\n{data}\r\n"
    conn.send(response.encode())

def set_key(data,conn,cache):
    parts = data.split()
    #['pear','blueberry']
    if 'px' in parts:
        cache[parts[0]] = Value(parts[1], int(parts[3]), current_milli_time())
    else:
        cache[parts[0]] = Value(parts[1])
    conn.send(b'+OK\r\n')

def get_val(data,conn, cache):
    parts = data.split()
    val = cache.get(parts[0], None)

    if not val:
        conn.send(b'$-1\r\n')
    elif val.exp and current_milli_time() - val.exp >= val.curr:
        del cache[parts[0]]
        conn.send(b'$-1\r\n')
    else:
        response = f"${len(val.val)}\r\n{val.val}\r\n"
        conn.send(response.encode())

def handle_client(conn, addr, cache):
    print(f'Connected to {addr}')

    commands = {
        "ECHO": echo,
        "PING": pong,
        "SET" : set_key,
        "GET" : get_val,
    }

    while True:
        try:
            data = conn.recv(1024)  # Read data as bytes
            if not data:  # If no data is received,  exit the loop
                break
            
            command, args = parse_resp(data)
            if command:
                command_handler = commands.get(command.upper())
                if command_handler:
                    command_handler(args, conn, cache)
        except Exception as e:
            print(f"Error handling client: {e}")
            break

    print(f"Connection to {addr} closed")
    conn.close()

def main():
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.listen()
    cache = {}

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr, cache))
        client_thread.start()

if __name__ == "__main__":
    main()