#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Pedro Hurtado González

#This file is part of plhurtado/lassercut.

#plhurtado/lassercut is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#plhurtado/lassercut is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with plhurtado/lassercut.  If not, see <http://www.gnu.org/licenses/>.

import sys, inkex, simplestyle
sys.path.append('/usr/share/inkscape/extensions')

class crearCaja(inkex.Effect):

    def __init__(self):

        # Recuperación de los parámetros.
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--x", action="store", type="int", dest="x")
        self.OptionParser.add_option("--y", action="store", type="int", dest="y")
        self.OptionParser.add_option("--longitud", action="store", type="float", dest="longitud")
        self.OptionParser.add_option("--tab", action="store", type="string", dest="tab")
        
    def effect(self):
        #Guardo los parámetros en variables sencillas
        x = self.options.x
        y = self.options.y
        longitud = self.options.longitud

        #Configuración de coordenadas
        linea = 'M ' + str(x) + ',' + str(y) + ' L ' + str(x + longitud) + ',' + str(y) + ' L ' + str(x + longitud) + ',' + str(y + longitud) + ' L ' + str(x) + ',' + str(y + longitud) + ' Z '
        
        #Estilo de la línea
        style={'stroke': '#FF0000', 'stroke-width': '1', 'fill': 'none'}
        #Estilo aplicado, nombre del objeto y coordenadas
        drw = {'style': simplestyle.formatStyle(style), inkex.addNS('label', 'inkscape'):'objetoCaja', 'd':linea}
        #Generamos el objeto como hijo de la capa actual
        inkex.etree.SubElement(self.current_layer, inkex.addNS('path', 'svg'), drw)
        
# Crea una instancia de effect y la aplica.
effect = crearCaja()
effect.affect() 
