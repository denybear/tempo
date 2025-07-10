#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 Denybear
#
# SPDX-License-Identifier: MIT

"""
Receive messages from the input port and print them out.
"""
import sys
import mido
from mido.ports import multi_receive, multi_send


# Playlist definition
playList = [
	{"song":"Papa was a rolling stone", "artist":"Temptations", "bpm":110},
	{"song":"I don't want a lover", "artist":"Texas", "bpm":120}
]


class NovationLaunchpad:
	# name
	name ='Launchpad Mini'

	# colors of the pads
	padColor = {
		'black':0x0C, 'lowRed':0x0D, 'highRed':0x0F, 'lowAmber':0x1D, 'highAmber':0x3F,
		'lowGreen':0x1C, 'highGreen':0x3C, 'lowOrange':0x1E, 'highOrange':0x2F, 'lowYellow':0x2D, 'highYellow':0x3E
	}

	def getKeyByValue (self, d, value):
		return next(filter(lambda item: item[1] == value, d.items()), (None,))[0]

	def padToTrack (self, val):		# convert padnumber into track number: from 0x00, 0x10, etc to 0-63
		# return (val >> 4) * 8 + (val && 0xF)
		return (((val && 0xF0) >> 1) + (val && 0x07))

	def trackToPad (self, val):		# convert track number into pad number: from 0-63 to 0x00, 0x10, etc
		# return ((val / 8) * 0x10) + (val % 8) 
		return (((val && 0xF0) << 1) + (val && 0x07) 
		
	def __init__(self):
		pass

	def clear (self):	# reset launchpad: B0 00 00
		lst = []
		lst.append (mido.Message ('control_change', control = 0, value = 0))
		#lst.append (mido.Message.from_bytes([0xB0, 0x00, 0x00]))
		return lst
		
	def colorPad (self, pad, color):
		lst = []
		lst.append (mido.Message ('note_on', note = pad, velocity = self.padColor [color]))
		return lst

	def colorRightPads (self, color):		# apply a color to the pads on the right of Novation control
		rightPads = [0x08, 0x18, 0x28, 0x38, 0x48, 0x58, 0x68, 0x78]
		lst = []
		for i in rightPads:
			lst.append (mido.Message ('note_on', note = i, velocity = self.padColor [color]))
		return lst


# inits
control = NovationLaunchpad ()
prevPad = -1


# define and open ports
# virtual ports need to be created in windows. For this, use this software: https://www.tobias-erichsen.de/software/loopmidi.html
# get the right port numbers for all ports that need to be opened
inPorts = []
outPorts = []
displayPorts = []


names = mido.get_input_names()
for name in names:
	if (control.name in name):
		inPorts.append (mido.open_input(name))			# use virtual=True on non-windows systems

names = mido.get_output_names()
for name in names:
	if ('tempoOUT' in name):
		outPorts.append (mido.open_output(name))		# use virtual=True on non-windows systems

names = mido.get_output_names()
for name in names:
	if (control.name in name):
		displayPorts.append (mido.open_output(name))


# clear display (control pad), then light pads corresponding to playlist elements
msgDisplayList = []
msgDisplayList.extend (control.clear ())
for i in range (len (playList)):
	msgDisplayList.extend (control.colorPad (control.trackToPad (i), "highAmber"))
for msg in msgDisplayList:
	multi_send (displayPorts, msg)


# main loop

try:

	for inPort in inPorts:
		print (f'Using IN:{inPort}')
	for outPort in outPorts:
		print (f'Using OUT:{outPort}')
	for displayPort in displayPorts:
		print (f'Using DISPLAY:{displayPort}')

	
	for messageIn in multi_receive (inPorts):

		if messageIn.type in ('note_on')):		# we manage only note on events from pads
			if messageIn.velocity == 0:			# note on with 0 velocity == note off
				break

			pad = messageIn.note
			# convert padnumber into actual track number: from 0x00, 0x10, etc to 0-63
			trackNumber = control.padToTrack (pad)
			# make sure the pressed pad is in the playlist; otherwise do nothing
			if trackNumber >= len (playList):
				break

			# deal with pad lighting / unlighting
			# light pressed pad in red, previous pad in highAmber
			# if same pad is pressed twice, it means song should be stopped
			msgDisplayList = []

			if (prevPad == pad):		# same pad is pressed twice : it means stop
				msgDisplayList.extend (control.colorPad (pad, "highAmber"))		# pressed pad becomes amber again
				prevPad = -1
				# also unlit the pads on the right of Novation control (used to show the rhythm)
				msgDisplayList.extend (control.colorRightPads ("black"))
				# send message to output (eg. reaper) indicating to stop via note-off
				messageOut = mido.Message ('note_off', note = trackNumber, velocity = 0x00)

			else:
				if (prevPad != -1):
					msgDisplayList.extend (control.colorPad (prevPad, "highAmber"))
				msgDisplayList.extend (control.colorPad (pad, "highRed"))
				prevPad = pad
				# send message to output (eg. reaper) indicating to play at the right BPM (sent as velocity = BPM/2)
				messageOut = mido.Message ('note_on', note = trackNumber, velocity = (playList [trackNumber]["bpm"] >> 1))

			
			# send messages to midi outputs
			for msg in msgDisplayList:
				multi_send (displayPorts, msg)

			for msg in messageOut:
				multi_send (outPorts, msg)

except KeyboardInterrupt:
	pass


"""
TO DO:

XSend BPM info to Reaper

Reaper would feature a track for each song:
1- program change code for the bass
2- metronome track for lighting of Novation circuit (notes on on 0x08, 0x18, etc) + lighting of raspi
3- battery track if required
Reaper should have an action developed to:
a1- determine if note-on or note-off to start of stop 
a2- stop current playing
b- get the track number, select the right track (or group of tracks)
c- adjust playback speed
d- rewind, play all the track/subtracks at correct speed

Start functionality: should be included in reaper
XStop functionality: done
XPressed pad could light with rhythm: no, but right round pads will lit with rhythm: this is done in reaper

Display song name in BIG on the screen
"""
