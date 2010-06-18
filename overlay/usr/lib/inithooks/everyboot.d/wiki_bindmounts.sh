#!/bin/sh

# The purpose of this script is to ensure that all files that we want
# to be backed up for the wiki are available from inside
# /innobackup/mediawiki.  This allows both backup and restore to be
# applied only to this directory, rather than to the root.  This is important
# because rdiff-backup attempts to write temporary files to the root
# of the restore target, even if no files need to be written there.
# If the files to be restored are all over the system, then the restore
# target has to be /, and apache (the www-data user) doesn't have permission
# to write temporary files in /.  Thus, bind-mounting all wiki-related
# directories into one place is necessary in order for restore to run
# without root permissions.

HOLDING_DIR=/innobackup/mediawiki

# Don't need to chown /var/lib/mediawiki/images, since this is already
# necessarily writeable by www-data
mkdir -p $HOLDING_DIR/var/lib/mediawiki/images
chown -R www-data $HOLDING_DIR/var
mount --bind /var/lib/mediawiki/images/ $HOLDING_DIR/var/lib/mediawiki/images/
