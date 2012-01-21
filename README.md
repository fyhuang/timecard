Timecard program
================

This is a simple Python script to keep track of time for you. It was originaly intended to be used for logging work hours (hence the name `timecard`).

It only keeps track of the total # of hours you worked, not the specific time of day. It supports multiple timecards, simple incrementing/decrementing, and also a "stopwatch" feature. When you use the "stopwatch", the time recorded is rounded to the nearest quarter-hour (15 minutes) by default.

Requires **Python 3.x**.

Usage
=====

`timecard.py` takes one argument, the filename of the database to use. If no filename is provided, the default DB used is `~/.timecarddb`. It provides a prompt-based interface. All operations operate on the current timecard (of which there can be multiple); use `newcard` to make a new card, `use` to change the current card, and `ls` to see a list of all the cards.

All the other operations should be self-explanatory. Use `help` to view a list of commands.
