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

import sys, inkex, simplestyle, random
sys.path.append('/usr/share/inkscape/extensions')

class colorporcapa(inkex.Effect):

    def __init__(self):

        # Call the base class constructor.
        inkex.Effect.__init__(self)
        
        self.OptionParser.add_option("--tab",
            action="store", type="string",
            dest="tab")
        self.OptionParser.add_option('--removeLayers', action = 'store',
          type = 'inkbool', dest = 'removeLayers', default = 'False',
          help = 'Marcar en caso de que se quieran eliminar todas las capas tras aplicar el color')

    #Funcion que devuelva el color de un estilo (el borde)
    @staticmethod
    def cambioColor(estilo, color):

        estilo = str(estilo)
        color = str(color)
        pos = estilo.find('stroke:')
        if pos == -1 : 
            return 'Sin borde'
        final = estilo[0:pos+7] + color + estilo[pos+14:]
        return final

    @staticmethod
    def colorAleatorio() :
        r = lambda: random.randint(0,255)
        return('#%02X%02X%02X' % (r(),r(),r()))
        
    def effect(self):

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()
        
        # Get script's "--what" option value.
        removeLayers = self.options.removeLayers

        #Lista con los colores ya utilizados
        coloresUsados =[]
         
        #Buscamos todos los nodos de capas
        capas = svg.findall('{http://www.w3.org/2000/svg}g')
        
        #En caso de que no haya ninguna capa en nuestro proyecto se mostrará un mensaje de error y se terminará la ejecución.
        if capas == [] :
            inkex.errormsg('No hay ninguna capa para aplicarle un color')
            error=1
            exit()
        
        if removeLayers :
            unica = inkex.etree.Element("g")
            unica.set(inkex.addNS('label', 'inkscape'), 'Unica')
            unica.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
            svg.append(unica)
        
        
        for capa in capas :
            cambiarNombre = False
            nombreCapa = (capa.get(inkex.addNS('label', 'inkscape'))).lower()
            if nombreCapa in simplestyle.svgcolors:
                color = simplestyle.svgcolors[nombreCapa]
            else :
                nombreColor = random.choice(simplestyle.svgcolors.keys())
                color = simplestyle.svgcolors[nombreColor]
                cambiarNombre = True
                
            #En caso de que ya exista cambiamos el color
            while (color in coloresUsados):
                nombreColor = random.choice(simplestyle.svgcolors.keys())
                color = simplestyle.svgcolors[nombreColor]

            #Lo añadimos a la lista de colores utilizados para que no se repitan
            coloresUsados.append(color)
            
            if cambiarNombre :
                
                pos = nombreCapa.find('+')
                if pos != -1 : 
                    nombreCapa = nombreCapa [:pos-1]
                nombreCapa = nombreCapa + ' + ' + nombreColor
                capa.set(inkex.addNS('label', 'inkscape'), '%s' % (nombreCapa))
            
            hijos = capa.getchildren()
            
            for hijo in hijos :
                if hijo.tag != '{http://www.w3.org/2000/svg}g' :
                    
                    #Si se van a eliminar las capas se colgará el hijo del nodo raiz para que no se pierda
                    if removeLayers == True:
                        nombreCapa = 'Unica' 
                        unica.set(inkex.addNS('label', 'inkscape'), '%s' % (nombreCapa))
                        unica.append(hijo)
                    
                    estilo = self.cambioColor(hijo.get('style'), color)
                    hijo.set('style', estilo)

            #Eliminamos todas las capas si lo ha solicitado el usuario
            if removeLayers == True :
                capa.getparent().remove(capa)

# Create effect instance and apply it.
effect = colorporcapa()
effect.affect() 
