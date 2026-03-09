OpenLP 2.4.6
============

* Fix a bug where the author type upgrade was being ignore because it was looking at the wrong table
* Fix a bug where the songs_songbooks table was not being created because the if expression was the wrong way round
* Change the songs_songbooks migration SQL slightly to take into account a bug that has (hopefully) been fixed
* Sometimes the timer goes off as OpenLP is shutting down, and the application has already been deleted (reported via support system)
* Fix opening the data folder (KDE thought the old way was an SMB share)
* Fix a problem with the new QMediaPlayer not controlling the playlist anymore
* Add importing of author types to the OpenLP 2 song importer
* Fix a problem with loading Qt's translation files, bug #1676163
* Disable the controls in the shortcut dialog unless a shortcut is actually selected
