OpenLP
======

You're probably reading this because you've just downloaded the source code for
OpenLP. If you are looking for the installer file, please go to the download
page on the web site::

    http://openlp.org/download

If you're looking for how to contribute to OpenLP, then please look at the
OpenLP wiki::

    http://wiki.openlp.org/

Thanks for downloading OpenLP!

Local Customizations
====================

This checkout contains local workflow enhancements for Paderkirche.

Service Manager agenda builder
------------------------------

The Service Manager has an additional ``A`` button. It opens an agenda dialog
that accepts structured service text such as::

    10:30  0:04  Lied: - Befreit durch deine Gnade - Aktive Songs  D
    10:34  0:05  Begrüßung + Gebet
    10:39  0:04  Infos
    10:55  0:03  Textlesung: Markus 4,1-20

The agenda builder creates service items with these rules:

* ``Lied:`` lines add the first matching song from the songs database.
* Songs added this way receive the service theme ``PK Lieder Petrol Groß``.
* ``Begrüßung`` adds the first matching custom slide
  ``0 - Begrüßung (Paderkirche-Logo)``.
* ``Infos`` adds the first matching custom slide ``0 - Termine und Infos``.
* ``Textlesung:`` lines are normalized into Bible references such as
  ``Markus 4:1-20`` or ``Markus 2:23-3:6`` and added as Bible items.
* Bible items added this way receive the service theme ``PK Textlesung``.
* Unsupported entries such as ``Predigt`` or ``Abendmahl`` are ignored.
* ``Vater unser`` is always appended after the agenda entries if a matching
  custom slide exists.
* ``0 - Termine und Infos 2 Seite`` is appended after ``Vater unser`` if a
  matching custom slide exists. Its service slide text is filled from the
  current ISO week number: even weeks show ``Jungschar``/``Kleingruppen`` and
  odd weeks show ``Gebet``.

If multiple songs or custom slides share the same name, the first match is
used.

Custom slide text parser
------------------------

The custom slide edit window contains an additional ``Parse`` button. It opens
a dialog where structured announcement text can be pasted and converted into
formatted custom slide markup.

Example input::

    Kleingruppenwoche
    18.03., 19:00 Uhr OPEN DOORS Gebetsabend für verfolgte Christen (Kamp 43, PB)
    18.04., ab 09:00 Uhr "Create to Inspire" (Design- und Medienkonferenz in Schlangen)
    12.09. Bibelkunde Intensiv (Paderborn)
    Kooperation mit TSA Adelshofen

Example output::

    {st}{/st}
    {b}Kleingruppenwoche{/b}

    {st}18.03., 19:00 Uhr:{/st}
    {b}OPEN DOORS Gebetsabend für verfolgte Christen{/b} Kamp 43, PB

    {st}18.04., ab 09:00 Uhr:{/st}
    {b}"Create to Inspire"{/b} Design- und Medienkonferenz in Schlangen

    {st}12.09.{/st}
    {b}Bibelkunde Intensiv{/b} Paderborn

    {st}{/st}
    {b}Kooperation mit TSA Adelshofen{/b}
