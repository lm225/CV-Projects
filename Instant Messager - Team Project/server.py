#!/usr/bin/env python

"""
    Server class that allows multiple clients to connect,
    each being allocated a thread where they can
    send and receive messages based on input recived over
    a socket connection to the client
"""

import socket
import threading
import pickle
import os
import gzip
import struct

def receive_message(message):
    """
    this method will be called when the client either
    sends a message or requests a message (similar format)
    Adds message to addressees inbox and then checks own inbox
    Returns any messages in there in list form
        Additionally witll create log files
    """
   
    get_log = message['get_log']

    # if a log file is requested, send that
    if get_log:
        return send_file(message)

    # get user id and address
    user_id = message['identity']
    addressees = message['address']

    # if message has an address, add message to correct users dict value
    if (len(message['address']) > 0):

        # for each addressee, if addressee already has messages on server add
        # them to his 'inbox', else create inbox then add
        for address in addressees:

            # add message to addressees dict key
            if address in message_dictionary:
                message_dictionary[address].append(message)
            else:
                message_dictionary[address] = []
                message_dictionary[address].append(message)

            # also add message to addressees log file
            # check if file exists, if not, create it
            log_file_name = str(address) + 'log.txt.gz'

            if (not (os.path.isfile(log_file_name))):
                log_file = gzip.open(log_file_name, 'w')
                log_file.close()
            try:
                # open in append mode
                log_file = gzip.open(log_file_name, 'a')
                log_file.write(str(message))
                log_file.write('\n')
                log_file.close()
            except IOError as e:
                print "Unable to open file..."

    # if message has no address, don't add message
    # after message has been added (or not), check if server is holding any
    # messages for the client
    returning_list = []
    if user_id in message_dictionary:
        for m in message_dictionary[user_id]:
            returning_list.append(m)
        # remove userid from dictionary when sending
        message_dictionary.pop(user_id)
    return returning_list


def run(sock):
    """
        Each connection creates a thread running this function.
        The function listens for messages from the connected client
        when message is recived, the receive_message function is 
        called on it, the output of the reciveds function is then
        passed back to the user over the socket connection
        """
    while True:
        # listens for the clients messages
        rec_msg = sock.recv(1024)
        msg_dict = pickle.loads(rec_msg)

        # server on-screen activity display
        print "\n message received from the client: ", msg_dict
        print "\n message_dictionary before receive message function: "
        print message_dictionary

        # digests the client's message and determines the response
        output = receive_message(msg_dict)

        # server on-screen activity display
        print "\n message_dictionary after receive message function: "
        print message_dictionary

        # sends the response to the client
        response = pickle.dumps(output)
        sock.sendall(response)


def send_file(message):
    """
        this function is used to read a log file and convert it to
        a data stream suitable for sending across a socket connection
        """
    try:
        user_name = message['identity']
        log_file_name = user_name + 'log.txt.gz'
        with gzip.open(log_file_name, 'rb') as file:
            data = file.read()
        return data
    except IOError:
        return []


def receive(listens):
    """
        This function is repeatedly called by the continuous_recive function
        it listens for connections and assigns new threads to each recived
        """
    try:
        conn, address = listens.accept()
        print 'Connection received from ', address
        conn.settimeout(100)

        # allocate new thread to client, passes the socket communicating with
        # the client
        t = threading.Thread(target = run, args = (conn,))
        t.setDaemon(True)
        t.start()

    except Exception, e:
        print 'Connection closed... %s' % (e)


def continuous_receive():
    """
    this function creates a socket listening for connections and then
    repeatedly calls the receive function taking that socket as a parameter
    """

    server = '0.0.0.0'
    port = 54321

    #  server socket is opened and initialised
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)
    s.bind((server,port))
    s.listen(5) # number is queue size, max 5

    #  listen for connection
    while True:
        receive(s)

def receive_multicast():
    """
    listens for clients multicasting, answers with the address of the machine
    the server is run on, to identify itself as a running server
    """
    group = '224.1.1.1'
    port = 5007

    # set up socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    m = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, m)

    # listen and respond to client connections
    # send server ip back to incoming client
    while True:
        ip, addr = sock.recvfrom(1024)
        print 'Heartbeat ping recived from - ', addr
        ourip = socket.gethostbyname(socket.gethostname())
        sock.sendto(ourip, addr)


# calls main function
if __name__ == '__main__':
    message_dictionary = {} # contains messgages for all clients
    # starts the multicasting to identify itself as a running server to potential
    # clients
    t = threading.Thread(target = receive_multicast, args = ())
    t.setDaemon(True)
    t.start()
    continuous_receive()
