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
Helpers for building service items from a pasted agenda.
"""
import logging
import re
import unicodedata
from datetime import date

from sqlalchemy.sql import func, or_

from openlp.core.common import Settings
from openlp.core.lib import ServiceItemContext


log = logging.getLogger(__name__)

AGENDA_LINE_RE = re.compile(r'^\s*(\d{1,2}:\d{2})\s+(\d{1,2}:\d{2})\s+(.*?)\s*$')
CUSTOM_TITLE_PREFIX_RE = re.compile(r'^\d+\s*-\s*')
BIBLE_BODY_RE = re.compile(r'^(?P<book>.+?)\s+(?P<body>\d.*)$')
BIBLE_DASH_CHARS = r'-\u00AD\u2010\u2011\u2012\u2014\u2015\u2212\uFE63\uFF0D'
BIBLE_INITIAL_CHAPTER_VERSE_RE = re.compile(r'^\s*(\d+),(\d+)')
BIBLE_CROSS_CHAPTER_VERSE_RE = re.compile(r'([%s])\s*(\d+),(\d+)(?=\s*(?:$|,))' % BIBLE_DASH_CHARS)


class AgendaEntry(object):
    """
    A parsed agenda line.
    """
    Song = 'song'
    Custom = 'custom'
    Bible = 'bible'

    def __init__(self, entry_type, value, raw_line):
        self.entry_type = entry_type
        self.value = value
        self.raw_line = raw_line


class AgendaBuildResult(object):
    """
    Collect the result of building an agenda.
    """
    def __init__(self):
        self.added = []
        self.skipped = []
        self.ignored = []


def parse_agenda_text(text):
    """
    Parse pasted agenda text into actionable entries.

    :param text: The raw agenda text.
    :return: A tuple containing actionable entries and ignored lines.
    """
    entries = []
    ignored = []
    for raw_line in text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line:
            continue
        description = _extract_description(stripped_line)
        if not description:
            continue
        entry = _parse_description(description, stripped_line)
        if entry is None:
            ignored.append(stripped_line)
        else:
            entries.append(entry)
    return entries, ignored


def _extract_description(line):
    """
    Extract the agenda description column from a pasted line.
    """
    parts = [part.strip() for part in line.split('\t') if part.strip()]
    if len(parts) >= 3:
        return _normalise_text(parts[2])
    match = AGENDA_LINE_RE.match(line)
    if match:
        return _normalise_text(match.group(3))
    return _normalise_text(line)


def _parse_description(description, raw_line):
    """
    Convert a description line into an actionable entry.
    """
    description = _normalise_text(description)
    lowered = description.casefold()
    if lowered.startswith('lied:'.casefold()):
        title = _extract_song_title(description)
        if title:
            return AgendaEntry(AgendaEntry.Song, title, raw_line)
        return None
    if lowered.startswith('textlesung'.casefold()):
        reference = _normalise_bible_reference(_extract_colon_value(description))
        if reference:
            return AgendaEntry(AgendaEntry.Bible, reference, raw_line)
        return None
    if lowered.startswith('begrüßung'.casefold()):
        return AgendaEntry(AgendaEntry.Custom, 'Begrüßung (Paderkirche-Logo)', raw_line)
    if lowered.startswith('infos'.casefold()):
        return AgendaEntry(AgendaEntry.Custom, 'Termine und Infos', raw_line)
    return None


def _extract_song_title(description):
    """
    Extract a song title from an agenda line.
    """
    title = _extract_colon_value(description)
    if title.startswith('-'):
        title = title[1:].strip()
    for separator in [' - Aktive Songs', ' Aktive Songs']:
        if separator in title:
            title = title.split(separator, 1)[0].strip()
            break
    return _normalise_text(title.strip(' -\t'))


def _collapse_repeated_song_title(title):
    """
    Collapse duplicated song titles like ``A - A`` or ``A - B - A - B``.
    """
    parts = [part.strip() for part in title.split(' - ')]
    if len(parts) < 2 or len(parts) % 2 != 0:
        return title
    midpoint = len(parts) // 2
    first_half = [_normalise_text(part).casefold() for part in parts[:midpoint]]
    second_half = [_normalise_text(part).casefold() for part in parts[midpoint:]]
    if first_half == second_half:
        return ' - '.join(parts[:midpoint]).strip()
    return title


def _get_song_search_titles(title):
    """
    Return song title candidates, preferring exact matches before de-duplicated fallbacks.
    """
    title = _normalise_text(title)
    search_titles = [title]
    collapsed_title = _collapse_repeated_song_title(title)
    if collapsed_title and collapsed_title.casefold() != title.casefold():
        search_titles.append(_normalise_text(collapsed_title))
    return search_titles


def _extract_colon_value(text):
    """
    Return the text behind the first colon.
    """
    if ':' in text:
        return _normalise_text(text.split(':', 1)[1])
    return ''


def _normalise_text(text):
    """
    Normalise user input so pasted umlauts match DB titles consistently.
    """
    return unicodedata.normalize('NFC', text.strip())


def _normalise_song_search_title(title):
    """
    Normalise a song title using the Songs plugin search rules.
    """
    from openlp.plugins.songs.lib import clean_string

    return clean_string(_normalise_text(title))


def _song_title_matches(song_title, title, search_title=None):
    """
    Match song titles exactly, while ignoring punctuation differences used by song search.
    """
    if not song_title:
        return False
    song_title = _normalise_text(song_title)
    title = _normalise_text(title)
    if song_title.casefold() == title.casefold():
        return True
    if search_title is None:
        search_title = _normalise_song_search_title(title)
    return _normalise_song_search_title(song_title) == search_title


def normalise_custom_title(text):
    """
    Normalise custom slide titles and ignore leading numeric prefixes like ``0 -``.
    """
    return CUSTOM_TITLE_PREFIX_RE.sub('', _normalise_text(text)).casefold()


def _normalise_bible_reference(reference):
    """
    Rewrite chapter/verse commas to a colon for the OpenLP Bible parser.
    """
    reference = _normalise_text(reference)
    match = BIBLE_BODY_RE.match(reference)
    if match:
        book = match.group('book')
        body = match.group('body')
    else:
        book = ''
        body = reference
    body = BIBLE_INITIAL_CHAPTER_VERSE_RE.sub(r'\1:\2', body)
    # Keep list separators like ``15:3-5,20-26`` intact while still normalising ``2,23-3,6``.
    body = BIBLE_CROSS_CHAPTER_VERSE_RE.sub(r'\1\2:\3', body)
    if book:
        return '%s %s' % (book, body)
    return body


class AgendaBuilder(object):
    """
    Build service items from parsed agenda entries.
    """
    bible_theme = 'PK Textlesung'
    song_theme = 'PK Lieder Petrol Groß'
    final_custom_slide_title = 'Vater unser'
    weekly_info_custom_slide_title = 'Termine und Infos 2 Seite'

    def __init__(self, service_manager):
        self.service_manager = service_manager
        self.plugin_manager = service_manager.plugin_manager

    def build(self, text):
        """
        Build and add agenda items to the current service.

        :param text: The raw agenda text entered by the user.
        :return: An AgendaBuildResult instance.
        """
        result = AgendaBuildResult()
        entries, ignored = parse_agenda_text(text)
        result.ignored.extend(ignored)
        if not entries:
            return result
        self.service_manager.application.set_busy_cursor()
        try:
            service_items = []
            for entry in entries:
                service_item = self._build_service_item(entry, result)
                if service_item:
                    service_items.append(service_item)
                    result.added.append(entry.value)
            final_item = self._build_custom_service_item(self.final_custom_slide_title)
            if final_item:
                service_items.append(final_item)
                result.added.append(self.final_custom_slide_title)
            else:
                result.skipped.append('Custom slide not found: %s' % self.final_custom_slide_title)
            weekly_info_item = self._build_weekly_info_service_item()
            if weekly_info_item:
                service_items.append(weekly_info_item)
                result.added.append(self.weekly_info_custom_slide_title)
            else:
                result.skipped.append('Custom slide not found: %s' % self.weekly_info_custom_slide_title)
            for index, service_item in enumerate(service_items):
                self.service_manager.add_service_item(service_item, repaint=index == len(service_items) - 1)
        finally:
            self.service_manager.application.set_normal_cursor()
        return result

    def _build_service_item(self, entry, result):
        """
        Resolve an agenda entry to a service item.
        """
        if entry.entry_type == AgendaEntry.Song:
            service_item = self._build_song_service_item(entry.value)
            if not service_item:
                result.skipped.append('Song not found: %s' % entry.value)
            return service_item
        if entry.entry_type == AgendaEntry.Custom:
            service_item = self._build_custom_service_item(entry.value)
            if not service_item:
                result.skipped.append('Custom slide not found: %s' % entry.value)
            return service_item
        if entry.entry_type == AgendaEntry.Bible:
            service_item = self._build_bible_service_item(entry.value)
            if not service_item:
                result.skipped.append('Bible passage not found: %s' % entry.value)
            return service_item
        return None

    def _build_song_service_item(self, title):
        """
        Build a service item for a song title.
        """
        plugin = self._get_active_plugin('songs')
        if plugin is None:
            return None
        song = self._find_song(plugin, title)
        if song is None:
            return None
        item = plugin.media_item.create_item_from_id(song.id)
        service_item = plugin.media_item.build_service_item(item, context=ServiceItemContext.Service)
        if service_item:
            service_item.theme = self.song_theme
        return service_item

    def _build_custom_service_item(self, title):
        """
        Build a service item for a custom slide title.
        """
        plugin = self._get_active_plugin('custom')
        if plugin is None:
            return None
        custom_slide = self._find_custom_slide(plugin, title)
        if custom_slide is None:
            return None
        item = plugin.media_item.create_item_from_id(custom_slide.id)
        return plugin.media_item.build_service_item(item, context=ServiceItemContext.Service)

    def _build_weekly_info_service_item(self):
        """
        Build the weekly second info slide and fill it for the current calendar week.
        """
        service_item = self._build_custom_service_item(self.weekly_info_custom_slide_title)
        if not service_item:
            return None
        weekly_info_text = get_weekly_info_slide_text()
        service_item._raw_frames = []
        service_item.add_from_text(weekly_info_text)
        return service_item

    def _build_bible_service_item(self, reference):
        """
        Build a service item for a Bible reference using the configured quick Bible.
        """
        plugin = self._get_active_plugin('bibles')
        if plugin is None:
            return None
        bible = self._get_default_bible(plugin)
        if not bible:
            return None
        search_results = plugin.manager.get_verses(bible, reference, False, show_error=False)
        if not search_results:
            return None
        items = plugin.media_item.build_display_results(bible, '', search_results)
        service_item = plugin.media_item.build_service_item(items, context=ServiceItemContext.Service)
        if service_item:
            service_item.theme = self.bible_theme
        return service_item

    def _get_active_plugin(self, name):
        """
        Return an active plugin by name.
        """
        plugin = self.plugin_manager.get_plugin_by_name(name)
        if plugin and plugin.is_active():
            return plugin
        log.warning('Agenda builder could not use inactive plugin "%s".', name)
        return None

    @staticmethod
    def _find_song(plugin, title):
        """
        Find the first matching song by title.
        """
        from openlp.plugins.songs.lib.db import Song

        for search_title_value in _get_song_search_titles(title):
            lower_title = search_title_value.lower()
            search_title = _normalise_song_search_title(search_title_value)
            songs = plugin.manager.get_all_objects(
                Song,
                or_(
                    Song.search_title.like(search_title + '@%'),
                    Song.search_title.like('%@' + search_title),
                    func.lower(Song.title) == lower_title,
                    func.lower(Song.alternate_title) == lower_title
                ),
                order_by_ref=Song.id
            )
            for song in songs:
                if _song_title_matches(song.title, search_title_value, search_title):
                    return song
                if _song_title_matches(song.alternate_title, search_title_value, search_title):
                    return song
            if songs:
                return songs[0]
        return None

    @staticmethod
    def _find_custom_slide(plugin, title):
        """
        Find the first matching custom slide by title.
        """
        title = _normalise_text(title)
        from openlp.plugins.custom.lib.db import CustomSlide

        exact_title = title.casefold()
        normalised_title = normalise_custom_title(title)
        custom_slides = plugin.db_manager.get_all_objects(
            CustomSlide,
            order_by_ref=CustomSlide.id
        )
        for custom_slide in custom_slides:
            if _normalise_text(custom_slide.title).casefold() == exact_title:
                return custom_slide
        for custom_slide in custom_slides:
            if normalise_custom_title(custom_slide.title) == normalised_title:
                return custom_slide
        return None

    @staticmethod
    def _get_default_bible(plugin):
        """
        Return the configured quick Bible or the first available Bible.
        """
        bibles = plugin.manager.get_bibles()
        if not bibles:
            return ''
        bible = Settings().value('bibles/quick bible')
        if bible in bibles:
            return bible
        return sorted([b for b in bibles.keys() if b])[0]


def get_weekly_info_slide_text(today=None):
    """
    Return the info slide text for the current ISO week number.
    """
    if today is None:
        today = date.today()
    week_number = today.isocalendar()[1]
    if week_number % 2 == 0:
        return (
            '{st}So., 10:30 Uhr:{/st}\n'
            '{b}Gottesdienst{/b} im Deelenhaus, Krämerstraße 8-10\n'
            '\n'
            '{st}Mi., 18:30 Uhr:{/st}\n'
            '{b}Jungschar{/b} \n'
            '\n'
            '{b}Kleingruppen{/b} '
        )
    return (
        '{st}So., 10:30 Uhr:{/st}\n'
        '{b}Gottesdienst{/b} im Deelenhaus, Krämerstraße 8-10\n'
        '\n'
        '{st}Mi., 19:30 Uhr:{/st}\n'
        '{b}Gebet{/b} am Kamp 43'
    )
