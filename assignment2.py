#!/usr/bin/python

## ============================================================================
# 	Name        : Filelist, CMPE230
# 	Author      : Berke Esmer & Cemal Aytekin
# 	Description : In this project, we implement a simple application called
#				  filelist. It takes several parameters and searches for
#				  files that meets the criteria.
# 	Environment : Python 2.7.15rc1
# 	How to Run  : python filelist.py [options] [directory list]
#	Example		: python filelist.py -bigger 10M zip myzip.zip ~/Documents 
## ============================================================================

import re
import os
import sys
import filecmp
import datetime
import collections

## Takes all the given command options and paths as parameters. Then it finds all the files recursively and executes commands.
# commands: All user input options.
# paths: All user input file folder paths.
def processCommands(commands, paths):
	global files
	global stats_totalNumberOfFiles
	global stats_totalBytesOfFiles

	# Finding all files in the given paths recursively.
	while paths:
		currentDir = paths.popleft()
		dirContents = os.listdir(currentDir)

		# Searching every item and checking whether they are folders or files.
		for entity in dirContents:
			currentEntity = currentDir + "/" + entity

			# If it is a folder, add it to the paths in order to execute the code recursively.
			if os.path.isdir(currentEntity):
				paths.append(currentEntity)
			else:
				files.append(currentEntity)
				stats_totalNumberOfFiles += 1
				stats_totalBytesOfFiles += os.path.getsize(currentEntity)

	# Directing the files into all the commands one by one. Some of them needs an argument..
	while commands:
		currentCommand = commands.popleft()

		if currentCommand == '-before':
			arg = commands.popleft()
			beforeFunc(arg)

		elif currentCommand == '-after':
			arg = commands.popleft()
			afterFunc(arg)

		elif currentCommand == '-match':
			arg = commands.popleft()
			matchFunc(arg)

		elif currentCommand == '-bigger':
			arg = commands.popleft()
			biggerFunc(arg)

		elif currentCommand == '-smaller':
			arg = commands.popleft()
			smallerFunc(arg)

		elif currentCommand == '-delete':
			deleteFunc()

		elif currentCommand == '-zip':
			arg = commands.popleft()
			zipFunc(arg)

		elif currentCommand == '-duplcont':
			duplcontFunc()

		elif currentCommand == '-duplname':
			duplnameFunc()

		elif currentCommand == '-stats':
			statsFunc()

		elif currentCommand == '-nofilelist':
			nofilelistFunc()

## -zip and -delete options do not contribute to the elimination process. Those are executed after others.
def processActions():
	global files
	global isZip
	global isDelete
	global zipName
	result_files = []

	# It first creates a temporary folder. It puts every files that are left after elimination into that folder. It zips them.
	# Files that have duplicate names are named as : file.txt, (2)file.txt, (3)file.txt
	if isZip:
		global zipName

		os.system("mkdir XksgPuwk2962")

		for file in files:
			dirContents = os.listdir("./XksgPuwk2962")
			fileName = os.path.basename(file)
			duplCounter = 1

			for i in range(len(dirContents)):
				index = 0

				if dirContents[i][0] == '(':
					index = dirContents[i].index(')')
					index += 1

				if fileName == dirContents[i][index:]:
					duplCounter += 1

			if duplCounter == 1:
				os.system("cp \"" + file + "\" ./XksgPuwk2962/")

			else:
				os.system("cp \"" + file + "\" './XksgPuwk2962/" + "(" + str(duplCounter) + ")" + fileName + "'")				

		os.system("cd XksgPuwk2962; zip " + zipName + " *; mv " + zipName + " ../; cd ..; rm -r XksgPuwk2962/")

	# It deletes every file that are left after elimination.
	if isDelete:
		for file in files:
			os.remove(file)

		files = []

## A sorting function. Files are sorted based on their filenames, not on their paths.
# arr : The list of all files.
def bubbleSort(arr):
	size = len(arr)

	for i in range(size):
		for j in range(0, size-i-1):
			s1 = os.path.basename(arr[j])
			s2 = os.path.basename(arr[j+1])

			if s1 > s2:
				arr[j], arr[j+1] = arr[j+1], arr[j]

