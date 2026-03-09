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
Package to test the openlp.plugins.songusage.forms.songusagedetailform package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import Registry
from openlp.plugins.songusage.forms.songusagedetailform import SongUsageDetailForm

from tests.helpers.testmixin import TestMixin


class TestSongUsageDetailForm(TestCase, TestMixin):
    """
    Test the SongUsageDetailForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        self.mocked_plugin = MagicMock()
        Registry().register('main_window', self.main_window)
        self.form = SongUsageDetailForm(self.mocked_plugin, self.main_window)

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    @patch('openlp.plugins.songusage.forms.songusagedetailform.Settings')
    def test_initalise_without_settings(self, MockedSettings):
        """
        Test the initialise() method when there are no settings
        """
        # GIVEN: A song usage detail form and a mocked settings object
        mocked_settings = MagicMock()
        mocked_settings.value.side_effect = ['', None, '']
        MockedSettings.return_value = mocked_settings

        # WHEN: initialise() is called
        self.form.initialise()

        # THEN: The dates on the calendar should be this month
        today = QtCore.QDate.currentDate()
        month_start = QtCore.QDate.currentDate().addDays(1 - today.day())
        assert self.form.from_date_calendar.selectedDate() == month_start, \
            self.form.from_date_calendar.selectedDate()
        assert self.form.to_date_calendar.selectedDate() == today, \
            self.form.to_date_calendar.selectedDate()

    @patch('openlp.plugins.songusage.forms.songusagedetailform.Settings')
    def test_initalise_with_settings(self, MockedSettings):
        """
        Test the initialise() method when there are existing settings
        """
        # GIVEN: A song usage detail form and a mocked settings object
        to_date = QtCore.QDate.currentDate().addDays(-1)
        from_date = QtCore.QDate.currentDate().addDays(2 - to_date.day())
        mocked_settings = MagicMock()
        mocked_settings.value.side_effect = [from_date, to_date, '']
        MockedSettings.return_value = mocked_settings

        # WHEN: initialise() is called
        self.form.initialise()

        # THEN: The dates on the calendar should be this month
        assert self.form.from_date_calendar.selectedDate() == from_date, \
            self.form.from_date_calendar.selectedDate()
        assert self.form.to_date_calendar.selectedDate() == to_date, \
            self.form.to_date_calendar.selectedDate()
