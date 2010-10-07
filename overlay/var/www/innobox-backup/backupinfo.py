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

