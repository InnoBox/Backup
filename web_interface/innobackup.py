def _get_mountpoints():
	f = open('/etc/mtab','r')
	mountpoints = []
	for line in f:
		# the mount point is the second whitespace-delimited substring
		# any whitespace characters in the mountpoint's name have
		# been escaped, so we need to unescape them
		mp = line.split(' ')[1].decode('string_escape')
		# all external media are mounted in /media/
		if mp[:7] == '/media/':
			mountpoints.append(mp)
	f.close()
	return mountpoints

MAGIC_FILE='Innobox_Backup_Directory'
def _is_backup(mp):
	from os import access, F_OK
	from os.path import join
	return access(join(mp, MAGIC_FILE))

def _get_backup_drives():
	mountpoints = _get_mountpoints()
	return filter(_is_backup, mountpoints)

def is_enabled():
	return True

def is_extra_drive():
	return True

def get_drivename():
	drives = _get_backup_drives()
	if drives:
		return drives[0]
	else:
		return None

def get_dates():
	return [str(i) for i in xrange(15)]

def start_backup():
	return False #always fails, of course

def start_restore(date):
	return False
