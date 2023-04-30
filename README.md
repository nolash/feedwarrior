# NAME

feedwarrior - Feeds, warrior style

# DESCRIPTION

Inspired by [](https//taskwarrior.org), this project seeks to simplify
the creation and maintenance of engineering work logs.

Entries of each individual log has core text content. Additionally,
every entry may have any number of file attachments associated with it.

# SYNOPSIS

**feedwarrior** add \[ -c config_file\] \[ -z \] \[ \--task-id \] \[
\--task-uuid \] \< -s subject \>

**feedwarrior** attach \[ -c config_file\] \[ -z \] \< -e entry \> file

**feedwarrior** create \[ -c config_file\] \[ \--alias name \]

**feedwarrior** entry \[ -c config_file\] \[ -z \] \[ \--task-id \] \[
\--task-uuid \] \< -s subject \> \< path_to_content \>

**feedwarrior** list \[ -c config_file\]

**feedwarrior** show \[ -c config_file\] \< -l feed_id \>

## Common options

**-l***log_id*

:   Log id to operate on. May be the full uuid or the alias defined at
    creation time.

**-c***config_file*

:   Load configuration from file.

## Options for show

**\--headers**

:   Include multipart-headers in output.

## Options for attach

**-e***entry_id*

:   uuid of entry to attach file to.

## Options for create

**\--alias***alias_id*

:   Create log id alias that may be used as argument to **-l** for
    future operations.

## Options for add and entry

**-s***subject*

:   Entry subject.

**\--task-id***id*

:   Associate the log entry with the given taskwarrior numeric id. This
    is a quasi-magical instruction which will resolve to the actual
    taskwarrior uuid.

**\--task-uuid***uuid*

:   Associate the log entry with the given taskwarrior numeric uuid.

# ATTACHMENTS

Both **feedwarrior add** and **feedwarrior entry** will return the
created entry id.

This id can be used further with the **-e** flag for attachments.

Any file in any format may be an attachment. The feedwarrior tool
imposes little if no restriction on what data qualifies as valid
attachment data.

# INTERACTIVE ENTRIES

The **feedwarrior add** command enables interactive definition of
textual update entry contents.

It will open an editor (at the moment hardcoded to **vim**) to receive
the contents.

# DATA STORE

Log entries are stored as email-like MIME Multipart messages, wrapped in
a json metadata structure.

Only the default, simple filesystem structure is currently available as
storage backend.

# EXAMPLE

    # create feed
    feedwarrior create --alias myfeed

    ¤ add log entry
    ENTRY=`feedwarrior -l myfeed entry -s "first update" /path/to/contents.txt

    # attach file to entry
    feedwarrior attach -e $ENTRY <attachment_file>

    ¤ interactively add log entry contents
    entry=`feedwarrior -l myfeed add -s "second update" 

    # show current state of feed (chronologically)
    feedwarrior -l myfeed show

# LICENSE

This documentation and its source is licensed under the Creative Commons
Attribution-Sharealike 4.0 International license.

The source code of the tool this documentation describes is licensed
under the GNU General Public License 3.0.

# COPYRIGHT AND CONTACT

[Louis Holbrook](mailto:dev@holbrook.no)

[](https://holbrook.no)https://holbrook.no

PGP: 59A844A484AC11253D3A3E9DCDCBD24DD1D0E001

# SOURCE CODE

https://holbrook.no/src/feedwarrior/log.html


# ABOUT THIS DOCUMENT

This document was generated using `pandoc -f man -t markdown ...`
