# -*- coding: utf-8 -*-
"""
TELEbot - CONTROL DSLR
Version 1.0.0
DELOARTS Research Inc.
Philip Delorenzo
12.01.2016

This script runs a bot for telegram.
It allows authorized users to control a dslr.

The chat-syntax is:

	/start    			Start the bot
	/info 				Returns syntax information
	/getCam 			Returns connected cameras			
	/getISO 			Returns available ISO values
	/setISO <value>		Sets ISO value
	/getAV 				Retunrs available AV value
	/setAV <value>		Sets AV value
	/getTV 				Returns available TV value
	/setTV <value> 		Sets TV value
	/pic 				Takes picture and sends it

Syntax for admin:
	/addUser <ID> <first name> <last name>

"""

import os
import sys
import glob
import telepot
import datetime
import subprocess

botName = "Camerabot"
botToken = "INSERT TOKEN HERE"
	
adminUsers = [00000000] # INSERT USER ID !
authUsers = []

def getDictFromCmd(Command):
	buffer = {}
	shellOut = subprocess.check_output(Command, shell=True)

	# Choice is the keyword! It is returned from gphoto2 into the shell.
	# We now take all the shell's return and look at it.
	# If 'Choice' is available, the data from the camera are followed by it.

	# 'Current' is the keyword for the current value.

	# This only works for ISO, Av, Tv, etc. and not for e.g. the connected cameras
	for line in shellOut.split('\n'):
		if "Choice: " in line:
			buffer[line.split(' ')[1]] = line.split(' ')[2]
		elif "Current: " in line:
			buffer['C'] = line.split(' ')[1]
		else:
			pass

	return buffer

def commandAddUser(ID, Command):
	userID = Command.split(' ')[1]
	userFirstName = Command.split(' ')[2]
	userLastName = Command.split(' ')[3]

	if not int(userID) in authUsers:
		authUsers.append(int(userID))

		# Read data from file
		fileContent = []
		fileObject = open("auth_usr", "r")
		for line in fileObject:
			fileContent.append(line.split('\n')[0])
		fileObject.close()

		# Write date + new user
		fileContent.append(Command.split("/addUser ")[1])
		fileObject = open("auth_usr", "w")
		for line in fileContent:
			fileObject.write(line + "\n")
		fileObject.close()

		bot.sendMessage(ID, "User added.")
		print "\n  Message sent."
		print "  User added."

	else:
		bot.sendMessage(ID, "User already exists.")
		print "\n  Message sent."
		print "  User exists."
########################################################################################################################
##### PROCESS COMMANDS (USER) ##########################################################################################
########################################################################################################################
def commandStart(ID):
	bot.sendMessage(ID, "Hello.\nI'm " + botName + ". I'm here to control your DSLR! You can send me commands (get them with /info) to make me do things for you.")
	print "\n  Message sent."

def commandInfo(ID):
	Info_Message = "/start: start the bot on your device.\n"
	Info_Message += "/info: information about the bot.\n"
	Info_Message += "/getCam: Returns connected cameras.\n"
	Info_Message += "/getISO: Returns available ISO values.\n"
	Info_Message += "/setISO <value>: Sets ISO value.\n"
	Info_Message += "/getAV: Retunrs available AV value.\n"
	Info_Message += "/setAV <value>: Sets AV value.\n"
	Info_Message += "/getTV: Returns available TV value.\n"
	Info_Message += "/setTV <value>: Sets TV value.\n"
	Info_Message += "/pic: Takes picture and sends it.\n"
	bot.sendMessage(ID, Info_Message)
	print "\n  Message sent." 

def commandGetCam(ID):
	shellOut = subprocess.check_output('gphoto2 --auto-detect', shell=True)
	camList = []

	for line in shellOut.split('\n'):
		if line.startswith("Modell") or line.startswith("---"):
			pass
		else:
			camList.append(line.split('   ')[0])

	if camList == []:
		bot.sendMessage(ID, "No camera connected.")
		print "\n  Message sent."
		print "No camera connected."
	else:
		botMsg = "Connected cameras:\n"
		for line in camList:
			botMsg += line + "\n"
		bot.sendMessage(ID, botMsg)
		print "\n  Message sent."

