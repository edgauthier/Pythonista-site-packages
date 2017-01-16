# This version of the getpass module was written specifically for the Pythonista
# UI. It only provides the getpass function (and not getuser, as iOS is not a 
# multi-user environment). Additionally, getpass has no stream parameter in this
# version.
# 
# Original Author: Ole Zorn
#
# Overridden version to strip trailing newline and
# match behavior on other operating systems.

import console

def getpass(prompt='Password: '):
	"""Prompt for a password.
	
	Args:
	  prompt: Written to the console to ask for input. Default: 'Password: '
	Returns:
	  The seKr3t input.
	"""
	
	password = console.secure_input(prompt).rstrip('\n')
	return password
