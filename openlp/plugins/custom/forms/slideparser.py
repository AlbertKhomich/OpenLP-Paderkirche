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
Helpers for parsing structured event text into custom slide markup.
"""
import re


EVENT_LINE_RE = re.compile(
    r'^(?P<label>\d{1,2}\.\d{1,2}\.(?:\d{2,4}\.?)?(?:,\s*(?:ab\s+)?\d{1,2}:\d{2}\s*Uhr)?)\s+(?P<body>.+)$'
)
LOCATION_RE = re.compile(r'^(?P<title>.+?)\s*\((?P<location>[^()]*)\)\s*$')


def parse_structured_custom_text(text):
    """
    Convert structured event text into OpenLP custom slide markup.

    :param text: Raw text pasted by the user.
    :return: Parsed slide text.
    """
    blocks = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = EVENT_LINE_RE.match(line)
        if match:
            blocks.append(_format_event_block(match.group('label'), match.group('body')))
        else:
            blocks.append(_format_heading_block(line))
    return '\n\n'.join(blocks)


def _format_heading_block(text):
    """
    Format a heading-style block.
    """
    return '{st}{/st}\n{b}%s{/b}' % text


def _format_event_block(label, body):
    """
    Format an event block with optional location details.
    """
    title, location = _split_location(body)
    label_text = '%s:' % label if ',' in label else label
    body_text = '{b}%s{/b}' % title
    if location:
        body_text = '%s %s' % (body_text, location)
    return '{st}%s{/st}\n%s' % (label_text, body_text)


def _split_location(text):
    """
    Split a title from a trailing parenthesized location.
    """
    match = LOCATION_RE.match(text)
    if match:
        return match.group('title').strip(), match.group('location').strip()
    return text.strip(), ''
