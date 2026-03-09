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
Package to test the openlp.core.ui.shortcutdialog package.
"""
from unittest.mock import MagicMock

from PyQt5 import QtCore

from openlp.core.ui.shortcutlistdialog import CaptureShortcutButton, ShortcutTreeWidget


def test_key_press_event():
    """
    Test the keyPressEvent method
    """
    # GIVEN: A checked button and a mocked event
    button = CaptureShortcutButton()
    button.setChecked(True)
    mocked_event = MagicMock()
    mocked_event.key.return_value = QtCore.Qt.Key_Space

    # WHEN: keyPressEvent is called with an event that should be ignored
    button.keyPressEvent(mocked_event)

    # THEN: The ignore() method on the event should have been called
    mocked_event.ignore.assert_called_once_with()


def test_keyboard_search():
    """
    Test the keyboardSearch method of the ShortcutTreeWidget
    """
    # GIVEN: A ShortcutTreeWidget
    widget = ShortcutTreeWidget()

    # WHEN: keyboardSearch() is called
    widget.keyboardSearch('')

    # THEN: Nothing happens
    assert True
