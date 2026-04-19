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
Tests for agenda parsing helpers.
"""
import unittest
from unittest.mock import MagicMock

from openlp.core.lib.agendabuilder import (
    AgendaEntry,
    _get_song_search_titles,
    _song_title_matches,
    normalise_custom_title,
    parse_agenda_text
)


class TestAgendaBuilder(unittest.TestCase):
    """
    Test agenda parsing.
    """

    def test_parse_agenda_text_extracts_supported_entries(self):
        """
        Supported song, custom, and Bible lines should be parsed.
        """
        text = (
            '10:30\t0:04\tLied: - Befreit durch deine Gnade - Aktive Songs  D\n'
            '10:34\t0:05\tBegrüßung + Gebet\n'
            '10:39\t0:04\tInfos\n'
            '10:55\t0:03\tTextlesung: Markus 4,1-20\n'
            '10:58\t0:30\tPredigt: Markus 4,1-20\n'
        )

        entries, ignored = parse_agenda_text(text)

        self.assertEqual(4, len(entries))
        self.assertEqual(AgendaEntry.Song, entries[0].entry_type)
        self.assertEqual('Befreit durch deine Gnade', entries[0].value)
        self.assertEqual(AgendaEntry.Custom, entries[1].entry_type)
        self.assertEqual('Begrüßung (Paderkirche-Logo)', entries[1].value)
        self.assertEqual(AgendaEntry.Custom, entries[2].entry_type)
        self.assertEqual('Termine und Infos', entries[2].value)
        self.assertEqual(AgendaEntry.Bible, entries[3].entry_type)
        self.assertEqual('Markus 4:1-20', entries[3].value)
        self.assertEqual(['10:58\t0:30\tPredigt: Markus 4,1-20'], ignored)

    def test_parse_agenda_text_handles_lines_without_columns(self):
        """
        Standalone supported lines should still be parsed.
        """
        entries, ignored = parse_agenda_text('Infos\nAbendmahl\n')

        self.assertEqual(1, len(entries))
        self.assertEqual('Termine und Infos', entries[0].value)
        self.assertEqual(['Abendmahl'], ignored)

    def test_parse_agenda_text_normalises_cross_chapter_bible_ranges(self):
        """
        Cross-chapter Bible ranges should be rewritten with colons for both chapter/verse pairs.
        """
        entries, ignored = parse_agenda_text('Textlesung: Markus 2,23-3,6\n')

        self.assertEqual(1, len(entries))
        self.assertEqual(AgendaEntry.Bible, entries[0].entry_type)
        self.assertEqual('Markus 2:23-3:6', entries[0].value)
        self.assertEqual([], ignored)

    def test_parse_agenda_text_keeps_same_chapter_bible_lists(self):
        """
        Same-chapter Bible list separators should remain commas after the initial verse reference.
        """
        entries, ignored = parse_agenda_text('11:00\t0:03\tTextlesung: 1.Korinther 15:3-5,20-26,42-44,50-57\n')

        self.assertEqual(1, len(entries))
        self.assertEqual(AgendaEntry.Bible, entries[0].entry_type)
        self.assertEqual('1.Korinther 15:3-5,20-26,42-44,50-57', entries[0].value)
        self.assertEqual([], ignored)

    def test_get_song_search_titles_adds_collapsed_duplicate_fallback(self):
        """
        Repeated song titles should add a collapsed fallback search term.
        """
        entries, ignored = parse_agenda_text('Lied: Herr, wohin sonst - Herr, wohin sonst - Aktive Songs\n')

        self.assertEqual(1, len(entries))
        self.assertEqual(AgendaEntry.Song, entries[0].entry_type)
        self.assertEqual(
            ['Herr, wohin sonst - Herr, wohin sonst', 'Herr, wohin sonst'],
            _get_song_search_titles(entries[0].value)
        )
        self.assertEqual([], ignored)

    def test_song_title_matches_ignore_punctuation(self):
        """
        Song lookup should treat punctuation-only differences like the songs title search does.
        """
        self.assertTrue(
            _song_title_matches('Jesus, Herr, ich denke an dein Opfer', 'Jesus Herr ich denke an dein Opfer')
        )

    def test_normalise_custom_title_strips_numeric_prefix(self):
        """
        Custom slide title matching should ignore numeric prefixes like ``0 -``.
        """
        self.assertEqual(
            normalise_custom_title('Begrüßung (Paderkirche-Logo)'),
            normalise_custom_title('0 - Begrüßung (Paderkirche-Logo)')
        )

    def test_song_service_items_get_agenda_theme(self):
        """
        Song service items created by the agenda builder should get the configured agenda theme.
        """
        from openlp.core.lib.agendabuilder import AgendaBuilder

        builder = AgendaBuilder(MagicMock())
        builder._get_active_plugin = MagicMock()
        plugin = builder._get_active_plugin.return_value
        plugin.media_item.create_item_from_id.return_value = MagicMock()
        plugin.media_item.build_service_item.return_value = MagicMock(theme='Old Theme')
        builder._find_song = MagicMock(return_value=MagicMock(id=7))

        service_item = builder._build_song_service_item('Test Song')

        self.assertEqual('PK Lieder Petrol Groß', service_item.theme)

    def test_bible_service_items_get_agenda_theme(self):
        """
        Bible service items created by the agenda builder should get the configured agenda theme.
        """
        from openlp.core.lib.agendabuilder import AgendaBuilder

        builder = AgendaBuilder(MagicMock())
        builder._get_active_plugin = MagicMock()
        builder._get_default_bible = MagicMock(return_value='Offline Luther 2017')
        plugin = builder._get_active_plugin.return_value
        plugin.manager.get_bibles.return_value = {'Offline Luther 2017': object()}
        plugin.manager.get_verses.return_value = [MagicMock()]
        plugin.media_item.build_display_results.return_value = [MagicMock()]
        plugin.media_item.build_service_item.return_value = MagicMock(theme='Other Theme')

        service_item = builder._build_bible_service_item('Markus 4:1-20')

        self.assertEqual('PK Textlesung', service_item.theme)


if __name__ == '__main__':
    unittest.main()
