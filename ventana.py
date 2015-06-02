#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  ventana.py
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

import sys
from PyQt4 import QtGui, QtCore
from osciloscopio import Osciloscopio
from pines import PinesFPGA
import time
#from modbus import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


class VentanaPrincipal(QtGui.QWidget):
	def __init__(self):
		super(VentanaPrincipal, self).__init__()
		self.rellenaVentana()
	
	def rellenaVentana(self):
		montaje1 = QtGui.QGroupBox('Montaje 1')
		montaje2 = QtGui.QGroupBox('Montaje 2')
		sof1 =  QtGui.QPushButton('SoF CH1', self)
		sof2 =  QtGui.QPushButton('SoF CH2', self)
		ojo1 =  QtGui.QPushButton('Sync CH1', self)
		ojo2 =  QtGui.QPushButton('Sync CH2', self)
		cerrar = QtGui.QPushButton('Cerrar', self)
		
		tot_layout = QtGui.QVBoxLayout()
		l1 = QtGui.QHBoxLayout()
		l2 = QtGui.QHBoxLayout()
		l3 = QtGui.QHBoxLayout()
		
		#l1.addStretch(1)
		l1.addWidget(sof1)
		l1.addWidget(ojo1)
		#l1.addStretch(1)
		
		#l2.addStretch(1)
		l2.addWidget(sof2)
		l2.addWidget(ojo2)
		#l2.addStretch(1)
		
		l3.addStretch(1)
		l3.addWidget(cerrar)
		
		cerrar.clicked.connect(QtCore.QCoreApplication.instance().quit)
		sof1.clicked.connect(lambda: self.sof(1))
		sof2.clicked.connect(lambda: self.sof(2))
		ojo1.clicked.connect(lambda: self.ojo(1))
		ojo2.clicked.connect(lambda: self.ojo(2))
		
		montaje1.setLayout(l1)
		montaje2.setLayout(l2)
		
		#tot_layout.addLayout(l1)
		#tot_layout.addLayout(l2)
		tot_layout.addWidget(montaje1)
		tot_layout.addWidget(montaje2)
		tot_layout.addLayout(l3)
		
		self.setLayout(tot_layout)
		self.setWindowTitle(u'Diagnóstico ICUE')
		self.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
		self.setFixedSize(350, 200)
		self.show()
		
	def sof(self, ch):
		self.v = VentanaSof(ch)
	
	def ojo(self, ch):
		self.v = VentanaOjo(ch)
		
