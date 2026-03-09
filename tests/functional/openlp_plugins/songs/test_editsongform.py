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
This module contains tests for the lib submodule of the Songs plugin.
"""
from unittest import TestCase

from PyQt5 import QtCore

from openlp.core.common import Registry, Settings
from openlp.core.lib import ServiceItem
from openlp.plugins.songs.forms.editsongform import EditSongForm
from openlp.plugins.songs.lib.db import AuthorType
from tests.functional import patch, MagicMock
from tests.helpers.testmixin import TestMixin


class TestEditSongForm(TestCase, TestMixin):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Set up the components need for all tests.
        """
        Registry.create()
        Registry().register('service_list', MagicMock())
        Registry().register('main_window', MagicMock())
        with patch('openlp.plugins.songs.forms.editsongform.EditSongForm.__init__', return_value=None):
            self.edit_song_form = EditSongForm(None, MagicMock(), MagicMock())
        self.setup_application()
        self.build_settings()
        QtCore.QLocale.setDefault(QtCore.QLocale('en_GB'))

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.destroy_settings()

    def validate_matching_tags_test(self):
        # Given a set of tags
        tags = ['{r}', '{/r}', '{bl}', '{/bl}', '{su}', '{/su}']

        # WHEN we validate them
        valid = self.edit_song_form._validate_tags(tags)

        # THEN they should be valid
        self.assertTrue(valid, "The tags list should be valid")

    def validate_nonmatching_tags_test(self):
        # Given a set of tags
        tags = ['{r}', '{/r}', '{bl}', '{/bl}', '{br}', '{su}', '{/su}']

        # WHEN we validate them
        valid = self.edit_song_form._validate_tags(tags)

        # THEN they should be valid
        self.assertTrue(valid, "The tags list should be valid")

    @patch('openlp.plugins.songs.forms.editsongform.set_case_insensitive_completer')
    def test_load_objects(self, mocked_set_case_insensitive_completer):
        """
        Test the _load_objects() method
        """
        # GIVEN: A song edit form and some mocked stuff
        mocked_class = MagicMock()
        mocked_class.name = 'Author'
        mocked_combo = MagicMock()
        mocked_combo.count.return_value = 0
        mocked_cache = MagicMock()
        mocked_object = MagicMock()
        mocked_object.name = 'Charles'
        mocked_object.id = 1
        mocked_manager = MagicMock()
        mocked_manager.get_all_objects.return_value = [mocked_object]
        self.edit_song_form.manager = mocked_manager

        # WHEN: _load_objects() is called
        self.edit_song_form._load_objects(mocked_class, mocked_combo, mocked_cache)

        # THEN: All the correct methods should have been called
        self.edit_song_form.manager.get_all_objects.assert_called_once_with(mocked_class, order_by_ref='Author')
        mocked_combo.clear.assert_called_once_with()
        mocked_combo.count.assert_called_once_with()
        mocked_combo.addItem.assert_called_once_with('Charles')
        mocked_cache.append.assert_called_once_with('Charles')
        mocked_combo.setItemData.assert_called_once_with(0, 1)
        mocked_set_case_insensitive_completer.assert_called_once_with(mocked_cache, mocked_combo)
        mocked_combo.setCurrentIndex.assert_called_once_with(-1)
        mocked_combo.setCurrentText.assert_called_once_with('')
