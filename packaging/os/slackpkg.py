#!/usr/bin/python

import sys
import shlex
import subprocess
import json

# (http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python)
#class bcolors:
#	HEADER = '\033[95m'
#	OKBLUE = '\033[94m'
#	OKGREEN = '\033[92m'
#	WARNING = '\033[93m'
#	FAIL = '\033[91m'
#	ENDC = '\033[0m'

slackpkg = "/usr/sbin/slackpkg"
slackpkgFlags = "-batch=on -default_answer=y -checksize=on"

# (http://docs.ansible.com/developing_modules.html#reading-input)
args_file = sys.argv[1]
args_data = file(args_file).read()
arguments = shlex.split(args_data)

## (https://docs.python.org/2.7/library/argparse.html)
#parser = argparse.ArgumentParser(description='This is a Python wrapper around Slackpkg')
#parser.add_argument('-a','--action', help='Action',required=True)
#args = parser.parse_args()

# (https://docs.python.org/2/library/subprocess.html)
(stdout, stderr) = subprocess.Popen(slackpkg + " " + slackpkgFlags + " " + arguments[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

print json.dumps({
	"action": arguments[0],
	"stdout": stdout,
	"stderr": stderr
})
