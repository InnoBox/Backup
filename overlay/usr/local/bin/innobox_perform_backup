#!/usr/bin/env python
import innobackup

MIN_FREEFRAC = 0.5 # Minimum 50% free

def get_freefrac(path):
	from os import statvfs
	s = os.statvfs(path)
	return float(s.f_bavail)/s.f_blocks

def remove_oldest_increment(path):
	dates = innobackup.get_dates()
	oldest_epoch = min([int(x[0]) for x in dates])
	from subprocess import Popen
	p = Popen(['rdiff-backup','--remove-older-than',str(oldest_epoch+1)])
	p.communicate()
	return p.returncode

def make_room(path):
	error_detected = False
	while get_freefrac(path) < MIN_FREEFRAC and not error_detected:
		r = remove_oldest_increment(path)
		if r != 0:
			error_detected = True
	return error_detected

def dump_database(path):
	from tempfile import mkdtemp
	d = mkdtemp()
	from os.path import join
	dbfilename = os.path.join(d,"wiki_db.sql")
	f = open('/etc/mediawiki/wiki_password.txt')
	wiki_password = f.read()
	f.close()
	cmd = "/usr/bin/nice -n 19 mysqldump -uwiki_user -p%s wiki_db -c > %s" % (wiki_password, dbfilename)
	from subprocess import Popen
	p = Popen(cmd,shell=True)
	p.communicate() #wait for the process to finish
	from shutil import move
	move(dbfilename,path)

def rdiff_backup(target):
	sources = '/usr/share/innobackup/wiki_backup_list'
	cmd = ['rdiff-backup','--include-filelist',sources,target]
	from subprocess import Popen
	p = Popen(cmd)
	p.communicate() #wait for backup to finish
	return p.returncode	

HOLDING_PATH='/innobackup/mediawiki/'

dump_database(HOLDING_PATH)
backupdir = innobackup.get_backupdir()
make_room(backupdir)
rdiff_backup(backupdir)
