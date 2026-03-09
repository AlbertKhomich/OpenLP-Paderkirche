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
This module contains tests for the manager submodule of the Bibles plugin.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from openlp.plugins.bibles.lib.manager import BibleManager


class TestManager(TestCase):
    """
    Test the functions in the :mod:`manager` module.
    """

    def setUp(self):
        app_location_patcher = patch('openlp.plugins.bibles.lib.manager.AppLocation')
        self.addCleanup(app_location_patcher.stop)
        app_location_patcher.start()
        log_patcher = patch('openlp.plugins.bibles.lib.manager.log')
        self.addCleanup(log_patcher.stop)
        self.mocked_log = log_patcher.start()
        settings_patcher = patch('openlp.plugins.bibles.lib.manager.Settings')
        self.addCleanup(settings_patcher.stop)
        settings_patcher.start()

    def test_delete_bible(self):
        """
        Test the BibleManager delete_bible method
        """
        # GIVEN: An instance of BibleManager and a mocked bible
        with patch.object(BibleManager, 'reload_bibles'), \
                patch('openlp.plugins.bibles.lib.manager.os.path.join', side_effect=lambda x, y: '{}/{}'.format(x, y)),\
                patch('openlp.plugins.bibles.lib.manager.delete_file', return_value=True) as mocked_delete_file:
            instance = BibleManager(MagicMock())
            # We need to keep a reference to the mock for close_all as it gets set to None later on!
            mocked_close_all = MagicMock()
            mocked_bible = MagicMock(file='KJV.sqlite', path='bibles', **{'session.close_all': mocked_close_all})
            instance.db_cache = {'KJV': mocked_bible}

            # WHEN: Calling delete_bible with 'KJV'
            result = instance.delete_bible('KJV')

            # THEN: The session should have been closed and set to None, the bible should be deleted, and the result of
            #       the deletion returned.
            self.assertTrue(result)
            mocked_close_all.assert_called_once_with()
            self.assertIsNone(mocked_bible.session)
            mocked_delete_file.assert_called_once_with('bibles/KJV.sqlite')