## The final stage of the program. It first decides on the printing style. Then if it is necessary, it prints stats.
def printListing():
	global files
	global fileListing
	global statsListing
	global isDuplCont
	global isDuplName
	global stats_totalNumberOfFiles
	global stats_totalBytesOfFiles
	listed_totalNumberOfFiles = 0
	listed_totalBytesOfFiles = 0
	duplcont_totalNumberOfUniqueFiles = 0
	duplcont_totalBytesOfUniqueFiles = 0
	duplname_totalNumberOfUniqueFiles = 0

	# Sorting files first.
	bubbleSort(files)

	# The first printing style. It prints files that have same name back to back. It puts "------" after every group of files.
	if (fileListing and isDuplName):
		final_list = []
		size = len(files)

 	  	for i in range(size):
			if files[i] not in final_list:
				final_list.append(files[i])

				for j in range(0, size-i-1):
					if files[i] != files[j]:
		 				fileName1 = os.path.basename(files[i])
						fileName2 = os.path.basename(files[j])

						# This check is for duplname.
						if fileName1 == fileName2:
							if files[j] not in final_list:
								final_list.append(files[j])
				
				duplname_totalNumberOfUniqueFiles +=1
				final_list.append("------")

		if len(final_list) != 0:
			print "------"

		# Printing...
		for fileElement in final_list:
			print(fileElement)

			if fileElement != "------":
				listed_totalNumberOfFiles +=1
				listed_totalBytesOfFiles += os.path.getsize(fileElement)

	# The second printing style. It prints files that have the same content back to back. It puts "------" after every group of files.
	elif (fileListing and isDuplCont):
		final_list = []
		size = len(files)

 	  	for i in range(size):
			if files[i] not in final_list:
				final_list.append(files[i])
				duplcont_totalBytesOfUniqueFiles += os.path.getsize(files[i])

				for j in range(0, size-i-1):
					if files[i] != files[j]:
		 				fileName1 = os.path.basename(files[i])
						fileName2 = os.path.basename(files[j])

						# This check is for duplcont.
						if filecmp.cmp(files[i],files[j], shallow=False):
							if files[j] not in final_list:
								final_list.append(files[j])
	
				duplcont_totalNumberOfUniqueFiles +=1
				final_list.append("------")

		if len(final_list) != 0:
			print "------"

		# Printing...
		for fileElement in final_list:
			print(fileElement)

			if fileElement != "------":
				listed_totalNumberOfFiles +=1
				listed_totalBytesOfFiles += os.path.getsize(fileElement)

	# Default file printing style. It just prints all the files in the sorted manner.
	elif fileListing:
		for file in files:
			print file

			listed_totalNumberOfFiles += 1
			listed_totalBytesOfFiles += os.path.getsize(file)

	# If -stats option is given, it prints default four stats. After, it prints duplcont or duplname stats if their option is given.
	if statsListing:
		print "Total number of files visited: " + str(stats_totalNumberOfFiles)
		print "Total size of files visited: " + str(stats_totalBytesOfFiles) + " bytes"
		print "Total number of files listed: " + str(listed_totalNumberOfFiles)
		print "Total size of files listed: " + str(listed_totalBytesOfFiles) + " bytes"

		if isDuplCont:
			print "Total number of unique files listed: " + str(duplcont_totalNumberOfUniqueFiles)
			print "Total size of unique files listed: " + str(duplcont_totalBytesOfUniqueFiles) + " bytes"

		if isDuplName:
			print "Total number of unique files with unique names listed: " + str(duplname_totalNumberOfUniqueFiles)	

## It finds all the files that has modification date and time before the given argument. An elimination option.
# arg: The user input for [modification date]T[modification time]
def beforeFunc(arg):
	global files
	result_files = []

	# Every file is examined during the process.
	for file in files:
		modificationTime = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y%m%dT%H%M%S')

		# If the given time format is 'YYYYMMDD'.
		if len(arg) == 8:
			modDate = modificationTime[:8]

			if int(arg) >= int(modDate):
				result_files.append(file)

		# If the given time format is 'YYYYMMDDTHHMMSS'.
		elif len(arg) == 15:
			argDate = arg[:8]
			argTime = arg[9:]
			modDate = modificationTime[:8]
			modTime = modificationTime[9:]

			if int(argDate) >= int(modDate):
				result_files.append(file)

			elif int(argDate) == int(modDate):
				if int(argTime) >= int(modTime):
					result_files.append(file)

	files = result_files 

## It finds all the files that has modification date and time after the given argument. An elimination option.
# arg: The user input for [modification date]T[modification time]
def afterFunc(arg):
	global files
	result_files = []

	# Every file is examined during the process.
	for file in files:
		modificationTime = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y%m%dT%H%M%S')

		# If the given time format is 'YYYYMMDD'.
		if len(arg) == 8:
			modDate = modificationTime[:8]

			if int(arg) <= int(modDate):
				result_files.append(file)

		# If the given time format is 'YYYYMMDDTHHMMSS'.
		elif len(arg) == 15:
			argDate = arg[:8]
			argTime = arg[9:]
			modDate = modificationTime[:8]
			modTime = modificationTime[9:]

			if int(argDate) <= int(modDate):
				result_files.append(file)

			elif int(argDate) == int(modDate):
				if int(argTime) <= int(modTime):
					result_files.append(file)

	files = result_files 