def commandGetISO(ID):
	isoAvailable = getDictFromCmd('gphoto2 --get-config iso')

	botMsg = "Available ISO:\n\n"
	for Key in isoAvailable:
		if Key != 'C':
			botMsg += Key + ": " + isoAvailable[Key] + "\n"
	botMsg += "\nCurrent ISO: " + isoAvailable['C']

	bot.sendMessage(ID, botMsg)
	print "\n  Message sent."

def commandSetISO(ID, Command):
	isoSel = Command.split(' ')[1]
	isoAvailable = getDictFromCmd('gphoto2 --get-config iso')

	if isoSel in isoAvailable:
		command = "gphoto2 --set-config iso=" + str(isoAvailable[isoSel])
		os.system(command)

		bot.sendMessage(ID, "ISO set to " + isoAvailable[isoSel] + ".")
		print "\n  Message sent."
		print "  ISO set."

	else:
		bot.sendMessage(ID, "Your selected ISO value is not available.")
		print "\n  Message sent."
		print "  ISO value not available."

def commandGetAV(ID):
	avAvailable = getDictFromCmd('gphoto2 --get-config aperture')

	botMsg = "Available aperture values:\n\n"
	for Key in avAvailable:
		if Key != 'C':
			botMsg += Key + ": f/" + avAvailable[Key] + "\n"
	botMsg += "\nCurrent value: f/" + avAvailable['C']

	bot.sendMessage(ID, botMsg)
	print "\n  Message sent."

def commandSetAV(ID, Command):
	avSel = Command.split(' ')[1]
	avAvailable = getDictFromCmd('gphoto2 --get-config aperture')

	if avSel in avAvailable:
		command = "gphoto2 --set-config aperture=" + str(avAvailable[avSel])
		os.system(command)

		bot.sendMessage(ID, "AV set to F/" + avAvailable[avSel] + ".")
		print "\n  Message sent."
		print "  AV set."

	else:
		bot.sendMessage(ID, "Your selected aperture value is not available.")
		print "\n  Message sent."
		print "  AV not available."

def commandGetTV(ID):
	tvAvailable = getDictFromCmd('gphoto2 --get-config shutterspeed')

	botMsg = "Available shutter speeds:\n\n"
	for Key in tvAvailable:
		if Key != 'C':
			botMsg += Key + ": " + tvAvailable[Key] + "\n"
	botMsg += "\nCurrent value: " + tvAvailable['C']

	bot.sendMessage(ID, botMsg)
	print "\n  Message sent."

def commandSetTV(ID, Command):
	tvSel = Command.split(' ')[1]
	tvAvailable = getDictFromCmd('gphoto2 --get-config shutterspeed')

	if tvSel in tvAvailable:
		command = "gphoto2 --set-config shutterspeed=" + str(tvAvailable[tvSel])
		os.system(command)

		bot.sendMessage(ID, "TV set to " + tvAvailable[tvSel] + ".")
		print "\n  Message sent."
		print "  TV set."

	else:
		bot.sendMessage(ID, "Your selected shutter speed is not available.")
		print "\n  Message sent."
		print "  TV not available."

def commandTakePicture(ID):
	# Delete old picture (we don't want to keep pictures in the raspberry)
	listImages = glob.glob("tmp.jpg")
	if listImages != []:
		os.remove("tmp.jpg")

	# Take the picture ...
	os.system('gphoto2 --capture-image-and-download --filename tmp.jpg > /dev/null')

	# ... and send it
	Picture = open('tmp.jpg', 'rb')
	bot.sendPhoto(ID, Picture)

	os.remove("tmp.jpg")

	print "\n  Picture sent."

