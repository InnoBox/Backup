def is_enabled():
	return True

def is_extra_drive():
	return True

def get_drivename():
	return "The Backup Drive"

def get_dates():
	return [str(i) for i in xrange(15)]

def start_backup():
	return False #always fails, of course

def start_restore(date):
	return False
