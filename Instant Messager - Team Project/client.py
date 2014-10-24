#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
from curses import ascii
import sys
import socket
import threading
import pickle
import time
import datetime
import gzip
import struct
import os

# global variable representing lines scrolled up by pad
padpos = -18


identity = ''
# global list variable to store messages to be sent
messages = []
# global variable to indicate when there are messages to be sent
messages_in_queue = False
# dictionary with no content or addressees to be sent to request messages every
# second
listen_dict = {'identity' : identity, 'timestamp': datetime.datetime.now(),
    'address' : (), 'content' : '', 'get_log' : False}

def send_multicast(pad):
    """ 
    method sending it's address to all servers and waiting for answers, so that
    a list of all runnning servers can be established.
    """
    
    group = '224.1.1.1' #multi-cast address on which the server(s) listen
    port = 5007

    # setting up the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(socket.gethostbyname(socket.gethostname()), (group, port))

    # listens for all responses within 1 seconds
    sock.settimeout(1)
    try:
        # continuously prints server responses until stopped by the timeout
        while True:
            add_and_update_pad(pad, str(sock.recv(1024)))
    except socket.timeout:
        return

def client_loop(sock, pad):
    """
    The client loop does the main communication to the server.
    It checks whether there are outgoing messages that need to be sent to the
    server. If not, it sends an empty dictionary to check if the server has 
    messages addressed to the client.
    """
    while True:
        
        global messages # list of outgoing messages
        global messages_in_queue # boolean specifying if messages need to be sent
        global listen_dict # empty dictionary for requesting messages from server

        time.sleep(0.1) # the server is checked every

        if messages_in_queue:
            # sends any outgoing messages
            for m in messages:
                mymess = [m]
                message_to_send = pickle.dumps(dict(m))
                receive_message(pad, mymess)
                sock.sendall(message_to_send)
            # no outgoing messages to be sent are left
            messages_in_queue = False
            messages = []

        else:
            # send an empty dictionary to request messages from the server
            sock.sendall(pickle.dumps(listen_dict))
            resp = pickle.loads(sock.recv(1024))
            # if the server returned a message, it is passed to the UI
            if resp != []:
                receive_message(pad, resp)
            

def connect(ip, pad):
    """
    Opens a socket and connets to the specified server. Once the conneciton is
    established, the loop checking for ingoing and outgoing messages is called.
    """
    server = ip
    port = 54321
    
    try:
        s = socket.socket() # creating a socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.settimeout(1000) # long timeout
        add_and_update_pad(pad, "Attempting to connect to server at " + ip)
                
        # connecting to the server
        try:
            s.connect((server, port))
            connected = True
            add_and_update_pad(pad, "Connected to server!")
        except socket.error as e:
            add_and_update_pad(pad, "Invalid IP, press esc to exit...")

            
        # calling the loop in charge of sending and receiving
        client_loop(s, pad)

        #closing the connection when messages aren't sent anymore
        s.close()
    
    except Exception as e:
        add_and_update_pad(pad, "something went wrong: " + str(e))


def formatInfo(screen, pad, win, content, time, addresseesString):

    """ method to split the addresseesString into individual addressee(s) and 
        fill a message dictionary with all of the message details, correctly 
        formatted according to the message protocol
    """
    
    global identity
    global messages_in_queue
    global messages

    # split the addressee(s) entered by the user to store them individually in
    # the dictionary
    addresseesList = addresseesString.split(",")
    for s in addresseesList:
        s = s.strip()
    # create a dictionary which includes the individual addressee(s)
    data = {'identity': identity, 'address': addresseesList,
        'content': content, 'timestamp': time, 'get_log': False}
    # add the new dictionary to the list of messages to be sent
    messages.append(data)
    messages_in_queue = True


def get_user_input(screen, pad, win, addresseesString):

    """
        method to get the message content from the user
    """
    global messageRequest
    # get the messgae content from the user
    content = get_text_via_curse(screen, pad, win, "Please type a message to " +addresseesString + ": ")

    while True:
        # check if the message content is equal to "exit"
        if content == "exit":
            # call the getInfo function, to allow the user to select new addressee(s)
            getInfo(screen, pad, win)
        else:
            time = datetime.datetime.now()
            # call the formatInfo function, to correctly format and create a message dictionary
            formatInfo(screen, pad, win, content, time, addresseesString)
            # get the messgae content from the user
            content = get_text_via_curse(screen, pad, win, "->")

def getInfo(screen, pad, win):
    """
        method to get the addressee(s) from the user and call the get_user_input 
        function, passing it addresseesString which contains the addressee(s)
    """
    # get the addressee(s) from the user
    addresseesString = get_text_via_curse(screen,pad,win,"Who would you like to message? ")
    get_user_input(screen, pad, win, addresseesString)

def receive_message(pad, list):
    """
        method to sort a list of dictionaries from the server and output the 
        messages in a readable format
    """
    try:
        # sorts the list of dictionaries using the value of 'timestamp'

        list.sort(key=lambda d: d['timestamp'])
        for message in list:
            messageidentity = message['identity']
            timestamp = message['timestamp']
            content = message['content']
            timestring = str(timestamp)[11:-7]
            # outputs message details to user in a readable format
            add_and_update_pad(pad, timestring + " - " + messageidentity + " - " + content)

    # if log file is requested, print it to pad
    except AttributeError:
        global identity
        add_and_update_pad(pad, "Log file created at " + identity + "log.txt.gz")
        log_file_name = identity + 'log.txt.gz'
        if (not (os.path.isfile(log_file_name))):
            log_file = gzip.open(log_file_name, 'w')
            log_file.close()
        try:
            # open in append mode
            log_file = gzip.open(log_file_name, 'a')
            log_file.write(list)
            log_file.close()
        except IOError as e:
            add_and_update_pad(pad, "Unable to open file…")

