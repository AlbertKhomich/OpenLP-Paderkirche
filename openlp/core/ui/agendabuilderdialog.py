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
Dialog for creating a service agenda from pasted text.
"""
from PyQt5 import QtWidgets

from openlp.core.common import translate
from openlp.core.lib.agendabuilder import AgendaBuilder
from openlp.core.lib.ui import create_button, create_button_box


class AgendaBuilderDialog(QtWidgets.QDialog):
    """
    Let the user paste agenda text and build service items from it.
    """
    def __init__(self, service_manager, parent=None):
        super(AgendaBuilderDialog, self).__init__(parent or service_manager)
        self.service_manager = service_manager
        self.builder = AgendaBuilder(service_manager)
        self._set_up_ui()

    def _set_up_ui(self):
        """
        Set up the dialog.
        """
        self.setWindowTitle(translate('OpenLP.AgendaBuilder', 'Agenda Builder'))
        self.resize(720, 480)
        layout = QtWidgets.QVBoxLayout(self)
        self.description_label = QtWidgets.QLabel(self)
        self.description_label.setWordWrap(True)
        self.description_label.setText(
            translate('OpenLP.AgendaBuilder',
                      'Paste an agenda with start time, duration, and description. '
                      'Supported entries: songs ("Lied"), "Begrüßung", "Infos", and "Textlesung".')
        )
        layout.addWidget(self.description_label)
        self.input_text_edit = QtWidgets.QPlainTextEdit(self)
        self.input_text_edit.setObjectName('agenda_input_text_edit')
        layout.addWidget(self.input_text_edit)
        self.create_button = create_button(
            self,
            'create_agenda_button',
            text=translate('OpenLP.AgendaBuilder', 'Create agenda'),
            click=self.on_create_agenda
        )
        self.button_box = create_button_box(self, 'agenda_button_box', ['close'], [self.create_button])
        layout.addWidget(self.button_box)

    def on_create_agenda(self):
        """
        Build agenda items from the pasted text and append them to the current service.
        """
        text = self.input_text_edit.toPlainText().strip()
        if not text:
            QtWidgets.QMessageBox.information(
                self,
                translate('OpenLP.AgendaBuilder', 'Agenda Builder'),
                translate('OpenLP.AgendaBuilder', 'Please paste an agenda first.')
            )
            return
        result = self.builder.build(text)
        if result.added:
            parts = [
                translate('OpenLP.AgendaBuilder', '%d item(s) were added to the service.') % len(result.added)
            ]
            if result.skipped:
                parts.append(
                    translate('OpenLP.AgendaBuilder', 'Skipped:\n- %s') % '\n- '.join(result.skipped)
                )
            if result.ignored:
                parts.append(
                    translate('OpenLP.AgendaBuilder', 'Ignored unsupported line(s): %d') % len(result.ignored)
                )
            QtWidgets.QMessageBox.information(
                self,
                translate('OpenLP.AgendaBuilder', 'Agenda Created'),
                '\n\n'.join(parts)
            )
        else:
            parts = [translate('OpenLP.AgendaBuilder', 'No agenda items were created.')]
            if result.skipped:
                parts.append(translate('OpenLP.AgendaBuilder', 'Skipped:\n- %s') % '\n- '.join(result.skipped))
            if result.ignored:
                parts.append(
                    translate('OpenLP.AgendaBuilder', 'Ignored unsupported line(s): %d') % len(result.ignored)
                )
            QtWidgets.QMessageBox.information(
                self,
                translate('OpenLP.AgendaBuilder', 'Agenda Builder'),
                '\n\n'.join(parts)
            )
