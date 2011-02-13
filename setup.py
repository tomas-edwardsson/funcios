## setup.py ###
from distutils.core import setup
from distutils.command.install_data import install_data
from subprocess import Popen, PIPE
import sys
import os
import glob

NAME = "funcios"
VERSION = '0.1.1'
SHORT_DESC = "%s - Func Nagios Agent" % NAME
LONG_DESC = """
%s is a suite of plugins which monitor Linux hosts.
""" % NAME


class pre_install(install_data):
	"""
	Pre-install hook for creating man pages from .pod files
	"""
	def run(self):
		#from pprint import pprint
		#for self.data_files[0][1])
		# Call parent 

		for pod in pods:
			pod2man(pod)
		install_data.run(self)


def pod2man(file):
	"""
	Convert pod files to man pages
	"""

	try:
		fh = open("%s.1.gz" % file.replace('.pod', ''), 'wb')
	except Exception, e:
		print "Unable to open file for writing: %s" % e
		sys.exit(1)
	call_pod2man = Popen(['pod2man', '--center=%s' % file.replace('.pod', ''), '--release=""',
		file], stdout=PIPE)
	call_gzip = Popen(['gzip', '-9', '-c'], stdin=call_pod2man.stdout, stdout=fh)
	os.waitpid(call_gzip.pid, 0)
	fh.close()

if __name__ == "__main__":

	logpath		= "/var/log/%s/" % NAME
	varpath		= "/var/lib/%s/" % NAME
	rotpath		= "/etc/logrotate.d"
	manpath		= "share/man/man1/"
	etcpath = "/etc/%s" % NAME
	initpath	= "/etc/init.d/"

	pods = glob.glob("docs/*.pod")
	manpages = []
	for pod in pods:
		manpages.append(pod.replace('.pod', '.1.gz'))
	setup(
		name='%s' % NAME,
		version = VERSION,
		author='Tomas Edwardsson',
		description = SHORT_DESC,
		long_description = LONG_DESC,
		author_email='tommi@tommi.org',
		url='https://github.com/tomas-edwardsson/funcios',
		license='GPL',
		cmdclass={"install_data": pre_install},
		scripts = [
			'scripts/funcios-disks',
			'scripts/funcios-load',
			'scripts/funcios-cpu',
			'scripts/funcios-time',
		],
    	data_files = [(manpath, manpages
		)],
	
		packages = [
			'funcios',
		],
	)
