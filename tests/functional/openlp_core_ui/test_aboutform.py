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
Package to test the openlp.core.ui.firsttimeform package.
"""
from unittest import TestCase

from openlp.core.ui.aboutform import AboutForm

from tests.functional import patch
from tests.helpers.testmixin import TestMixin


class TestAboutForm(TestCase, TestMixin):

    @patch('openlp.core.ui.aboutform.get_application_version')
    def test_create_about_form(self, mocked_get_application_version):
        """
        Test creating an about form
        """
        # GIVEN: An application version with a build number
        mocked_get_application_version.return_value = {'version': '3.1.1', 'build': '3000'}

        # WHEN: The about form is created
        about_form = AboutForm(None)

        # THEN: The correct version information should be in the dialog
        assert 'OpenLP 3.1.1 build 3000' in about_form.about_text_edit.toPlainText()

    @patch('openlp.core.ui.aboutform.webbrowser')
    def test_on_volunteer_button_clicked(self, mocked_webbrowser):
        """
        Test that clicking on the "Volunteer" button opens a web page.
        """
        # GIVEN: A new About dialog and a mocked out webbrowser module
        about_form = AboutForm(None)

        # WHEN: The "Volunteer" button is "clicked"
        about_form.on_volunteer_button_clicked()

        # THEN: A web browser is opened
        mocked_webbrowser.open_new.assert_called_with('http://openlp.org/en/contribute')

    def test_about_form_date_test(self):
        """
        Test that the copyright date is included correctly
        """
        # GIVEN: A correct application date
        # WHEN: The about form is created
        about_form = AboutForm(None)
        license_text = about_form.license_text_edit.toPlainText()

        # THEN: The date should be in the text twice.
        self.assertTrue(license_text.count('2017', 0) == 2,
                        "The text string should be added twice to the license string")
