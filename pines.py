#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  pines.py
#  
#  Author: Miguel Angel Martinez Lopez <miguelang.martinezl@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Some code here is reused from Adafruit_Python_GPIO/Adafruit_GPIO/Platform.py
#  Copyright (c) 2014 Adafruit Industries
#  Author: Tony DiCola

import platform
import re
from singleton import Singleton

@Singleton
class PinesFPGA:
  
  def __init__(self):
	  
	pi = self.pi_version()
	if pi is not None:
		import RPi.GPIO as gpio #RbP
		self.gpio = gpio
		self.pines = {'l1_ls': 12,'l1_ms': 11, 'r1_ls': 22, 'r1_ms': 21,'l2_ls': 16,'l2_ms': 15, 'r2_ls': 24, 'r2_ms': 23, 'sync_ls': 19, 'sync_ms': 18, 'rst': 13} #RbP
		gpio.setmode(gpio.BOARD) #RbP
		print 'Raspberry'
	else:
		'''plat = platform.platform()
		if plat.lower().find('armv7l-with-debian') > -1:
			import Adafruit_BBIO.GPIO as gpio #BBB
			self.pines = {'l1_ls': "P8_10",'l1_ms': "P8_8", 'r1_ls': "P8_14", 'r1_ms': "P8_12",'l2_ls': "P8_9",'l2_ms': "P8_7", 'r2_ls': "P8_13", 'r2_ms': "P8_11", 'sync_ls': "P8_18", 'sync_ms': "P8_16", 'rst': "P8_17"} #BBB
			print 'BBB'
		'''
		import Adafruit_BBIO.GPIO as gpio #BBB
		self.gpio = gpio
		self.pines = {'l1_ls': "P8_10",'l1_ms': "P8_8", 'r1_ls': "P8_14", 'r1_ms': "P8_12",'l2_ls': "P8_9",'l2_ms': "P8_7", 'r2_ls': "P8_13", 'r2_ms': "P8_11", 'sync_ls': "P8_18", 'sync_ms': "P8_16", 'rst': "P8_17"} #BBB
	
	'''for i in self.pines.keys():
		gpio.setup(self.pines[i], gpio.OUT)
		gpio.output(self.pines[i], gpio.LOW)
	'''
	[gpio.setup(self.pines[i], gpio.OUT) for i in self.pines.keys()]	
	[gpio.output(self.pines[i], gpio.LOW) for i in self.pines.keys()]
	self.reset(True)
		
  def pi_version(self):
    """Detect the version of the Raspberry Pi.  Returns either 1, 2 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), or not a Raspberry Pi.
    """
    # Check /proc/cpuinfo for the Hardware field value.
    # 2708 is pi 1
    # 2709 is pi 2
    # Anything else is not a pi.
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return 1
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return 2
    else:
        # Something else, not a pi.
        return None
  
  def setLength1(self, length):
    gpio = self.gpio
    if length == 0:
      gpio.output(self.pines["l1_ms"], gpio.LOW)
      gpio.output(self.pines["l1_ls"], gpio.LOW)
    elif length == 1:
      gpio.output(self.pines["l1_ms"], gpio.LOW)
      gpio.output(self.pines["l1_ls"], gpio.HIGH)
    elif length == 2:
      gpio.output(self.pines["l1_ms"], gpio.HIGH)
      gpio.output(self.pines["l1_ls"], gpio.LOW)
    elif length == 3:
      gpio.output(self.pines["l1_ms"], gpio.HIGH)
      gpio.output(self.pines["l1_ls"], gpio.HIGH)
  
  def setRate1(self, rate):
    gpio = self.gpio
    if rate == 0:
      gpio.output(self.pines["r1_ms"], gpio.LOW)
      gpio.output(self.pines["r1_ls"], gpio.LOW)
    elif rate == 1:
      gpio.output(self.pines["r1_ms"], gpio.LOW)
      gpio.output(self.pines["r1_ls"], gpio.HIGH)
    elif rate == 2:
      gpio.output(self.pines["r1_ms"], gpio.HIGH)
      gpio.output(self.pines["r1_ls"], gpio.LOW)
    elif rate == 3:
      gpio.output(self.pines["r1_ms"], gpio.HIGH)
      gpio.output(self.pines["r1_ls"], gpio.HIGH)
  
  def setLength2(self, length):
    gpio = self.gpio
    if length == 0:
      gpio.output(self.pines["l2_ms"], gpio.LOW)
      gpio.output(self.pines["l2_ls"], gpio.LOW)
    elif length == 1:
      gpio.output(self.pines["l2_ms"], gpio.LOW)
      gpio.output(self.pines["l2_ls"], gpio.HIGH)
    elif length == 2:
      gpio.output(self.pines["l2_ms"], gpio.HIGH)
      gpio.output(self.pines["l2_ls"], gpio.LOW)
    elif length == 3:
      gpio.output(self.pines["l2_ms"], gpio.HIGH)
      gpio.output(self.pines["l2_ls"], gpio.HIGH)
  
  def setRate2(self, rate):
    gpio = self.gpio
    if rate == 0:
      gpio.output(self.pines["r2_ms"], gpio.LOW)
      gpio.output(self.pines["r2_ls"], gpio.LOW)
    elif rate == 1:
      gpio.output(self.pines["r2_ms"], gpio.LOW)
      gpio.output(self.pines["r2_ls"], gpio.HIGH)
    elif rate == 2:
      gpio.output(self.pines["r2_ms"], gpio.HIGH)
      gpio.output(self.pines["r2_ls"], gpio.LOW)
    elif rate == 3:
      gpio.output(self.pines["r2_ms"], gpio.HIGH)
      gpio.output(self.pines["r2_ls"], gpio.HIGH)
  
  def setClock(self, clock):
    gpio = self.gpio
    if clock == 1:
      gpio.output(self.pines["sync_ms"], gpio.LOW)
      gpio.output(self.pines["sync_ls"], gpio.LOW)
    if clock == 2:
      gpio.output(self.pines["sync_ms"], gpio.HIGH)
      gpio.output(self.pines["sync_ls"], gpio.LOW)
    if clock == 3: #SoF1
      gpio.output(self.pines["sync_ms"], gpio.LOW)
      gpio.output(self.pines["sync_ls"], gpio.HIGH)
    if clock == 4: #SoF2
      gpio.output(self.pines["sync_ms"], gpio.HIGH)
      gpio.output(self.pines["sync_ls"], gpio.HIGH)
  
  def reset(self, state):
    gpio = self.gpio
    if state:
      gpio.output(self.pines["rst"], gpio.LOW)
      for i in range(100): # Perdemos tiempo
        a = i+1
      gpio.output(self.pines["rst"] , gpio.HIGH)
    else:
      gpio.output(self.pines["rst"], gpio.HIGH)
      
  def config(self, r1, l1, r2, l2, sync):
	  self.setRate1(r1)
	  self.setLength1(l1)
	  self.setRate2(r2)
	  self.setLength2(l2)
	  self.setClock(sync)
  
  def quitGPIO(self):
    self.gpio.cleanup()
