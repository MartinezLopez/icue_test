#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  main.py
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

from ventana import *

def main():
  '''Punto de entrada de la aplicacion.
  
  Crea un objeto de la clase VentanaPrincipal para iniciar la GUI.
  
  '''
  app = QtGui.QApplication(sys.argv)
  app.setStyle("cleanlooks")
  main_window = VentanaPrincipal()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
