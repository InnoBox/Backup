#    Copyright 2010 InnoBox Devices <code@innoboxdevices.com>
#    This file is part of InnoBox Backup.
#
#    InnoBox Backup is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    InnoBox Backup is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details. 
#
#    You should have received a copy of the GNU Affero General Public License
#    along with InnoBox Backup.  If not, see <http://www.gnu.org/licenses/>.
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
		successtime, failtime, last_is_success = innobackup.get_date_claims()
		if innobackup.is_enabled():
			elapsed_backup = innobackup.get_backup_elapsed()
			elapsed_restore = innobackup.get_restore_elapsed()
			if elapsed_backup is not None or elapsed_restore is not None:
				return render.operation_inprogress(elapsed_backup, elapsed_restore)
			
			name = innobackup.get_drivename()
			dates = innobackup.get_dates()
			dates.insert(0,("","No date selected"))
			extra_drive = innobackup.is_extra_drive()

			return render.backup_on(name, extra_drive, restoreform(dates), successtime, failtime, last_is_success)
		else:
			return render.backup_off(successtime, failtime, last_is_success)
	def POST(self):
		headers = web.input()
		if 'backup' in headers:
			if innobackup.start_backup():
				return self.GET()
			else:
				return render.backup_failure()
		elif 'restore' in headers:
			if 'date' in headers and headers['date']:
				# Having inserted ("", "No date selected") into dates above,
				# we must only proceed with restore if a date has been selected
				datecode = headers['date']
				human_date = dict(innobackup.get_dates())[datecode]
				return render.confirm_restore(datecode,human_date)
			else:
				#if the user tries to perform a restore
				#without selecting a date, just reload the
				#page.
				return self.GET()
		elif 'confirmrestore' in headers:
			datecode = headers['confirmrestore']
			human_date = dict(innobackup.get_dates())[datecode]
			return render.really_restore(datecode,human_date)
		elif 'reallyrestore' in headers:
			if ('check1' in headers and
			   'check2' in headers and
			   'check3' in headers):
				#The user has checked all the boxes and passed both confirmation
				#pages, so now actually initiate the restore sequence.
				datecode = headers['reallyrestore']
				if innobackup.start_restore(datecode):
					return self.GET()
				else:
					return render.restore_failure()
			else:
				return self.GET()

if __name__ == "__main__": app.run()