def start_communication(screen, pad, win):
    """
        method to get ther users identity and call the getInfo function
    """

    global identity
    global listen_dict
    global messages
    global messages_in_queue

    identity = get_text_via_curse(screen, pad, win, "Please enter your user name: ")
    listen_dict['identity'] = identity
    get_log = get_text_via_curse(screen, pad, win, "Request log file? y/n: ")
    if get_log == 'y':
        req_dict = {'identity' : identity, 'timestamp': datetime.datetime.now(), 'address' : (), 'content' : '', 'get_log' : True}
        pickle.dumps(req_dict)
        messages.append(req_dict)
        messages_in_queue = True
    getInfo(screen, pad, win)


def get_text_via_curse(screen, pad, win, prompt):
    """
        gets some text from the user using the curse ui
        displays the prompt to the user then recives his input
        NOTE - hit ESC and a BLANK STRING is returned
        NOTE - hit ENTER to finish string
        """
    global padpos

    text = ''
    win.addstr(prompt)
    win.refresh()
    while True: # wait until button is pressed
        event = screen.getch()
        if event == curses.ascii.ESC: # exit if esc is pushed
            curses.nocbreak()
            curses.echo()
            curses.endwin()
            exit()
        # hardcoded for backspace as curses.assci gives
        # 13 instead of the 127 used by lab machines...
        elif event == curses.ascii.ESC | 127:
            text = text[:-1]
            win.clear()
            win.addstr(prompt + text)
            win.refresh()
        # new line char
        elif event == curses.ascii.NL:
            win.clear()
            return text
        # any other char
        else:
            text += (chr(event))
            win.addstr(chr(event))
            win.refresh()

def add_and_update_pad(pad, text):
    """
        updates and refreshes pad with given text
    """
    global padpos

    # updates padpos by an amount equal to lines printed
    padpos += len(text) / 80
    textplusn = text + '\n'
    padpos += 1
    pad.addstr(textplusn)
    pad.refresh(padpos, 0, 0, 0, 19, 80)

def display_manual(pad):
    """
        method to print the help manual
    """
    manual1 = "Help Manual"
    manual2 = "Address - To send a message to multiple addressees - enter user names of all"
    manual2a = "addressees, using commas to seperate them."
    manual3 = "	- To change the addressee(s) you are messaging - enter 'exit' instead"
    manual3a = "of typing in a message."
    manual4 = "Log File - The log  file will display your message history (all of the"
    manual4a = "messages you have ever received)."
    manual5 = "	 - To view the log file - enter 'y' when prompted."
    manual6 = "	 - If a log file is created, the file name will be shown and will be"
    manual6a = "stored in the same directory as the client file."
    manual7 = "	 - If no infomation is stored for that user, no log file will appear"
    manual7a = "in this directory."
    manual8 = "Quitting the program - To quit the instant messaging program - press the"
    manual8a = "Esc key at any time."
    manual9 = "If the display is unreadable, press backspace to refresh the display."

    add_and_update_pad(pad, manual1)
    add_and_update_pad(pad, manual2)
    add_and_update_pad(pad, manual2a)
    add_and_update_pad(pad, manual3)
    add_and_update_pad(pad, manual3a)
    add_and_update_pad(pad, manual4)
    add_and_update_pad(pad, manual4a)
    add_and_update_pad(pad, manual5)
    add_and_update_pad(pad, manual6)
    add_and_update_pad(pad, manual6a)
    add_and_update_pad(pad, manual7)
    add_and_update_pad(pad, manual7a)
    add_and_update_pad(pad, manual8)
    add_and_update_pad(pad, manual8a)
    add_and_update_pad(pad, manual9)

def main(screen):
    """
        curse tui
        NOTES - TERMINAL WINDOW MUST BE AT LEAST 80 BY 24
        """
    global padpos
    global identity

    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(0)
    
    # biiiiig pad for many lines of text
    pad = curses.newpad(10000,80)

    begin_x = 1; begin_y = 21
    height = 2; width = 78
    win = curses.newwin(height, width, begin_y, begin_x)
    boarder1 = curses.newwin(height + 2, width + 2, begin_y - 1, begin_x - 1)
    boarder1.border()
    boarder1.refresh()

    
    pad.addstr("PYTHON MESSAGING SYSYTEM:\n\n")
    pad.refresh(padpos, 0, 0, 0, 19, 80)
    win.clear()
    win.refresh()

    if len(sys.argv) == 1:
        add_and_update_pad(pad, "No address specified, the following servers have been detected:")
        send_multicast(pad)
        addr = get_text_via_curse(screen, pad, win, "Please choose a server: ")
    elif (sys.argv[1] == 'help'):
        display_manual(pad)
        add_and_update_pad(pad, "")
        add_and_update_pad(pad, "No address specified, the following servers have been detected:")

        send_multicast(pad)
        addr = get_text_via_curse(screen, pad, win, "Please choose a server: ")
    else:
        addr = sys.argv[1]

    time.sleep(0.1)


    win.clear()
    pad.refresh(padpos, 0, 0, 0, 19, 80)
    win.refresh()

    # start network tread
    t = threading.Thread(target=connect, args=(addr, pad,))
    t.setDaemon(True)
    t.start()

    # start user interface thread
    u = threading.Thread(target=start_communication, args=(screen, pad, win,))
    u.setDaemon(True)
    u.start()

    # wait.
    u.join()
    
    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    
    curses.wrapper(main)