#!/usr/bin/python

import sys

# check for updates, reutrn False if none available, return output if updates are available:
def checkUpdates(slackpkgPath, slackpkgFlags):
	(stdout, stderr) = subprocess.Popen(slackpkgPath + ' ' + slackpkgFlags + ' check-updates', \
		shell=True, stdout=subprocess.PIPE).communicate()
	print stdout
	if 'No news is good news' in stdout:
		return False
	else:
		return (stdout)

# upgrade everything: update repositories, install new packages, upgrade existing packages, clean system
def upgradeAll(slackpkgPath, slackpkgFlags):
	print 'Upgrading everything'

def main():
	module = AnsibleModule(
		argument_spec = dict(
			action	= dict(required=True),
			package	= dict(required=False),
		),
	)

	action = module.params.get('action')
	package = module.params.get('package')

	# path to slackpkg script
	slackpkgPath = '/usr/sbin/slackpkg'
	# flags for slackpkg, batch=on and -default_answer=y are a must execution via Ansible
	slackpkgFlags = '-batch=on -default_answer=y -checksize=on'

	if action == 'check-updates':
		module.exit_json(changed=False, updates=checkUpdates(slackpkgPath, slackpkgFlags))

	if action == 'upgrade-all':
		module.exit_json(changed=True, output=upgradeAll())
# import module snippets
from ansible.module_utils.basic import *

main()
