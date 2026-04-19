# -*- coding: utf-8 -*-

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
Tests for structured custom slide parsing.
"""
from unittest import TestCase

from openlp.plugins.custom.forms.slideparser import parse_structured_custom_text


class TestSlideParser(TestCase):
    """
    Test structured custom slide parsing.
    """

    def test_parse_structured_custom_text_formats_sample(self):
        """
        The structured text should be converted into the expected custom slide markup.
        """
        source_text = (
            'Kleingruppenwoche\n'
            '18.03., 19:00 Uhr OPEN DOORS Gebetsabend für verfolgte Christen (Kamp 43, PB)\n'
            '18.04., ab 09:00 Uhr "Create to Inspire" (Design- und Medienkonferenz in Schlangen)\n'
            '12.09. Bibelkunde Intensiv (Paderborn)\n'
            'Kooperation mit TSA Adelshofen\n'
        )
        expected = (
            '{st}{/st}\n'
            '{b}Kleingruppenwoche{/b}\n\n'
            '{st}18.03., 19:00 Uhr:{/st}\n'
            '{b}OPEN DOORS Gebetsabend für verfolgte Christen{/b} Kamp 43, PB\n\n'
            '{st}18.04., ab 09:00 Uhr:{/st}\n'
            '{b}"Create to Inspire"{/b} Design- und Medienkonferenz in Schlangen\n\n'
            '{st}12.09.{/st}\n'
            '{b}Bibelkunde Intensiv{/b} Paderborn\n\n'
            '{st}{/st}\n'
            '{b}Kooperation mit TSA Adelshofen{/b}'
        )

        assert expected == parse_structured_custom_text(source_text)

    def test_parse_structured_custom_text_keeps_year_in_date_label(self):
        """
        Dates with a year should be parsed and keep the year in the output label.
        """
        source_text = (
            '04.04.25 OPEN DOORS Gebetsabend für verfolgte Christen (Kamp 43, PB)\n'
            '04.04.25, 19:00 Uhr Bibelkunde Intensiv (Paderborn)\n'
        )
        expected = (
            '{st}04.04.25{/st}\n'
            '{b}OPEN DOORS Gebetsabend für verfolgte Christen{/b} Kamp 43, PB\n\n'
            '{st}04.04.25, 19:00 Uhr:{/st}\n'
            '{b}Bibelkunde Intensiv{/b} Paderborn'
        )

        assert expected == parse_structured_custom_text(source_text)

    def test_parse_structured_custom_text_formats_date_with_time(self):
        """
        Dates in day.month., time format should be parsed into a slide title block.
        """
        source_text = '07.03., 10:30 Uhr Gottesdienst (Paderborn)\n'
        expected = (
            '{st}07.03., 10:30 Uhr:{/st}\n'
            '{b}Gottesdienst{/b} Paderborn'
        )

        assert expected == parse_structured_custom_text(source_text)

    def test_parse_structured_custom_text_formats_weekday_events_without_dates(self):
        """
        Weekday-based events without a calendar date should still be parsed as event blocks.
        """
        source_text = (
            'Kleingruppen\n'
            'So., 10:30 Uhr (Deelenhaus, Krämerstraße 8-10)\n'
            'Mt., 19:30 Uhr Gebet (am Kamp 43)\n'
            'Mi., 18:30 Uhr Jungschar ?\n'
        )
        expected = (
            '{st}{/st}\n'
            '{b}Kleingruppen{/b}\n\n'
            '{st}So., 10:30 Uhr:{/st}\n'
            'Deelenhaus, Krämerstraße 8-10\n\n'
            '{st}Mt., 19:30 Uhr:{/st}\n'
            '{b}Gebet{/b} am Kamp 43\n\n'
            '{st}Mi., 18:30 Uhr:{/st}\n'
            '{b}Jungschar ?{/b}'
        )

        assert expected == parse_structured_custom_text(source_text)

    def test_parse_structured_custom_text_formats_weekday_date_labels(self):
        """
        Weekday labels should support an added date, with or without a time.
        """
        source_text = (
            'So., 10.04. 10:30 Uhr Gottesdienst (Paderborn)\n'
            'So., 10.04.26 10:30 Uhr Taufgottesdienst (Deelenhaus)\n'
            'So., 10.04. Bibelstunde (Kamp 43)\n'
            'So., 10.04.26 Jugendabend\n'
        )
        expected = (
            '{st}So., 10.04. 10:30 Uhr:{/st}\n'
            '{b}Gottesdienst{/b} Paderborn\n\n'
            '{st}So., 10.04.26 10:30 Uhr:{/st}\n'
            '{b}Taufgottesdienst{/b} Deelenhaus\n\n'
            '{st}So., 10.04.{/st}\n'
            '{b}Bibelstunde{/b} Kamp 43\n\n'
            '{st}So., 10.04.26{/st}\n'
            '{b}Jugendabend{/b}'
        )

        assert expected == parse_structured_custom_text(source_text)
