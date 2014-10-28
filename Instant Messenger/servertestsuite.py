#!/usr/bin/env python

"""Test suite for workingserver.py"""

import unittest
import server_fin_mult
import pickle

class test_unit_tests(unittest.TestCase):

    def test_no_message_on_server(self):
        """
            tests output when there is nothing in dictionary and request is made
            output should be an empty list
            """
        server_fin_mult.message_dictionary = {}
        message = {'get_log':False, 'identity':'user', 'address':(), 'content':'no address, therefore this message requests an update from server'}
        output = server_fin_mult.receive_message(message)
        self.assertEqual(output, [])

    def test_pass_message(self):
        """
            tests message is passed across users
            user 1 sends a message to user 2
            output should be a list containing the message sent
            after passing the message, the messagedictionary should be empty
            """

        server_fin_mult.message_dictionary = {}
        message1 = {'get_log':False, 'identity':'user1', 'address':('user2',), 'content':'blahblahblah'}
        user1_output = server_fin_mult.receive_message(message1)
        message2 = {'get_log':False, 'identity':'user2', 'address':(), 'content':''}
        user2_output = server_fin_mult.receive_message(message2)
        user2_expected_output = [message1, ]

        self.assertEqual(user1_output, [])
        self.assertEqual(user2_output, user2_expected_output)
        # after passing the message, the messagedictionary should be empty
        self.assertEqual(len(server_fin_mult.message_dictionary), 0)


#calls main function
if __name__ == '__main__':
    unittest.main()