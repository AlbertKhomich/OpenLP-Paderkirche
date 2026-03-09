# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4
# pylint: disable=invalid-name

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
Package to test the openlp.core.ui.general package.
"""
from unittest import TestCase

from openlp.core.ui.generaltab import GeneralTab

from tests.functional import MagicMock, patch


class TestGeneralTab(TestCase):
    """
    Test the General tab
    """

    @patch('openlp.core.ui.generaltab.translate')
    @patch('openlp.core.ui.generaltab.ScreenList')
    def create_general_tab_test(self, MockedScreenList, mocked_translate):
        """
        Test that the General tab has the correct settings when created
        """
        # GIVEN: A GeneralTab class and a mocked out ScreenList
        mocked_screen_list = MagicMock()
        MockedScreenList.return_value = mocked_screen_list
        mocked_translate.side_effect = lambda x, y: y

        # WHEN: An instance of the class is created
        general_tab = GeneralTab(None)

        # THEN: Various member variables should be initialised
        self.assertEqual(mocked_screen_list, general_tab.screens)
        self.assertEqual(':/icon/openlp-logo-16x16.png', general_tab.icon_path)