## It finds all the files that have the given regex string format. An elimination option.
# arg: The user input for regex.
def matchFunc(arg):
	global files
	result_files = []

	# Every file is examined during the process.
	for file in files:
		fileName = os.path.basename(file)		
		
		# Checking if the filename (not the path) has the regex format.
		if re.search(arg, fileName):
			result_files.append(file)

	files = result_files

## It finds all the files that have size bigger than the given argument. An elimination option.
# arg: The user input for file size.
def biggerFunc(arg):
	global files
	result_files = []

	# If given argument is in kilobytes.
	if arg[len(arg)-1:] == "K":
		arg = int(arg[:len(arg)-1])*1024

	# If given argument is in megabytes.
	elif arg[len(arg)-1:] == "M":
		arg = int(arg[:len(arg)-1])*1024*1024

	# If given argument is in gigabytes.
	elif arg[len(arg)-1:] == "G":
		arg = int(arg[:len(arg)-1])*1024*1024*1024

	# Every file is examined during the process.
	for file in files:
		fileSize = os.path.getsize(file)

		if int(fileSize) >= int(arg):
			result_files.append(file)

	files = result_files

## It finds all the files that have size smaller than the given argument. An elimination option.
# arg: The user input for file size.
def smallerFunc(arg):
	global files
	result_files = []

	# If given argument is in kilobytes.
	if arg[len(arg)-1:] == "K":
		arg = int(arg[:len(arg)-1])*1024

	# If given argument is in megabytes.
	elif arg[len(arg)-1:] == "M":
		arg = int(arg[:len(arg)-1])*1024*1024

	# If given argument is in gigabytes.
	elif arg[len(arg)-1:] == "G":
		arg = int(arg[:len(arg)-1])*1024*1024*1024

	# Every file is examined during the process.
	for file in files:
		fileSize = os.path.getsize(file)

		if int(fileSize) <= int(arg):
			result_files.append(file)

	files = result_files

## It enables the usage of deletion by changing the boolean value.
def deleteFunc():
	global isDelete

	isDelete = True

## It enables the usage of zipping by changing the boolean value.
# arg: The user input zipname. (E.g. mylist.zip)
def zipFunc(arg):
	global isZip
	global zipName

	isZip = True
	zipName = arg

## It enables the searching of duplcont by changing the boolean value.
def duplcontFunc():
	global isDuplCont

	isDuplCont = True

## It enables the searching of duplname by changing the boolean value.	
def duplnameFunc():
	global isDuplName

	isDuplName = True
	
## It enables the printing of stats by changing the boolean value.
def statsFunc():
	global statsListing

	statsListing = True

## It disables the file listing.
def nofilelistFunc():
	global fileListing

	fileListing = False

## Main function

# args 		=> System arguments taken from the terminal which contains user inputs.
# commands 	=> An initialized deque in order the store all the options.
# paths 	=> An initialized deque in order the store all the paths.
# files 	=> An initialized list in order the store all the files in the paths.

args = sys.argv
commands = collections.deque()
paths = collections.deque()
files = []

# fileListing 	=> A boolean value for deciding on printing the list of files.
# statsListing 	=> A boolean value for deciding on printing the stats of files.
# isDuplCont 	=> A boolean value for deciding on using duplcont functionality.
# isDuplName 	=> A boolean value for deciding on using duplname functionality.
# isDelete 		=> A boolean value for deciding on deleting all the files that are left after eliminations.
# isZip 		=> A boolean value for deciding on zipping all the files that are left after elimination.
# zipName 		=> A string initilization for given zipname argument.

fileListing = True
statsListing = False
isDuplCont = False
isDuplName = False
isDelete = False
isZip = False
zipName = ""

# stats_totalNumberOfFiles 	=> A statistic variable for finding total number of files.
# stats_totalBytesOfFiles 	=> A statistic variable for finding total size of files.

stats_totalNumberOfFiles = 0
stats_totalBytesOfFiles = 0

# Examining all system arguments and deciding on which list they belong to. (Command or Path?)
for i in range(1, len(args)):
	currentArg = args[i]

	if os.path.isdir(currentArg):
		if currentArg[len(currentArg)-1:] == "/":
			paths.append(currentArg[:len(currentArg)-1])
		else:
			paths.append(currentArg)

	else:
		commands.append(currentArg)

# If there is no path argument, the current directory will be accepted as default.
if len(paths) == 0:
	paths.append(".")

# Run the program.
processCommands(commands, paths)
processActions()
printListing()