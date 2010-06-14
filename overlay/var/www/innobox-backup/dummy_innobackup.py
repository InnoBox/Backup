def is_enabled():
	return True

def is_extra_drive():
	return True

def get_drivename():
	return "The Backup Drive"

def get_dates():
	return [("square is " + str(i*i),str(i)) for i in xrange(15)]

def start_backup():
	return False #always fails, of course

def start_restore(date):
	return False

def get_elapsed_backup():
	return None

def get_elapsed_restore():
	return None
	from random import randint
	return "Eleventeen hours and %d minutes" % randint(0,60)
