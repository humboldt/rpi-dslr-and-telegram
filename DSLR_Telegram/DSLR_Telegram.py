# -*- coding: utf-8 -*-
"""
TELEBOT - CONTROL DSLR
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

Bot_Name = "CameraBot"
Bot_Token = "INSERT TOKEN HERE"
	
Admin_Users = [00000000] # INSERT USER ID !
Authorized_Users = []

#################################################################################################
##### ROUTINES ##################################################################################
#################################################################################################
def getDictFromCmd(Command):
	Buffer = {}
	Shell_Output = subprocess.check_output(Command, shell=True)

	# Choice is the keyword! It is returned from gphoto2 into the shell.
	# We now take all the shell's return and look at it.
	# If 'Choice' is available, the data from the camera are followed by it.

	# 'Current' is the keyword for the current value.

	# This only works for ISO, Av, Tv, etc. and not for e.g. the connected cameras
	for Line in Shell_Output.split('\n'):
		if "Choice: " in Line:
			Buffer[Line.split(' ')[1]] = Line.split(' ')[2]
		elif "Current: " in Line:
			Buffer['C'] = Line.split(' ')[1]
		else:
			pass

	return Buffer
########################################################################################################################
##### PROCESS COMMANDS (ADMIN) #########################################################################################
########################################################################################################################
def commandAddUser(ID, Command):
	User_ID = Command.split(' ')[1]
	User_First_Name = Command.split(' ')[2]
	User_Last_Name = Command.split(' ')[3]

	if not int(User_ID) in Authorized_Users:
		Authorized_Users.append(int(User_ID))

		# Read data from file
		File_Content = []
		File_Object = open("auth_usr", "r")
		for Line in File_Object:
			File_Content.append(Line.split('\n')[0])
		File_Object.close()

		# Write date + new user
		File_Content.append(Command.split("/addUser ")[1])
		File_Object = open("auth_usr", "w")
		for Line in File_Content:
			File_Object.write(Line + "\n")
		File_Object.close()

		Bot.sendMessage(ID, "User added.")
		print "\n  Message sent."
		print "  User added."

	else:
		Bot.sendMessage(ID, "User already exists.")
		print "\n  Message sent."
		print "  User exists."
########################################################################################################################
##### PROCESS COMMANDS (USER) ##########################################################################################
########################################################################################################################
def commandStart(ID):
	Bot.sendMessage(ID, "Hello.\nI'm " + Bot_Name + ". I'm here to control your DSLR! You can send me commands (get them with /info) to make me do things for you.")
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
	Bot.sendMessage(ID, Info_Message)
	print "\n  Message sent." 

def commandGetCam(ID):
	Shell_Output = subprocess.check_output('gphoto2 --auto-detect', shell=True)
	Cam_List = []

	for Line in Shell_Output.split('\n'):
		if Line.startswith("Modell") or Line.startswith("---"):
			pass
		else:
			Cam_List.append(Line.split('   ')[0])

	if Cam_List == []:
		Bot.sendMessage(ID, "No camera connected.")
		print "\n  Message sent."
		print "No camera connected."
	else:
		Bot_Message = "Connected cameras:\n"
		for Line in Cam_List:
			Bot_Message += Line + "\n"
		Bot.sendMessage(ID, Bot_Message)
		print "\n  Message sent."

def commandGetISO(ID):
	ISO_Available = getDictFromCmd('gphoto2 --get-config iso')

	Bot_Message = "Available ISO:\n\n"
	for Key in ISO_Available:
		if Key != 'C':
			Bot_Message += Key + ": " + ISO_Available[Key] + "\n"
	Bot_Message += "\nCurrent ISO: " + ISO_Available['C']

	Bot.sendMessage(ID, Bot_Message)
	print "\n  Message sent."

def commandSetISO(ID, Command):
	ISO_Selected = Command.split(' ')[1]
	ISO_Available = getDictFromCmd('gphoto2 --get-config iso')

	if ISO_Selected in ISO_Available:
		command = "gphoto2 --set-config iso=" + str(ISO_Available[ISO_Selected])
		os.system(command)

		Bot.sendMessage(ID, "ISO set to " + ISO_Available[ISO_Selected] + ".")
		print "\n  Message sent."
		print "  ISO set."

	else:
		Bot.sendMessage(ID, "Your selected ISO value is not available.")
		print "\n  Message sent."
		print "  ISO value not available."

def commandGetAV(ID):
	AV_Available = getDictFromCmd('gphoto2 --get-config aperture')

	Bot_Message = "Available aperture values:\n\n"
	for Key in AV_Available:
		if Key != 'C':
			Bot_Message += Key + ": f/" + AV_Available[Key] + "\n"
	Bot_Message += "\nCurrent value: f/" + AV_Available['C']

	Bot.sendMessage(ID, Bot_Message)
	print "\n  Message sent."

def commandSetAV(ID, Command):
	AV_Selected = Command.split(' ')[1]
	AV_Available = getDictFromCmd('gphoto2 --get-config aperture')

	if AV_Selected in AV_Available:
		command = "gphoto2 --set-config aperture=" + str(AV_Available[AV_Selected])
		os.system(command)

		Bot.sendMessage(ID, "AV set to F/" + AV_Available[AV_Selected] + ".")
		print "\n  Message sent."
		print "  AV set."

	else:
		Bot.sendMessage(ID, "Your selected aperture value is not available.")
		print "\n  Message sent."
		print "  AV not available."

def commandGetTV(ID):
	TV_Available = getDictFromCmd('gphoto2 --get-config shutterspeed')

	Bot_Message = "Available shutter speeds:\n\n"
	for Key in TV_Available:
		if Key != 'C':
			Bot_Message += Key + ": " + TV_Available[Key] + "\n"
	Bot_Message += "\nCurrent value: " + TV_Available['C']

	Bot.sendMessage(ID, Bot_Message)
	print "\n  Message sent."

def commandSetTV(ID, Command):
	TV_Selected = Command.split(' ')[1]
	TV_Available = getDictFromCmd('gphoto2 --get-config shutterspeed')

	if TV_Selected in TV_Available:
		command = "gphoto2 --set-config shutterspeed=" + str(TV_Available[TV_Selected])
		os.system(command)

		Bot.sendMessage(ID, "TV set to " + TV_Available[TV_Selected] + ".")
		print "\n  Message sent."
		print "  TV set."

	else:
		Bot.sendMessage(ID, "Your selected shutter speed is not available.")
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
	Bot.sendPhoto(ID, Picture)

	os.remove("tmp.jpg")

	print "\n  Picture sent."
########################################################################################################################
##### TELEGRAM #########################################################################################################
########################################################################################################################
def accessNotfication(Time, ID, Title, Last_Name, First_Name, Command, SendToAdmin):
	# Print the access in the cmd
	print "\n- - - - - - - - - - - - - - - - - - - - - - - - - -\n"
	print "  Access recognized.\n"
	print "  Time:     " + str(Time)
	print "  ID:       " + str(ID)
	print "  Title:    " + str(Title)
	print "  User:     " + str(Last_Name) + ", " + str(First_Name)
	print "  Command:  " + str(Command)

	# Send the access to the amdins (but not, if the admin accesses the bot)
	if SendToAdmin and ID not in Admin_Users:
		for Admin in Admin_Users:
			Admin_Message = "Access recognized (Reminder).\n  Time: " + str(Time) + " (UTC)\n  ID: " + str(ID) + "\n  Title: " + str(Title) + "\n  User: " + str(Last_Name) + ", " + str(First_Name) + "\n  Command: " + str(Command)
			Bot.sendMessage(Admin, Admin_Message) 

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
	if Chat_ID in Admin_Users:
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
	if Chat_ID in Authorized_Users:
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
		Bot.sendMessage(Chat_ID, "Access denied.")
		accessNotfication(Received_Time, Chat_ID, Chat_Title, Chat_Last_Name, Chat_First_Name, Chat_Command, True)
		print "\n  Unauthorized user."
########################################################################################################################
##### MAIN #############################################################################################################
########################################################################################################################
if __name__ == "__main__":
	# Create authorized users file, if non-existend
	if not os.path.exists("auth_usr"):
		File_Object = open("auth_usr", "w")
		File_Object.close()

	# Get authorized users
	File_Object = open("auth_usr", "r")
	for Line in File_Object:
		Authorized_Users.append(int(Line.split(' ')[0]))

	# Setup bot
	Bot = telepot.Bot(Bot_Token)
	Bot_Info = Bot.getMe()
	Bot.message_loop(messageHandler)

	# Startup phrase
	os.system('clear')
	print "TELEBOT DSLR v1.0.0"
	print Bot_Info['first_name'] + " initialized."
	for Admin in Admin_Users:
		Bot.sendMessage(Admin, "Telebot 'DSLR' started.")

	# Loop
	while True:
		pass
########################################################################################################################
##### END OF CODE ######################################################################################################
########################################################################################################################