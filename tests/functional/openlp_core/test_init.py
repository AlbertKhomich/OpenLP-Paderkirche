# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2017 OpenLP Developers                                   #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

from PyQt5 import QtWidgets

from openlp.core import OpenLP, parse_options


class TestInitFunctions(TestCase):

    def parse_options_basic_test(self):
        """
        Test the parse options process works

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = []
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, 'warning', 'The log level should be set to warning')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, [], 'The service file should be blank')

    def parse_options_debug_test(self):
        """
        Test the parse options process works for debug only

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['-l debug']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, ' debug', 'The log level should be set to debug')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, [], 'The service file should be blank')

    def parse_options_debug_and_portable_test(self):
        """
        Test the parse options process works for debug and portable

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['--portable']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, 'warning', 'The log level should be set to warning')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertTrue(args.portable, 'The portable flag should be set to true')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, [], 'The service file should be blank')

    def parse_options_all_no_file_test(self):
        """
        Test the parse options process works with two options

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['-l debug', '-d']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertTrue(args.dev_version, 'The dev_version flag should be True')
        self.assertEquals(args.loglevel, ' debug', 'The log level should be set to debug')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, [], 'The service file should be blank')

    def parse_options_file_test(self):
        """
        Test the parse options process works with a file

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['dummy_temp']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, 'warning', 'The log level should be set to warning')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, 'dummy_temp', 'The service file should not be blank')

    def parse_options_file_and_debug_test(self):
        """
        Test the parse options process works with a file and the debug log level

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['-l debug', 'dummy_temp']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, ' debug', 'The log level should be set to debug')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, 'dummy_temp', 'The service file should not be blank')


class TestOpenLP(TestCase):
    """
    Test the OpenLP app class
    """
    @patch('openlp.core.QtWidgets.QApplication.exec')
    def test_exec(self, mocked_exec):
        """
        Test the exec method
        """
        # GIVEN: An app
        app = OpenLP([])
        app.shared_memory = MagicMock()
        mocked_exec.return_value = False

        # WHEN: exec() is called
        result = app.exec()

        # THEN: The right things should be called
        assert app.is_event_loop_active is True
        mocked_exec.assert_called_once_with()
        app.shared_memory.detach.assert_called_once_with()
        assert result is False

        del app

    @patch('openlp.core.QtCore.QSharedMemory')
    def test_is_already_running_not_running(self, MockedSharedMemory):
        """
        Test the is_already_running() method when OpenLP is NOT running
        """
        # GIVEN: An OpenLP app and some mocks
        mocked_shared_memory = MagicMock()
        mocked_shared_memory.attach.return_value = False
        MockedSharedMemory.return_value = mocked_shared_memory
        app = OpenLP([])

        # WHEN: is_already_running() is called
        result = app.is_already_running()

        # THEN: The result should be false
        MockedSharedMemory.assert_called_once_with('OpenLP')
        mocked_shared_memory.attach.assert_called_once_with()
        mocked_shared_memory.create.assert_called_once_with(1)
        assert result is False

    @patch('openlp.core.QtWidgets.QMessageBox.critical')
    @patch('openlp.core.QtWidgets.QMessageBox.StandardButtons')
    @patch('openlp.core.QtCore.QSharedMemory')
    def test_is_already_running_is_running_continue(self, MockedSharedMemory, MockedStandardButtons, mocked_critical):
        """
        Test the is_already_running() method when OpenLP IS running and the user chooses to continue
        """
        # GIVEN: An OpenLP app and some mocks
        mocked_shared_memory = MagicMock()
        mocked_shared_memory.attach.return_value = True
        MockedSharedMemory.return_value = mocked_shared_memory
        MockedStandardButtons.return_value = 0
        mocked_critical.return_value = QtWidgets.QMessageBox.Yes
        app = OpenLP([])

        # WHEN: is_already_running() is called
        result = app.is_already_running()

        # THEN: The result should be false
        MockedSharedMemory.assert_called_once_with('OpenLP')
        mocked_shared_memory.attach.assert_called_once_with()
        MockedStandardButtons.assert_called_once_with(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        mocked_critical.assert_called_once_with(None, 'Error', 'OpenLP is already running. Do you wish to continue?', 0)
        assert result is False

    @patch('openlp.core.QtWidgets.QMessageBox.critical')
    @patch('openlp.core.QtWidgets.QMessageBox.StandardButtons')
    @patch('openlp.core.QtCore.QSharedMemory')
    def test_is_already_running_is_running_stop(self, MockedSharedMemory, MockedStandardButtons, mocked_critical):
        """
        Test the is_already_running() method when OpenLP IS running and the user chooses to stop
        """
        # GIVEN: An OpenLP app and some mocks
        mocked_shared_memory = MagicMock()
        mocked_shared_memory.attach.return_value = True
        MockedSharedMemory.return_value = mocked_shared_memory
        MockedStandardButtons.return_value = 0
        mocked_critical.return_value = QtWidgets.QMessageBox.No
        app = OpenLP([])

        # WHEN: is_already_running() is called
        result = app.is_already_running()

        # THEN: The result should be false
        MockedSharedMemory.assert_called_once_with('OpenLP')
        mocked_shared_memory.attach.assert_called_once_with()
        MockedStandardButtons.assert_called_once_with(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        mocked_critical.assert_called_once_with(None, 'Error', 'OpenLP is already running. Do you wish to continue?', 0)
        assert result is True
