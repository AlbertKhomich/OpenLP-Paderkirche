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

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import translate
from openlp.core.lib.ui import create_button, create_button_box
from .slideparser import parse_structured_custom_text


class CustomSlideParserForm(QtWidgets.QDialog):
    """
    Dialog for parsing structured event text into custom slide markup.
    """
    def __init__(self, parent=None):
        super(CustomSlideParserForm, self).__init__(parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self._set_up_ui()

    def _set_up_ui(self):
        """
        Build the dialog UI.
        """
        self.setObjectName('custom_slide_parser_dialog')
        self.resize(520, 380)
        self.setWindowTitle(translate('CustomPlugin.CustomSlideParser', 'Parse Slide Text'))
        self.dialog_layout = QtWidgets.QVBoxLayout(self)
        self.description_label = QtWidgets.QLabel(self)
        self.description_label.setWordWrap(True)
        self.description_label.setText(
            translate('CustomPlugin.CustomSlideParser',
                      'Paste structured text here. Click Parse to convert it into the current slide text.')
        )
        self.dialog_layout.addWidget(self.description_label)
        self.source_text_edit = QtWidgets.QPlainTextEdit(self)
        self.source_text_edit.setObjectName('source_text_edit')
        self.dialog_layout.addWidget(self.source_text_edit)
        self.parse_button = create_button(
            self,
            'parse_button',
            text=translate('CustomPlugin.CustomSlideParser', 'Parse'),
            click=self.accept
        )
        self.button_box = create_button_box(self, 'button_box', ['cancel'], [self.parse_button])
        self.dialog_layout.addWidget(self.button_box)

    def get_parsed_text(self):
        """
        Return the parsed slide text for the entered source.
        """
        return parse_structured_custom_text(self.source_text_edit.toPlainText())
