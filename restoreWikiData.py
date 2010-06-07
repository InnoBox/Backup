#!/usr/bin/env python
import innobackup
HOLDING_DIR = '/innobackup/mediawiki/'
from os.path import join
DB_FILE = join(HOLDING_DIR,'wiki_db.sql')

def rdiff_restore(repository, date):
	cmd = ['rdiff-backup','--restore-as-of',str(date),repository,'/']
	from subprocess import Popen
	p = Popen(cmd)
	p.communicate()
	return p.returncode

def load_database(filename, password):
	cmd = 'mysql -uwiki_user -p%s wiki_db < %s' % (password,filename)
	from subprocess import Popen
	p = Popen(cmd, shell=True)
	p.communicate()
	return p.returncode

def get_password():
	f = open('/etc/mediawiki/wiki_password.txt')
	s = f.read()
	f.close()
	return s

backupdir = innobackup.get_backupdir()
from sys import argv
restoredate = argv[1]
rdiff_restore(backupdir,restoredate)
load_database(DB_FILE,get_password())
