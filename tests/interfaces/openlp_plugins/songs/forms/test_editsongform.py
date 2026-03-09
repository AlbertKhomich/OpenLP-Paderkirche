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
Package to test the openlp.plugins.songs.forms.editsongform package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import Registry
from openlp.core.common.uistrings import UiStrings
from openlp.plugins.songs.forms.editsongform import EditSongForm
from tests.helpers.testmixin import TestMixin


class TestEditSongForm(TestCase, TestMixin):
    """
    Test the EditSongForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        Registry().register('theme_manager', MagicMock())
        self.form = EditSongForm(MagicMock(), self.main_window, MagicMock())

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def ui_defaults_test(self):
        """
        Test that the EditSongForm defaults are correct
        """
        self.assertFalse(self.form.verse_edit_button.isEnabled(), 'The verse edit button should not be enabled')
        self.assertFalse(self.form.verse_delete_button.isEnabled(), 'The verse delete button should not be enabled')
        self.assertFalse(self.form.author_remove_button.isEnabled(), 'The author remove button should not be enabled')
        self.assertFalse(self.form.topic_remove_button.isEnabled(), 'The topic remove button should not be enabled')

    def is_verse_edit_form_executed_test(self):
        pass

    def verse_order_no_warning_test(self):
        """
        Test if the verse order warning is not shown
        """
        # GIVEN: Mocked methods.
        given_verse_order = 'V1 V2'
        self.form.verse_list_widget.rowCount = MagicMock(return_value=2)
        # Mock out the verse.
        first_verse = MagicMock()
        first_verse.data.return_value = 'V1'
        second_verse = MagicMock()
        second_verse.data.return_value = 'V2'
        self.form.verse_list_widget.item = MagicMock(side_effect=[first_verse, second_verse])
        self.form._extract_verse_order = MagicMock(return_value=given_verse_order.split())

        # WHEN: Call the method.
        self.form.on_verse_order_text_changed(given_verse_order)

        # THEN: No text should be shown.
        assert self.form.warning_label.text() == '', 'There should be no warning.'

    def verse_order_incomplete_warning_test(self):
        """
        Test if the verse-order-incomple warning is shown
        """
        # GIVEN: Mocked methods.
        given_verse_order = 'V1'
        self.form.verse_list_widget.rowCount = MagicMock(return_value=2)
        # Mock out the verse.
        first_verse = MagicMock()
        first_verse.data.return_value = 'V1'
        second_verse = MagicMock()
        second_verse.data.return_value = 'V2'
        self.form.verse_list_widget.item = MagicMock(side_effect=[first_verse, second_verse])
        self.form._extract_verse_order = MagicMock(return_value=[given_verse_order])

        # WHEN: Call the method.
        self.form.on_verse_order_text_changed(given_verse_order)

        # THEN: The verse-order-incomplete text should be shown.
        assert self.form.warning_label.text() == self.form.not_all_verses_used_warning, \
            'The verse-order-incomplete warning should be shown.'

    def bug_1170435_test(self):
        """
        Regression test for bug 1170435 (test if "no verse order" message is shown)
        """
        # GIVEN: Mocked methods.
        given_verse_order = ''
        self.form.verse_list_widget.rowCount = MagicMock(return_value=1)
        # Mock out the verse. (We want a verse type to be returned).
        mocked_verse = MagicMock()
        mocked_verse.data.return_value = 'V1'
        self.form.verse_list_widget.item = MagicMock(return_value=mocked_verse)
        self.form._extract_verse_order = MagicMock(return_value=[])
        self.form.verse_order_edit.text = MagicMock(return_value=given_verse_order)
        # WHEN: Call the method.
        self.form.on_verse_order_text_changed(given_verse_order)

        # THEN: The no-verse-order message should be shown.
        assert self.form.warning_label.text() == self.form.no_verse_order_entered_warning,  \
            'The no-verse-order message should be shown.'

    def bug_1404967_test(self):
        """
        Test for CCLI label showing correct text
        """
        # GIVEN; Mocked methods
        form = self.form
        # THEN: CCLI label should be CCLI song label
        self.assertNotEquals(form.ccli_label.text(), UiStrings().CCLINumberLabel,
                             'CCLI label should not be "{}"'.format(UiStrings().CCLINumberLabel))
        self.assertEquals(form.ccli_label.text(), UiStrings().CCLISongNumberLabel,
                          'CCLI label text should be "{}"'.format(UiStrings().CCLISongNumberLabel))

    def verse_order_lowercase_test(self):
        """
        Test that entering a verse order in lowercase automatically converts to uppercase
        """
        # GIVEN; Mocked methods
        form = self.form

        # WHEN: We enter a verse order in lowercase
        form.verse_order_edit.setText('v1 v2 c1 v3 c1 v4 c1')
        # Need to manually trigger this method as it is only triggered by manual input
        form.on_verse_order_text_changed(form.verse_order_edit.text())

        # THEN: The verse order should be converted to uppercase
        self.assertEqual(form.verse_order_edit.text(), 'V1 V2 C1 V3 C1 V4 C1')

    @patch('openlp.plugins.songs.forms.editsongform.QtWidgets.QListWidgetItem')
    def test_add_author_to_list(self, MockedQListWidgetItem):
        """
        Test the _add_author_to_list() method
        """
        # GIVEN: A song edit form and some mocked stuff
        mocked_author = MagicMock()
        mocked_author.id = 1
        mocked_author.get_display_name.return_value = 'John Newton'
        mocked_author_type = 'words'
        mocked_widget_item = MagicMock()
        MockedQListWidgetItem.return_value = mocked_widget_item

        # WHEN: _add_author_to_list() is called
        with patch.object(self.form.authors_list_view, 'addItem') as mocked_add_item:
            self.form._add_author_to_list(mocked_author, mocked_author_type)

        # THEN: All the correct methods should have been called
        mocked_author.get_display_name.assert_called_once_with('words')
        MockedQListWidgetItem.assert_called_once_with('John Newton')
        mocked_widget_item.setData.assert_called_once_with(QtCore.Qt.UserRole, (1, mocked_author_type))
        mocked_add_item.assert_called_once_with(mocked_widget_item)

    @patch('openlp.plugins.songs.forms.editsongform.SongBookEntry')
    @patch('openlp.plugins.songs.forms.editsongform.QtWidgets.QListWidgetItem')
    def test_add_songbook_entry_to_list(self, MockedQListWidgetItem, MockedSongbookEntry):
        """
        Test the add_songbook_entry_to_list() method
        """
        # GIVEN: A song edit form and some mocked stuff
        songbook_id = 1
        songbook_name = 'Hymnal'
        entry = '546'
        MockedSongbookEntry.get_display_name.return_value = 'Hymnal #546'
        mocked_widget_item = MagicMock()
        MockedQListWidgetItem.return_value = mocked_widget_item

        # WHEN: _add_author_to_list() is called
        with patch.object(self.form.songbooks_list_view, 'addItem') as mocked_add_item:
            self.form.add_songbook_entry_to_list(songbook_id, songbook_name, entry)

        # THEN: All the correct methods should have been called
        MockedSongbookEntry.get_display_name.assert_called_once_with(songbook_name, entry)
        MockedQListWidgetItem.assert_called_once_with('Hymnal #546')
        mocked_widget_item.setData.assert_called_once_with(QtCore.Qt.UserRole, (songbook_id, entry))
        mocked_add_item.assert_called_once_with(mocked_widget_item)
