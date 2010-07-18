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

class index:
	def GET(self):
		successtime, failtime, last_is_success = innobackup.get_date_claims()
		name = innobackup.get_drivename()
		extra_drive = innobackup.is_extra_drive()
		elapsed_backup = innobackup.get_backup_elapsed()
		elapsed_restore = innobackup.get_restore_elapsed()
		if elapsed_restore is None and elapsed_backup is None:
			dates = innobackup.get_dates()
		else:
			dates = None
		return render.backup_info(name, extra_drive, elapsed_backup, elapsed_restore, dates, successtime, failtime, last_is_success)

if __name__ == "__main__": app.run()

