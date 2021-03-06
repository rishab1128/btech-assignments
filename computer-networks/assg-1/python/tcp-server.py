# File: tcp-server.py

# Author: Anindya Kundu <anindya.k22@outlook.com>
# Date: 2020-06-02

# Reference: https://docs.python.org/3/library/

"""
A Simple TCP server program.

This server can chat with one client at a time. The client initiates
a conversation, to which this server replies. The server and client
get alternate changes to send a message. The conversation ends when
one of them sends a "bye".

Functions:

- `_chat()`: conducts the chat with the client
- `_recv_msg()`: receives data in small chunks and assembles message
- `_send_msg()`: sends message with the length as header

How To Use This Module
======================
1. run this script using [python3 tcp-server.py]
2. run client script using [python3 tcp-client.py]
"""


import socket
import sys
from os import system


def _recv_msg(connection):
    """
    Assembles message by receiving data in small chunks.

    Parameters `connection`: client socket object

    Return message assembled by concatenating all received data chunks
    """

    SIZE = 16       # size of data chunk in bytes
    message = ""    # message received

    sendlen = int(connection.recv(8).decode())      # message length
    recvlen = 0

    while not recvlen == sendlen:
        # receive data in small chunks and concatenate
        data = connection.recv(SIZE).decode()
        recvlen += len(data)
        message += data

    return message


def _send_msg(connection, message):
    """
    Sends message length and message.

    Parameters:

    - `connection`: client socket object
    - `message`: message string to send

    Return void
    """

    # pad message length string with 0s to get 8 bytes
    msglen = str(len(message))
    zeros = 8 - min(len(msglen), 8)
    for _ in range(zeros):
        msglen = "0" + msglen

    connection.sendall(msglen.encode())     # send message length
    connection.sendall(message.encode())    # send message


def _chat(connection):
    """
    Waits for the client to initiate the conversation. Prints the
    client's message and takes a message to send to the client.
    This process continues until one of then says "bye".

    Parameters:

    - `connection`: client socket object
    """

    # infinite loop with one turn to each of client and server per iteration
    while True:
        response = _recv_msg(connection)
        print('CLIENT: %s' % response, file=sys.stderr)
        if response == 'bye':
            break

        message = input('SERVER: ')
        _send_msg(connection, message)
        if message == 'bye':
            break


if __name__ == "__main__":
    """
    Attribute is __main__ when module is run as main program.
    """

    # clear console
    system('clear')

    # create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind socket to the address and port
    server_address = ('localhost', 4200)
    print('starting up on %s port %s' % server_address, file=sys.stderr)
    sock.bind(server_address)

    # listen for incoming connections
    sock.listen(1)

    # wait for a connection
    print('waiting for a connection', file=sys.stderr)
    connection, client_address = sock.accept()
    print('connection from %s port %s\n' % client_address, file=sys.stderr)

    try:
        # call chat function to conduct chat
        _chat(connection)

    finally:
        # clean up connection
        print('\nclosing socket', file=sys.stderr)
        sock.close()
        connection.close()
