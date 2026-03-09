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
"""
Package to test the openlp.plugins.songs.forms.authorsform package.
"""
from unittest import TestCase
from unittest.mock import patch

from PyQt5 import QtWidgets

from openlp.core.common import Registry
from openlp.plugins.songs.forms.authorsform import AuthorsForm
from tests.helpers.testmixin import TestMixin


class TestAuthorsForm(TestCase, TestMixin):
    """
    Test the AuthorsForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = AuthorsForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def ui_defaults_test(self):
        """
        Test the AuthorForm defaults are correct
        """
        self.assertEqual(self.form.first_name_edit.text(), '', 'The first name edit should be empty')
        self.assertEqual(self.form.last_name_edit.text(), '', 'The last name edit should be empty')
        self.assertEqual(self.form.display_edit.text(), '', 'The display name edit should be empty')

    def get_first_name_property_test(self):
        """
        Test that getting the first name property on the AuthorForm works correctly
        """
        # GIVEN: A first name to set
        first_name = 'John'

        # WHEN: The first_name_edit's text is set
        self.form.first_name_edit.setText(first_name)

        # THEN: The first_name property should have the correct value
        self.assertEqual(self.form.first_name, first_name, 'The first name property should be correct')

    def set_first_name_property_test(self):
        """
        Test that setting the first name property on the AuthorForm works correctly
        """
        # GIVEN: A first name to set
        first_name = 'James'

        # WHEN: The first_name property is set
        self.form.first_name = first_name

        # THEN: The first_name_edit should have the correct value
        self.assertEqual(self.form.first_name_edit.text(), first_name, 'The first name should be set correctly')

    def get_last_name_property_test(self):
        """
        Test that getting the last name property on the AuthorForm works correctly
        """
        # GIVEN: A last name to set
        last_name = 'Smith'

        # WHEN: The last_name_edit's text is set
        self.form.last_name_edit.setText(last_name)

        # THEN: The last_name property should have the correct value
        self.assertEqual(self.form.last_name, last_name, 'The last name property should be correct')

    def set_last_name_property_test(self):
        """
        Test that setting the last name property on the AuthorForm works correctly
        """
        # GIVEN: A last name to set
        last_name = 'Potter'

        # WHEN: The last_name property is set
        self.form.last_name = last_name

        # THEN: The last_name_edit should have the correct value
        self.assertEqual(self.form.last_name_edit.text(), last_name, 'The last name should be set correctly')

    def get_display_name_property_test(self):
        """
        Test that getting the display name property on the AuthorForm works correctly
        """
        # GIVEN: A display name to set
        display_name = 'John'

        # WHEN: The display_name_edit's text is set
        self.form.display_edit.setText(display_name)

        # THEN: The display_name property should have the correct value
        self.assertEqual(self.form.display_name, display_name, 'The display name property should be correct')

    def set_display_name_property_test(self):
        """
        Test that setting the display name property on the AuthorForm works correctly
        """
        # GIVEN: A display name to set
        display_name = 'John'

        # WHEN: The display_name property is set
        self.form.display_name = display_name

        # THEN: The display_name_edit should have the correct value
        self.assertEqual(self.form.display_edit.text(), display_name, 'The display name should be set correctly')

    @patch('openlp.plugins.songs.forms.authorsform.QtWidgets.QDialog.exec')
    def test_exec(self, mocked_exec):
        """
        Test the exec() method
        """
        # GIVEN: An authors for and various mocked objects
        with patch.object(self.form.first_name_edit, 'clear') as mocked_first_name_edit_clear, \
                patch.object(self.form.last_name_edit, 'clear') as mocked_last_name_edit_clear, \
                patch.object(self.form.display_edit, 'clear') as mocked_display_edit_clear, \
                patch.object(self.form.first_name_edit, 'setFocus') as mocked_first_name_edit_setFocus:
            # WHEN: The exec() method is called
            self.form.exec(clear=True)

            # THEN: The clear and exec() methods should have been called
        mocked_first_name_edit_clear.assert_called_once_with()
        mocked_last_name_edit_clear.assert_called_once_with()
        mocked_display_edit_clear.assert_called_once_with()
        mocked_first_name_edit_setFocus.assert_called_once_with()
        mocked_exec.assert_called_once_with(self.form)

    def test_first_name_edited(self):
        """
        Test the on_first_name_edited() method
        """
        # GIVEN: An author form
        self.form.auto_display_name = True

        with patch.object(self.form.last_name_edit, 'text') as mocked_last_name_edit_text, \
                patch.object(self.form.display_edit, 'setText') as mocked_display_edit_setText:
            mocked_last_name_edit_text.return_value = 'Newton'

            # WHEN: on_first_name_edited() is called
            self.form.on_first_name_edited('John')

        # THEN: The display name should be updated
        assert mocked_last_name_edit_text.call_count == 2
        mocked_display_edit_setText.assert_called_once_with('John Newton')

    def test_first_name_edited_no_auto(self):
        """
        Test the on_first_name_edited() method without auto_display_name
        """
        # GIVEN: An author form
        self.form.auto_display_name = False

        with patch.object(self.form.last_name_edit, 'text') as mocked_last_name_edit_text, \
                patch.object(self.form.display_edit, 'setText') as mocked_display_edit_setText:

            # WHEN: on_first_name_edited() is called
            self.form.on_first_name_edited('John')

        # THEN: The display name should not be updated
        assert mocked_last_name_edit_text.call_count == 0
        assert mocked_display_edit_setText.call_count == 0

    def test_last_name_edited(self):
        """
        Test the on_last_name_edited() method
        """
        # GIVEN: An author form
        self.form.auto_display_name = True

        with patch.object(self.form.first_name_edit, 'text') as mocked_first_name_edit_text, \
                patch.object(self.form.display_edit, 'setText') as mocked_display_edit_setText:
            mocked_first_name_edit_text.return_value = 'John'

            # WHEN: on_last_name_edited() is called
            self.form.on_last_name_edited('Newton')

        # THEN: The display name should be updated
        assert mocked_first_name_edit_text.call_count == 2
        mocked_display_edit_setText.assert_called_once_with('John Newton')

    def test_last_name_edited_no_auto(self):
        """
        Test the on_last_name_edited() method without auto_display_name
        """
        # GIVEN: An author form
        self.form.auto_display_name = False

        with patch.object(self.form.first_name_edit, 'text') as mocked_first_name_edit_text, \
                patch.object(self.form.display_edit, 'setText') as mocked_display_edit_setText:

            # WHEN: on_last_name_edited() is called
            self.form.on_last_name_edited('Newton')

        # THEN: The display name should not be updated
        assert mocked_first_name_edit_text.call_count == 0
        assert mocked_display_edit_setText.call_count == 0

    @patch('openlp.plugins.songs.forms.authorsform.critical_error_message_box')
    def test_accept_no_first_name(self, mocked_critical_error):
        """
        Test the accept() method with no first name
        """
        # GIVEN: A form and no text in thefirst name edit
        with patch.object(self.form.first_name_edit, 'text') as mocked_first_name_edit_text, \
                patch.object(self.form.first_name_edit, 'setFocus') as mocked_first_name_edit_setFocus:
            mocked_first_name_edit_text.return_value = ''

            # WHEN: accept() is called
            result = self.form.accept()

        # THEN: The result should be false and a critical error displayed
        assert result is False
        mocked_critical_error.assert_called_once_with(message='You need to type in the first name of the author.')
        mocked_first_name_edit_text.assert_called_once_with()
        mocked_first_name_edit_setFocus.assert_called_once_with()

    @patch('openlp.plugins.songs.forms.authorsform.critical_error_message_box')
    def test_accept_no_last_name(self, mocked_critical_error):
        """
        Test the accept() method with no last name
        """
        # GIVEN: A form and no text in the last name edit
        with patch.object(self.form.first_name_edit, 'text') as mocked_first_name_edit_text, \
                patch.object(self.form.last_name_edit, 'text') as mocked_last_name_edit_text, \
                patch.object(self.form.last_name_edit, 'setFocus') as mocked_last_name_edit_setFocus:
            mocked_first_name_edit_text.return_value = 'John'
            mocked_last_name_edit_text.return_value = ''

            # WHEN: accept() is called
            result = self.form.accept()

        # THEN: The result should be false and a critical error displayed
        assert result is False
        mocked_critical_error.assert_called_once_with(message='You need to type in the last name of the author.')
        mocked_first_name_edit_text.assert_called_once_with()
        mocked_last_name_edit_text.assert_called_once_with()
        mocked_last_name_edit_setFocus.assert_called_once_with()

    @patch('openlp.plugins.songs.forms.authorsform.critical_error_message_box')
    def test_accept_no_display_name_no_combine(self, mocked_critical_error):
        """
        Test the accept() method with no display name and no combining
        """
        # GIVEN: A form and no text in the display name edit
        mocked_critical_error.return_value = QtWidgets.QMessageBox.No
        with patch.object(self.form.first_name_edit, 'text') as mocked_first_name_edit_text, \
                patch.object(self.form.last_name_edit, 'text') as mocked_last_name_edit_text, \
                patch.object(self.form.display_edit, 'text') as mocked_display_edit_text, \
                patch.object(self.form.display_edit, 'setFocus') as mocked_display_edit_setFocus:
            mocked_first_name_edit_text.return_value = 'John'
            mocked_last_name_edit_text.return_value = 'Newton'
            mocked_display_edit_text.return_value = ''

            # WHEN: accept() is called
            result = self.form.accept()

        # THEN: The result should be false and a critical error displayed
        assert result is False
        mocked_critical_error.assert_called_once_with(
            message='You have not set a display name for the author, combine the first and last names?',
            parent=self.form, question=True)
        mocked_first_name_edit_text.assert_called_once_with()
        mocked_last_name_edit_text.assert_called_once_with()
        mocked_display_edit_text.assert_called_once_with()
        mocked_display_edit_setFocus.assert_called_once_with()

    @patch('openlp.plugins.songs.forms.authorsform.critical_error_message_box')
    @patch('openlp.plugins.songs.forms.authorsform.QtWidgets.QDialog.accept')
    def test_accept_no_display_name(self, mocked_accept, mocked_critical_error):
        """
        Test the accept() method with no display name and auto-combine
        """
        # GIVEN: A form and no text in the display name edit
        mocked_accept.return_value = True
        mocked_critical_error.return_value = QtWidgets.QMessageBox.Yes
        with patch.object(self.form.first_name_edit, 'text') as mocked_first_name_edit_text, \
                patch.object(self.form.last_name_edit, 'text') as mocked_last_name_edit_text, \
                patch.object(self.form.display_edit, 'text') as mocked_display_edit_text, \
                patch.object(self.form.display_edit, 'setText') as mocked_display_edit_setText:
            mocked_first_name_edit_text.return_value = 'John'
            mocked_last_name_edit_text.return_value = 'Newton'
            mocked_display_edit_text.return_value = ''

            # WHEN: accept() is called
            result = self.form.accept()

        # THEN: The result should be false and a critical error displayed
        assert result is True
        mocked_critical_error.assert_called_once_with(
            message='You have not set a display name for the author, combine the first and last names?',
            parent=self.form, question=True)
        assert mocked_first_name_edit_text.call_count == 2
        assert mocked_last_name_edit_text.call_count == 2
        mocked_display_edit_text.assert_called_once_with()
        mocked_display_edit_setText.assert_called_once_with('John Newton')
        mocked_accept.assert_called_once_with(self.form)

    @patch('openlp.plugins.songs.forms.authorsform.QtWidgets.QDialog.accept')
    def test_accept(self, mocked_accept):
        """
        Test the accept() method
        """
        # GIVEN: A form and text in the right places
        mocked_accept.return_value = True
        with patch.object(self.form.first_name_edit, 'text') as mocked_first_name_edit_text, \
                patch.object(self.form.last_name_edit, 'text') as mocked_last_name_edit_text, \
                patch.object(self.form.display_edit, 'text') as mocked_display_edit_text:
            mocked_first_name_edit_text.return_value = 'John'
            mocked_last_name_edit_text.return_value = 'Newton'
            mocked_display_edit_text.return_value = 'John Newton'

            # WHEN: accept() is called
            result = self.form.accept()

        # THEN: The result should be false and a critical error displayed
        assert result is True
        mocked_first_name_edit_text.assert_called_once_with()
        mocked_last_name_edit_text.assert_called_once_with()
        mocked_display_edit_text.assert_called_once_with()
        mocked_accept.assert_called_once_with(self.form)
