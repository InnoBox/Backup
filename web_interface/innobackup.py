def _get_mountpoints():
	"""Get a list of all mountpoints that are potentially eligible to be backup drives"""
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

MAGIC_FILE='Innobox_Backup_Directory' #Determines whether a mountpoint is a backup point
def _is_backup(mp):
	"""Return True iff the specified mountpoint is a designated backup drive"""
	from os import access, F_OK
	from os.path import join
	return access(join(mp, MAGIC_FILE)) #True iff MAGIC_FILE exists

def _get_backup_drives():
	"""Returns all available backup drives as a list of absolute mountpoint paths."""
	mountpoints = _get_mountpoints()
	return filter(_is_backup, mountpoints)

def is_enabled():
	"""Return True iff there is at least one recognized backup drive."""
	return len(_get_backup_drives()) > 0

def is_extra_drive():
	"""Return True iff there are multiple redundant backup drives.  (This is currently
	considered an error condition.)"""
	return len(_get_backup_drives()) > 1

def get_drivename():
	drives = _get_backup_drives()
	if drives:
		return drives[0]
	else:
		return None

def _get_dates(backupdir):
	"""Return a list of all restorable dates in some rdiff-backup directory, in ctime()
	format.  The list is empty if there are no restorable dates (e.g. if the directory
	does not exist."""
	from subprocess import Popen
	#This command prints each available increment in order by increasing epoch time
	process = Popen(['rdiff-backup','--list-increments','--parsable-output',backupdir])
	output = process.communicate()[0]
	if process.returncode != 0:
		#Indicates failure, probably because the specified directory is not a valid
		#backup point.  Return an empty list of available restored points.
		return []
	epochs = [y.split()[0] for y in output.splitlines()]
	from time import ctime
	#Return a list of human-readable timestamps for the increments
	return [ctime(int(t)) for t in epochs]

from os.path import join
_backupdir = join(MAGIC_FILE,'Innobox_Wiki_Backup_v1.0')
def get_dates():
	return _get_dates(_backupdir)

#the backup command must be a systemwide executable under this name, taking a single argument:
#the backup directory.
_backup_command = "innobox_perform_backup"
def start_backup():
	"""Initiate the backup sequence, and return True iff backup has started correctly"""
	if get_backup_elapsed() is not None or get_restore_elapsed is not None:
		return False #failed to start because backup or restore is already running
	from subprocess import Popen
	Popen([_backup_command,_backupdir])
	return True #return without waiting for it to complete!

# The restore command must be a systemwide executable under this name, taking as arguments
# the backup directory and the desired restore date
_restore_command = "innobox_perform_restore"
def start_restore(date):
	"""Initiate restoration from the specified date, and return True iff the restore has
	started successfully.  This will only work if rdiff-backup supports timestamps
	as rendered by ctime() (and returned by get_dates()).  Needs testing."""
	if get_backup_elapsed() is not None or get_restore_elapsed is not None:
		return False #failed to start because backup or restore is already running
	#FIXME: Should ideally return False if the restore command is going to fail,
	#for example because the specified date is invalid.  I don't know how to tell that
	#that is the case at this time.
	from subprocess import Popen
	Popen([_restore_command,_backupdir,date])
	return True #return without waiting for it to complete!

def _get_elapsed(cmd):
	"""Return the elapsed time of a process with name cmd as a string, or None if the
	process is not running. """
	from subprocess import Popen
	#Get the elapsed time of any and all running instances of the specified command.
	x = subprocess.Popen(['ps','--no-headers','-C',cmd,'-o','etime']).communicate()[0]
	if x:
		#return the first line of output (the first elapsed-time) with
		#any whitespace stripped.  This may misbehave slightly if multiple instances
		#of the backup script are running simultaneously, but that should almost never be the case.
		return x.splitlines()[0].strip()
	else:
		return None

def get_backup_elapsed():
	"""Return the elapsed time of the running backup process as a human-readable string,
	or None if no backup process is running"""
	return _get_elapsed(_backup_command)

def get_restore_elapsed():
	"""Return the elapsed time of the running restore process as a human-readable string,
	or None if no restore process is running"""
	return _get_elapsed(_restore_command)
