PYTHON = python3
XEMU = /aux/builds/xemu/build/bin/xmega65.native -fastboot
ACME = acme
M65 = /aux/builds/mega65-tools/bin/m65
#
#		Directories
#
ROOTDIR =  $(dir $(realpath $(lastword $(MAKEFILE_LIST))))..$(S)
#
#		Uncommenting .SILENT will shut the whole build up.
#
ifndef VERBOSE
#.SILENT:
endif

