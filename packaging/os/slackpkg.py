#!/usr/bin/env python
DOCUMENTATION = '''
---
module: slackpkg
version_added: 
short_description: Engage's slackpkg, Slackware's package manager
extends_documentation_fragment: files
description:
  - The Engage's slackpkg, Slackware's package manager
options:
  action:
    description:
      - Which action should the module take, or otherwise pass directly to slackpkg
    required: true
    default: null
  package:
    description:
      - If operating on an individual package, pass its name
    required: false
    default: null
author: Ernest Kugel
'''

EXAMPLES = '''
# Check for updates:
- slackpkg: action=check-updates
# Update NTP:
- slackpkg: action=upgrade package=ntp
'''

import sys

# run *anything* slackpkg supports by taking a slackpkg action and a package name (can be left blank)
def slackpkgAux(slackpkgAction, slackpkgPackage):
	(stdout, stderr) = subprocess.Popen(slackpkgPath + ' ' \
		+ slackpkgFlags + ' ' \
		+ slackpkgAction + ' ' \
		+ slackpkgPackage, \
		shell=True, stdout=subprocess.PIPE).communicate()
	return stdout

# check for updates, reutrn True if available:
def checkUpdates():
	if 'No news is good news' in slackpkgAux('check-updates', ''):
		return False
	else:
		return True

# check for updates, reutrn True if available:
def update():
	# Don't re-download an identical changelog
	if checkUpdates():
		output = slackpkgAux('update', '')
		return output
	else:
		return 'No changes in ChangeLog.txt'

# upgrade everything: update repositories, install new packages, upgrade existing packages, clean system
def upgradeAll():
	return update() \
		+ slackpkgAux('install-new', '') \
		+ slackpkgAux ('upgrade-all', '')

def main():
	module = AnsibleModule(
		argument_spec = dict(
			action	= dict(required=True),
			package	= dict(required=False),
		),
	)

	# Get action and package from module parameters
	action = module.params.get('action')
	package = module.params.get('package')
	if package is None:
		package = ''

	# path to slackpkg script
	global slackpkgPath 
	slackpkgPath = '/usr/sbin/slackpkg'

	# flags for slackpkg, batch=on and -default_answer=y are a must execution via Ansible
	global slackpkgFlags
	slackpkgFlags = '-batch=on -default_answer=y -checksize=on'

	# call appropriate function
	if action == 'check-updates':
		module.exit_json(changed=False, updates=checkUpdates())
	if action == 'update':
		module.exit_json(output=update())
	elif action == 'upgrade-all':
		module.exit_json(output=upgradeAll())
	else:
		module.exit_json(output=slackpkgAux(action, package))

# import module snippets
from ansible.module_utils.basic import *
main()
