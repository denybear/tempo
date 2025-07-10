# library from: https://github.com/blaz-r/pi_pico_neopixel
# library from: https://docs.circuitpython.org/en/stable/shared-bindings/usb_midi/
# library from: https://github.com/adafruit/Adafruit_CircuitPython_MIDI
# this uses circuitpython, NOT micropython !!!
# URL for .UF2: https://circuitpython.org/board/raspberry_pi_pico/

import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from neopixel import Neopixel

# number of pixels
numpix = 5
# state machine 0, GPIO 0
pixels = Neopixel(numpix, 0, 0, "GRB")

# colors
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
chartreuse = (128,255,0)
green = (0, 255, 0)
spring = (0,255,128)
cyan = (0,255,255)
azure = (0,128,255)
blue = (0, 0, 255)
violet = (128, 0, 255)
magenta = (255, 0, 255)
rose = (255,0,128)
colors = [black, red, orange, yellow, chartreuse, green, spring, cyan, azure, blue, violet, magenta, rose, red]

#  midi setup
print (usb_midi.ports)
midi = adafruit_midi.MIDI (midi_in = usb_midi.ports[0], in_channel = 1)

while True:
    #  receive midi messages
    msg = midi.receive()

    if msg is not None:
        #  if a NoteOn message, light all the strip
        if isinstance(msg, NoteOn) and msg.velocity !=0:
            string_msg = 'NoteOn'
            #  get note number
            string_val = str(msg.note)	
			pixels.fill (red)

        #  if a NoteOff message, unlight all the strip
        if isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
            string_msg = 'NoteOff'
            #  get note number
            string_val = str(msg.note)
			pixels.clear ()

        #  update text area with message type and value of message as strings
        text_area.text = (string_msg + " " + string_val)


"""
NEO PIXEL EXAMPLES:

pixels.set_pixel(5, (10, 0, 0))
pixels.set_pixel_line(5, 7, (0, 10, 0))
pixels.fill((20, 5, 0))

rgb1 = (0, 0, 50)
rgb2 = (50, 0, 0)
pixels.set_pixel(42, (0, 50, 0))
pixels.set_pixel_line(5, 7, rgb1)
pixels.set_pixel_line_gradient(0, 13, rgb1, rgb2)

For new settings to take effect you write:
pixels.show()

howBright parameter for lightness (0 to 255)
pixels.set_pixel(5, (10, 0, 0), howBright)
"""
