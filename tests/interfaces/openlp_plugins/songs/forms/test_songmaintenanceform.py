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
Package to test the openlp.plugins.songs.forms.songmaintenanceform package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import Registry, UiStrings
from openlp.plugins.songs.forms.songmaintenanceform import SongMaintenanceForm

from tests.helpers.testmixin import TestMixin


class TestSongMaintenanceForm(TestCase, TestMixin):
    """
    Test the SongMaintenanceForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.mocked_manager = MagicMock()
        self.form = SongMaintenanceForm(self.mocked_manager)

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def test_constructor(self):
        """
        Test that a SongMaintenanceForm is created successfully
        """
        # GIVEN: A SongMaintenanceForm
        # WHEN: The form is created
        # THEN: It should have some of the right components
        assert self.form is not None
        assert self.form.manager is self.mocked_manager

    @patch.object(QtWidgets.QDialog, 'exec')
    def test_exect(self, mocked_exec):
        """
        Test the song maintenance form being executed
        """
        # GIVEN: A song maintenance form
        mocked_exec.return_value = True

        # WHEN: The song mainetnance form is executed
        with patch.object(self.form, 'type_list_widget') as mocked_type_list_widget, \
                patch.object(self.form, 'reset_authors') as mocked_reset_authors, \
                patch.object(self.form, 'reset_topics') as mocked_reset_topics, \
                patch.object(self.form, 'reset_song_books') as mocked_reset_song_books:
            result = self.form.exec(from_song_edit=True)

        # THEN: The correct methods should have been called
        assert self.form.from_song_edit is True
        mocked_type_list_widget.setCurrentRow.assert_called_once_with(0)
        mocked_reset_authors.assert_called_once_with()
        mocked_reset_topics.assert_called_once_with()
        mocked_reset_song_books.assert_called_once_with()
        mocked_type_list_widget.setFocus.assert_called_once_with()
        mocked_exec.assert_called_once_with(self.form)
        assert result is True

    def test_get_current_item_id_no_item(self):
        """
        Test _get_current_item_id() when there's no item
        """
        # GIVEN: A song maintenance form without a selected item
        mocked_list_widget = MagicMock()
        mocked_list_widget.currentItem.return_value = None

        # WHEN: _get_current_item_id() is called
        result = self.form._get_current_item_id(mocked_list_widget)

        # THEN: The result should be -1
        mocked_list_widget.currentItem.assert_called_once_with()
        assert result == -1

    def test_get_current_item_id(self):
        """
        Test _get_current_item_id() when there's a valid item
        """
        # GIVEN: A song maintenance form with a selected item
        mocked_item = MagicMock()
        mocked_item.data.return_value = 7
        mocked_list_widget = MagicMock()
        mocked_list_widget.currentItem.return_value = mocked_item

        # WHEN: _get_current_item_id() is called
        result = self.form._get_current_item_id(mocked_list_widget)

        # THEN: The result should be -1
        mocked_list_widget.currentItem.assert_called_once_with()
        mocked_item.data.assert_called_once_with(QtCore.Qt.UserRole)
        assert result == 7

    @patch('openlp.plugins.songs.forms.songmaintenanceform.critical_error_message_box')
    def test_delete_item_no_item_id(self, mocked_critical_error_message_box):
        """
        Test the _delete_item() method when there is no item selected
        """
        # GIVEN: Some mocked items
        mocked_item_class = MagicMock()
        mocked_list_widget = MagicMock()
        mocked_reset_func = MagicMock()
        dialog_title = 'Delete Item'
        delete_text = 'Are you sure you want to delete this item?'
        error_text = 'There was a problem deleting this item'

        # WHEN: _delete_item() is called
        with patch.object(self.form, '_get_current_item_id') as mocked_get_current_item_id:
            mocked_get_current_item_id.return_value = -1
            self.form._delete_item(mocked_item_class, mocked_list_widget, mocked_reset_func, dialog_title, delete_text,
                                   error_text)

        # THEN: The right things should have been called
        mocked_get_current_item_id.assert_called_once_with(mocked_list_widget)
        mocked_critical_error_message_box.assert_called_once_with(dialog_title, UiStrings().NISs)

    @patch('openlp.plugins.songs.forms.songmaintenanceform.critical_error_message_box')
    def test_delete_item_invalid_item(self, mocked_critical_error_message_box):
        """
        Test the _delete_item() method when the item doesn't exist in the database
        """
        # GIVEN: Some mocked items
        self.mocked_manager.get_object.return_value = None
        mocked_item_class = MagicMock()
        mocked_list_widget = MagicMock()
        mocked_reset_func = MagicMock()
        dialog_title = 'Delete Item'
        delete_text = 'Are you sure you want to delete this item?'
        error_text = 'There was a problem deleting this item'

        # WHEN: _delete_item() is called
        with patch.object(self.form, '_get_current_item_id') as mocked_get_current_item_id:
            mocked_get_current_item_id.return_value = 1
            self.form._delete_item(mocked_item_class, mocked_list_widget, mocked_reset_func, dialog_title, delete_text,
                                   error_text)

        # THEN: The right things should have been called
        mocked_get_current_item_id.assert_called_once_with(mocked_list_widget)
        self.mocked_manager.get_object.assert_called_once_with(mocked_item_class, 1)
        mocked_critical_error_message_box.assert_called_once_with(dialog_title, error_text)

    @patch('openlp.plugins.songs.forms.songmaintenanceform.critical_error_message_box')
    def test_delete_item(self, mocked_critical_error_message_box):
        """
        Test the _delete_item() method
        """
        # GIVEN: Some mocked items
        mocked_item = MagicMock()
        mocked_item.songs = []
        mocked_item.id = 1
        self.mocked_manager.get_object.return_value = mocked_item
        mocked_critical_error_message_box.return_value = QtWidgets.QMessageBox.Yes
        mocked_item_class = MagicMock()
        mocked_list_widget = MagicMock()
        mocked_reset_func = MagicMock()
        dialog_title = 'Delete Item'
        delete_text = 'Are you sure you want to delete this item?'
        error_text = 'There was a problem deleting this item'

        # WHEN: _delete_item() is called
        with patch.object(self.form, '_get_current_item_id') as mocked_get_current_item_id:
            mocked_get_current_item_id.return_value = 1
            self.form._delete_item(mocked_item_class, mocked_list_widget, mocked_reset_func, dialog_title, delete_text,
                                   error_text)

        # THEN: The right things should have been called
        mocked_get_current_item_id.assert_called_once_with(mocked_list_widget)
        self.mocked_manager.get_object.assert_called_once_with(mocked_item_class, 1)
        mocked_critical_error_message_box.assert_called_once_with(dialog_title, delete_text, self.form, True)
        self.mocked_manager.delete_object(mocked_item_class, 1)
        mocked_reset_func.assert_called_once_with()

    @patch('openlp.plugins.songs.forms.songmaintenanceform.QtWidgets.QListWidgetItem')
    @patch('openlp.plugins.songs.forms.songmaintenanceform.Author')
    def test_reset_authors(self, MockedAuthor, MockedQListWidgetItem):
        """
        Test the reset_authors() method
        """
        # GIVEN: A mocked authors_list_widget and a few other mocks
        mocked_author1 = MagicMock()
        mocked_author1.display_name = 'John Newton'
        mocked_author1.id = 1
        mocked_author2 = MagicMock()
        mocked_author2.display_name = None
        mocked_author2.first_name = 'John'
        mocked_author2.last_name = 'Wesley'
        mocked_author2.id = 2
        mocked_authors = [mocked_author1, mocked_author2]
        mocked_author_item1 = MagicMock()
        mocked_author_item2 = MagicMock()
        MockedQListWidgetItem.side_effect = [mocked_author_item1, mocked_author_item2]
        MockedAuthor.display_name = None
        self.mocked_manager.get_all_objects.return_value = mocked_authors

        # WHEN: reset_authors() is called
        with patch.object(self.form, 'authors_list_widget') as mocked_authors_list_widget:
            self.form.reset_authors()

        # THEN: The authors list should be reset
        expected_widget_item_calls = [call('John Newton'), call('John Wesley')]
        mocked_authors_list_widget.clear.assert_called_once_with()
        self.mocked_manager.get_all_objects.assert_called_once_with(MockedAuthor,
                                                                    order_by_ref=MockedAuthor.display_name)
        assert MockedQListWidgetItem.call_args_list == expected_widget_item_calls, MockedQListWidgetItem.call_args_list
        mocked_author_item1.setData.assert_called_once_with(QtCore.Qt.UserRole, 1)
        mocked_author_item2.setData.assert_called_once_with(QtCore.Qt.UserRole, 2)
        mocked_authors_list_widget.addItem.call_args_list == [
            call(mocked_author_item1), call(mocked_author_item2)]

    @patch('openlp.plugins.songs.forms.songmaintenanceform.QtWidgets.QListWidgetItem')
    @patch('openlp.plugins.songs.forms.songmaintenanceform.Topic')
    def test_reset_topics(self, MockedTopic, MockedQListWidgetItem):
        """
        Test the reset_topics() method
        """
        # GIVEN: Some mocked out objects and methods
        MockedTopic.name = 'Grace'
        mocked_topic = MagicMock()
        mocked_topic.id = 1
        mocked_topic.name = 'Grace'
        self.mocked_manager.get_all_objects.return_value = [mocked_topic]
        mocked_topic_item = MagicMock()
        MockedQListWidgetItem.return_value = mocked_topic_item

        # WHEN: reset_topics() is called
        with patch.object(self.form, 'topics_list_widget') as mocked_topic_list_widget:
            self.form.reset_topics()

        # THEN: The topics list should be reset correctly
        mocked_topic_list_widget.clear.assert_called_once_with()
        self.mocked_manager.get_all_objects.assert_called_once_with(MockedTopic, order_by_ref=MockedTopic.name)
        MockedQListWidgetItem.assert_called_once_with('Grace')
        mocked_topic_item.setData.assert_called_once_with(QtCore.Qt.UserRole, 1)
        mocked_topic_list_widget.addItem.assert_called_once_with(mocked_topic_item)

    @patch('openlp.plugins.songs.forms.songmaintenanceform.QtWidgets.QListWidgetItem')
    @patch('openlp.plugins.songs.forms.songmaintenanceform.Book')
    def test_reset_song_books(self, MockedBook, MockedQListWidgetItem):
        """
        Test the reset_song_books() method
        """
        # GIVEN: Some mocked out objects and methods
        MockedBook.name = 'Hymnal'
        mocked_song_book = MagicMock()
        mocked_song_book.id = 1
        mocked_song_book.name = 'Hymnal'
        mocked_song_book.publisher = 'Hymns and Psalms, Inc.'
        self.mocked_manager.get_all_objects.return_value = [mocked_song_book]
        mocked_song_book_item = MagicMock()
        MockedQListWidgetItem.return_value = mocked_song_book_item

        # WHEN: reset_song_books() is called
        with patch.object(self.form, 'song_books_list_widget') as mocked_song_book_list_widget:
            self.form.reset_song_books()

        # THEN: The song_books list should be reset correctly
        mocked_song_book_list_widget.clear.assert_called_once_with()
        self.mocked_manager.get_all_objects.assert_called_once_with(MockedBook, order_by_ref=MockedBook.name)
        MockedQListWidgetItem.assert_called_once_with('Hymnal (Hymns and Psalms, Inc.)')
        mocked_song_book_item.setData.assert_called_once_with(QtCore.Qt.UserRole, 1)
        mocked_song_book_list_widget.addItem.assert_called_once_with(mocked_song_book_item)

    @patch('openlp.plugins.songs.forms.songmaintenanceform.and_')
    @patch('openlp.plugins.songs.forms.songmaintenanceform.Author')
    def test_check_author_exists(self, MockedAuthor, mocked_and):
        """
        Test the check_author_exists() method
        """
        # GIVEN: A bunch of mocked out stuff
        MockedAuthor.first_name = 'John'
        MockedAuthor.last_name = 'Newton'
        MockedAuthor.display_name = 'John Newton'
        mocked_new_author = MagicMock()
        mocked_new_author.first_name = 'John'
        mocked_new_author.last_name = 'Newton'
        mocked_new_author.display_name = 'John Newton'
        mocked_and.return_value = True
        mocked_authors = [MagicMock(), MagicMock()]
        self.mocked_manager.get_all_objects.return_value = mocked_authors

        # WHEN: check_author_exists() is called
        with patch.object(self.form, '_check_object_exists') as mocked_check_object_exists:
            mocked_check_object_exists.return_value = True
            result = self.form.check_author_exists(mocked_new_author, edit=True)

        # THEN: The correct result is returned
        mocked_and.assert_called_once_with(True, True, True)
        self.mocked_manager.get_all_objects.assert_called_once_with(MockedAuthor, True)
        mocked_check_object_exists.assert_called_once_with(mocked_authors, mocked_new_author, True)
        assert result is True

    @patch('openlp.plugins.songs.forms.songmaintenanceform.Topic')
    def test_check_topic_exists(self, MockedTopic):
        """
        Test the check_topic_exists() method
        """
        # GIVEN: Some mocked stuff
        MockedTopic.name = 'Grace'
        mocked_new_topic = MagicMock()
        mocked_new_topic.name = 'Grace'
        mocked_topics = [MagicMock(), MagicMock()]
        self.mocked_manager.get_all_objects.return_value = mocked_topics

        # WHEN: check_topic_exists() is run
        with patch.object(self.form, '_check_object_exists') as mocked_check_object_exists:
            mocked_check_object_exists.return_value = True
            result = self.form.check_topic_exists(mocked_new_topic, True)

        # THEN: The correct things should have been called
        self.mocked_manager.get_all_objects.assert_called_once_with(MockedTopic, True)
        mocked_check_object_exists.assert_called_once_with(mocked_topics, mocked_new_topic, True)
        assert result is True

    @patch('openlp.plugins.songs.forms.songmaintenanceform.and_')
    @patch('openlp.plugins.songs.forms.songmaintenanceform.Book')
    def test_check_song_book_exists(self, MockedBook, mocked_and):
        """
        Test the check_song_book_exists() method
        """
        # GIVEN: Some mocked stuff
        MockedBook.name = 'Hymns'
        MockedBook.publisher = 'Christian Songs'
        mocked_new_book = MagicMock()
        mocked_new_book.name = 'Hymns'
        mocked_new_book.publisher = 'Christian Songs'
        mocked_and.return_value = True
        mocked_books = [MagicMock(), MagicMock()]
        self.mocked_manager.get_all_objects.return_value = mocked_books

        # WHEN: check_book_exists() is run
        with patch.object(self.form, '_check_object_exists') as mocked_check_object_exists:
            mocked_check_object_exists.return_value = True
            result = self.form.check_song_book_exists(mocked_new_book, True)

        # THEN: The correct things should have been called
        mocked_and.assert_called_once_with(True, True)
        self.mocked_manager.get_all_objects.assert_called_once_with(MockedBook, True)
        mocked_check_object_exists.assert_called_once_with(mocked_books, mocked_new_book, True)
        assert result is True

    def test_check_object_exists_no_existing_objects(self):
        """
        Test the _check_object_exists() method when there are no existing objects
        """
        # GIVEN: A SongMaintenanceForm instance
        # WHEN: _check_object_exists() is called without existing objects
        result = self.form._check_object_exists([], None, False)

        # THEN: The result should be True
        assert result is True

    def test_check_object_exists_without_edit(self):
        """
        Test the _check_object_exists() method when edit is false
        """
        # GIVEN: A SongMaintenanceForm instance
        # WHEN: _check_object_exists() is called with edit set to false
        result = self.form._check_object_exists([MagicMock()], None, False)

        # THEN: The result should be False
        assert result is False

    def test_check_object_exists_not_found(self):
        """
        Test the _check_object_exists() method when the object is not found
        """
        # GIVEN: A SongMaintenanceForm instance and some mocked objects
        mocked_existing_objects = [MagicMock(id=1)]
        mocked_new_object = MagicMock(id=2)

        # WHEN: _check_object_exists() is called with edit set to false
        result = self.form._check_object_exists(mocked_existing_objects, mocked_new_object, True)

        # THEN: The result should be False
        assert result is False

    def test_check_object_exists(self):
        """
        Test the _check_object_exists() method
        """
        # GIVEN: A SongMaintenanceForm instance and some mocked objects
        mocked_existing_objects = [MagicMock(id=1)]
        mocked_new_object = MagicMock(id=1)

        # WHEN: _check_object_exists() is called with edit set to false
        result = self.form._check_object_exists(mocked_existing_objects, mocked_new_object, True)

        # THEN: The result should be False
        assert result is True
