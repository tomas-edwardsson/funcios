#!/usr/bin/python

# Copyright 2011, Tomas Edwardsson <tommi@tommi.org>
#
# funcios-disks is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# funcios-disks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Design goals
#   handle multiple disks with optional variant levels
#   handle checks for single hosts
#   can check multiple hosts, but not for use within nagios, only running from cmd line
#   -w and -c set defaults, but thresholds can be defined per disk
#   -x exclude mountpoint
#   -X exclude devce
#   -F exclude filesystem type
#   -f include filesystem types


# Example:
#    funcios-disks -H host -d /:10%:2% -d /boot:20:5 -w 100 -c 10
#
# / warn at 10% crit 2%
# /boot warn at 20MB crit at 5MB
# Everything else warn at 100MB crit at 10MB


# Nagios plugin extensions
from pynag.Plugins import WARNING, CRITICAL, OK, UNKNOWN, simple as Plugin

# Func client
import func.overlord.client as fc
import func.CommonErrors

# Create the pynag.Plugin object
np = Plugin()

## Add command line arguments
# Device file
np.add_arg("d", "device-file", "Path to device to monitor", required=None)

# Filesystem path
np.add_arg("m", "mountpoint", "Path to mountpoint", required=None)

# Filesystem path
np.add_arg("L", "list-hosts", "List hosts", required=None)

# Filesystem path
np.add_arg("l", "list-disks", "List disks", required=None)

# Hosts (bah, I want this but it's built into pynag)
#np.add_arg("H", "hostname", "Hostname to check (wildcards allowed)", required=None)

# Plugin activation
np.activate()


#TODO WRITE conditions with thresholds and whatever...

# Set defaults
#crit = np['critical'] or '0'
crit = np['critical'] or '0'
warn = np['warning'] or '0'

threshold_type = 'mb'

if crit[:-1] == '%':
	threshold_type = 'percentage'

if warn[:-1] == '%' and threshold_type == 'percentage':
	nagios_exit("UNKNOWN", "Cannot mix percentage and MB for warning and critical")





# Probably not needed, removing when I'm older
all_minions = fc.Client('*').list_minions()

# No hostname specified, we default to all
host = np['host'] or '*'

# Try to setup func client object
try:
	client = fc.Client(host)
except func.CommonErrors.Func_Client_Exception as err:
	np.nagios_exit("UNKNOWN", err)

# Run disk usage
try:
	du = client.disk.usage()
except:
	pass

# Set the default return code
return_code = 0

for hostn in du:
	for mp in du[hostn]:
		np.add_perfdata(mp, du[hostn][mp]['percentage'], '%', warn.replace('%', ''), crit.replace('%', ''), '0', '100')

np.add_message(UNKNOWN, "ze unknown")
np.add_message("UNKNOWN", "ze warn")
(code, message) = np.check_messages(joinallstr = " ")
np.nagios_exit( code, message )

# vi: ts=4 :