def accessNotfication(Time, ID, Title, Last_Name, First_Name, Command, SendToadmin):
	# Print the access in the cmd
	print "\n- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
	print "  Access recognized.\n"
	print "  Time:     " + str(Time)
	print "  ID:       " + str(ID)
	print "  Title:    " + str(Title)
	print "  User:     " + str(Last_Name) + ", " + str(First_Name)
	print "  Command:  " + str(Command)

	# Send the access to the amdins (but not, if the admin accesses the bot)
	if SendToadmin and ID not in adminUsers:
		for admin in adminUsers:
			admin_Message = "Access recognized (Reminder).\n  Time: " + str(Time) + " (UTC)\n  ID: " + str(ID) + "\n  Title: " + str(Title) + "\n  User: " + str(Last_Name) + ", " + str(First_Name) + "\n  Command: " + str(Command)
			bot.sendMessage(admin, admin_Message) 

# The messageHandler processes the incomming messages from telegram
def messageHandler(MSG):
	Chat_ID = Chat_First_Name = Chat_Last_Name = Chat_Title = Chat_Message_Type = Chat_Command = ""
	Received_Time = str(str(datetime.datetime.now()).split('.')[0])
	
	# Get chat ID (unique ID) and type of message
	Chat_ID = MSG['chat']['id']
	Chat_Message_Type = MSG['chat']['type']
	# Get the users first and last name
	# Use try & except, because some users don't have a last name, and groups only have an title!
	try:
		Chat_First_Name = MSG['chat']['first_name']
	except:
		Chat_First_Name = "empty"
	try:
		Chat_Last_Name = MSG['chat']['last_name']
	except:
		Chat_Last_Name = "empty"
	try:
		Chat_Title = MSG['chat']['title']
	except:
		Chat_Title = "empty"
	# Finally get the command
	Chat_Command = MSG['text']

	# Process admin commands
	if Chat_ID in adminUsers:
		if Chat_Message_Type == 'private':
			# ADD USER
			if Chat_Command.startswith("/addUser "):
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, False)
				commandAddUser(Chat_ID, Chat_Command)
			# ERROR
			else:
				pass
		else:
			pass

	# Check if user is allowed to send messages to the bot
	if Chat_ID in authUsers:
		if Chat_Message_Type == 'private' or Chat_Message_Type == 'group':
			# START
			if Chat_Command == "/start":
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandStart(Chat_ID)
			# INFO
			elif Chat_Command == "/info":
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandInfo(Chat_ID)     
			# GET CONNECTED CAMERA
			elif Chat_Command == "/getCam":
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandGetCam(Chat_ID) 
			# GET ISO
			elif Chat_Command == "/getISO":
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandGetISO(Chat_ID) 
			# SET ISO
			elif Chat_Command.startswith("/setISO "):
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandSetISO(Chat_ID, Chat_Command) 
			# GET AV
			elif Chat_Command == "/getAV":
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandGetAV(Chat_ID) 
			# SET AV
			elif Chat_Command.startswith("/setAV "):
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandSetAV(Chat_ID, Chat_Command) 
			# GET TV
			elif Chat_Command == "/getTV":
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandGetTV(Chat_ID) 
			# SET TV
			elif Chat_Command.startswith("/setTV "):
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandSetTV(Chat_ID, Chat_Command) 
			# TAKE PICTURE
			elif Chat_Command == "/pic":
				accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
				commandTakePicture(Chat_ID) 
			# ERROR
			else:
				pass
		else:
			pass

	# Unauthorized access
	else:
		bot.sendMessage(Chat_ID, "Access denied.")
		accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
		print "\n  Unauthorized user."

if __name__ == "__main__":
	# Create authorized users file, if non-existend
	if not os.path.exists("auth_usr"):
		fileObject = open("auth_usr", "w")
		fileObject.close()

	# Get authorized users
	fileObject = open("auth_usr", "r")
	for line in fileObject:
		authUsers.append(int(line.split(' ')[0]))

	# Setup bot
	bot = telepot.bot(botToken)
	botInfo = bot.getMe()
	bot.message_loop(messageHandler)

	# Startup phrase
	os.system('clear')
	print "TELEbot DSLR v1.0.0"
	print botInfo['first_name'] + " initialized."
	for admin in adminUsers:
		bot.sendMessage(admin, "Telebot 'DSLR' started.")

	# Loop
	while True:
		pass