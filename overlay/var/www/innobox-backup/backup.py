import web
from web import form
import innobackup

urls = (
	'/', 'index'
)

app = web.application(urls, globals())
application = app.wsgifunc() #the application variable is used by mod_wsgi

from os.path import abspath, dirname, join
rootdir = abspath(dirname(__file__))
render = web.template.render(join(rootdir,'templates/'))

def restoreform(dates):
	return form.Form(form.Dropdown('date', dates, description='Available Backup Dates'))()

class index:
	def GET(self):
		if innobackup.is_enabled():
			name = innobackup.get_drivename()
			dates = innobackup.get_dates()
			extra_drive = innobackup.is_extra_drive()
			elapsed_backup = innobackup.get_backup_elapsed()
			elapsed_restore = innobackup.get_restore_elapsed()

			return render.backup_on(name, extra_drive, elapsed_backup, elapsed_restore, restoreform(dates))
		else:
			return render.backup_off()
	def POST(self):
		headers = web.input()
		if 'backup' in headers:
			if innobackup.start_backup():
				return render.backup_success()
			else:
				return render.backup_failure()
		elif 'restore' in headers:
			if 'date' in headers:
				return render.confirm_restore(headers['date'])
			else:
				#if the user tries to perform a restore
				#without selecting a date, just reload the
				#page.
				return self.GET()
		elif 'reallyrestore' in headers:
			if innobackup.start_restore(headers['date']):
				return render.restore_success()
			else:
				return render.restore_failure()

if __name__ == "__main__": app.run()