class VentanaResultados(QtGui.QWidget):
	dic_medida = {0:'Frecuencia: 10 MHz\nLongitud de trama: 4', 1:'Frecuencia: 10 MHz\nLongitud de trama: 8', 2:'Frecuencia: 10 MHz\nLongitud de trama: 12', 3:'Frecuencia: 10 MHz\nLongitud de trama: 16', 4:'Frecuencia: 30 MHz\nLongitud de trama: 4', 5:'Frecuencia: 30 MHz\nLongitud de trama: 8', 6:'Frecuencia: 30 MHz\nLongitud de trama: 12', 7:'Frecuencia: 30 MHz\nLongitud de trama: 16', 8:'Frecuencia: 70 MHz\nLongitud de trama: 4', 9:'Frecuencia: 70 MHz\nLongitud de trama: 8', 10:'Frecuencia: 70 MHz\nLongitud de trama: 12', 11:'Frecuencia: 70 MHz\nLongitud de trama: 16', 12:'Frecuencia: 125 MHz\nLongitud de trama: 4', 13:'Frecuencia: 125 MHz\nLongitud de trama: 8', 14:'Frecuencia: 125 MHz\nLongitud de trama: 12', 15:'Frecuencia: 125 MHz\nLongitud de trama: 16', 16:''}
	def __init__(self):
		super(VentanaResultados, self).__init__()
		self.config = 0
		self.creaInterfaz()
		osc = Osciloscopio.Instance()
		osc.set_display('YT')
		osc.set_trigger('ext5', 1)
		osc.disp_channel(True, '1')
		osc.set_vertical('1', '500mv', 'AC', '1')
		osc.disp_channel(True, '2')
		osc.set_vertical('2', '500mv', 'AC', '1')
		time.sleep(0.1)
	
	def creaInterfaz(self):
		vbox = QtGui.QVBoxLayout()
		self.figure = plt.figure(1)
		self.canvas = FigureCanvas(self.figure)
		self.canvas.setParent(self) 
		
		self.ax1 = plt.subplot2grid((2,1),(0,0))
		self.ax2 = plt.subplot2grid((2,1),(1,0))
		
		self.formatter_tiempo = EngFormatter(unit='s', places=2)
		self.ax1.xaxis.set_major_formatter(self.formatter_tiempo)
		self.ax2.xaxis.set_major_formatter(self.formatter_tiempo)
		
		correcto = QtGui.QPushButton('Correcto', self)
		correcto.setIcon(QtGui.QIcon('%s/img/ok.svg' % sys.path[0]))
		error = QtGui.QPushButton('Error', self)
		error.setIcon(QtGui.QIcon('%s/img/ko.svg' % sys.path[0]))
		correcto.clicked.connect(self.siguiente)
		error.clicked.connect(self.error)
		
		self.texto = QtGui.QLabel('Instrucciones')
		
		hbox = QtGui.QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(correcto)
		hbox.addWidget(error)
		
		vbox.addWidget(self.canvas)
		vbox.addWidget(self.texto)
		vbox.addLayout(hbox)
		self.setLayout(vbox)
		#self.setWindowTitle('Diagnostico ICUE')
		self.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
		self.show()
	
	def siguiente(self):
		print 'siguiente'
	
	def error(self):
		reply = QtGui.QMessageBox.question(self, u'Confirmación', u"¿Está seguro de que es un error?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		
		if reply == QtGui.QMessageBox.Yes:
			self.close()

class VentanaSof(VentanaResultados):
	dic_tb = {0:['250ns', '800E-9'], 1:['100ns', '260E-9'], 2:['25ns', '105E-9'], 3:['25ns','64E-9'], 4:['25ns','64E-9']}
	def __init__(self, ch):
		super(VentanaSof, self).__init__()
		self.setWindowTitle(u'Diagnóstico ICUE: SOF CH %d' % (ch,))
		self.ch = ch
		self.configuracion()
		self.medida()
	
	def configuracion(self):
		freq = self.config // 4 #Parte entera
		leng = self.config % 4  #Resto
		
		sync = {1:3, 2:4}
		
		osc = Osciloscopio.Instance()
		osc.set_tb(self.dic_tb[freq][0], self.dic_tb[freq][1])
		
		pines = PinesFPGA.Instance()
		pines.config(freq, leng, freq, leng, sync[self.ch])
	
	def medida(self):
		osc = Osciloscopio.Instance()
		
		#Para empezar supongo que solo queremos ver los unos y que con una base de tiempos podemos ver todo
		ch1, inc1 = osc.get_data('1', 1, 2500, '1')
		tiempos1 = []
		[tiempos1.append(inc1*i) for i in xrange(len(ch1))]
		
		self.ax1.cla()
		self.ax1.xaxis.set_major_formatter(self.formatter_tiempo)
		self.ax1.plot(tiempos1, ch1)
		
		ch2, inc2 = osc.get_data('2', 1, 2500, '1')
		tiempos2 = []
		[tiempos2.append(inc2*i) for i in xrange(len(ch2))]
		
		self.ax2.cla()
		self.ax2.xaxis.set_major_formatter(self.formatter_tiempo)
		self.ax2.plot(tiempos2, ch2)
		
		self.texto.setText(self.dic_medida[self.config])
		
		self.figure.canvas.draw()
	
	def siguiente(self):
		 QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		 QtCore.QCoreApplication.processEvents()
		 self.config += 1
		 self.configuracion()
		 self.medida()
		 QtGui.QApplication.restoreOverrideCursor()
		 if self.config == 16:
                         w = VentanaInfo('Se ha completado el test de manera satisfactoria')
                         self.close()


class VentanaOjo(VentanaResultados):
	dic_tb = {0:['25ns', '50E-9'], 1:['5ns', '22E-9'], 2:['2.5ns', '12E-9'], 3:['2.5ns','2E-9'], 4:['2.5ns','2E-9']}
	def __init__(self, ch):
		super(VentanaOjo, self).__init__()
		self.setWindowTitle(u'Diagnóstico ICUE: SYNC CH %d' % (ch,))
		self.ch = ch
		
		self.timer_osc = QtCore.QTimer()
		QtCore.QObject.connect(self.timer_osc, QtCore.SIGNAL("timeout()"), self.adquiere)
		
		self.osc = Osciloscopio.Instance()
		
		self.configuracion()
		self.medida()
	
	def configuracion(self):
		freq = self.config // 4 #Parte entera
		leng = self.config % 4  #Resto
		
		#sync = {1:3, 2:4} Aqui no hace falta porque ya son 1 y 2, pero podria cambiar en algun momento
		osc = Osciloscopio.Instance()
                osc.set_tb(self.dic_tb[freq][0], self.dic_tb[freq][1])
		
		pines = PinesFPGA.Instance()
		pines.config(freq, leng, freq, leng, self.ch)
	
	def medida(self):
		#self.adquisiciones = 0
		ch2, inc2 = self.osc.get_data('2', 1, 2500, '1')
		tiempos2 = []
		[tiempos2.append(inc2*i) for i in xrange(len(ch2))]
		
		self.ax2.cla()
		self.ax2.plot(tiempos2, ch2)
		self.ax2.xaxis.set_major_formatter(self.formatter_tiempo)
		
		self.texto.setText(self.dic_medida[self.config])
		
		self.timer_osc.start(700)
	
	def adquiere(self):
		ch1, inc1 = self.osc.get_data('1', 1, 2500, '1')
		tiempos1 = []
		[tiempos1.append(inc1*i) for i in xrange(len(ch1))]
		
		self.ax1.plot(tiempos1, ch1, 'b')
		self.figure.canvas.draw()
		
	def siguiente(self):
		 self.timer_osc.stop()
		 self.ax1.cla()
		 self.ax1.xaxis.set_major_formatter(self.formatter_tiempo)
		 QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		 QtCore.QCoreApplication.processEvents()
		 self.config += 1
		 self.configuracion()
		 self.medida()
		 QtGui.QApplication.restoreOverrideCursor()
		 if self.config == 16:
			 w = VentanaInfo('Se ha completado el test de manera satisfactoria')
			 self.close()
	
	def closeEvent(self, evnt):
		self.timer_osc.stop()
		super(VentanaOjo, self).closeEvent(evnt)
		
	def error(self):
		self.timer_osc.stop()
		super(VentanaOjo, self).error()

class VentanaInfo(QtGui.QWidget):
  '''Tiene un botón aceptar para volver al orden de ejecución'''
  
  def __init__(self, texto):
    '''Constructor de una ventana de información
    
    Parametros:
      texto: Texto que mostrará la ventana
    
    '''
    super(VentanaInfo, self).__init__()
    self.inicializa(texto)
  
  def inicializa(self, texto):
    win = QtGui.QMessageBox()
    win.timer = QtCore.QTimer(self)
    win.timer.timeout.connect(win.close)
    win.timer.start(30000) # Se cierra automaticamente a los 30 segundos
    win.setInformativeText(texto)
    win.setWindowTitle('Aviso')
    win.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
    win.exec_()
