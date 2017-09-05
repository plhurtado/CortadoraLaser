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

import sys, inkex, simplestyle, math
sys.path.append('/usr/share/inkscape/extensions')

class capaporcolor(inkex.Effect):

    def __init__(self):

        # Call the base class constructor.
        inkex.Effect.__init__(self)

    #Funcion que devuelva el color a partir de un estilo (el borde)
    @staticmethod
    def color(style):

        estilo = str(style)
        pos = estilo.find('stroke:#')
        if pos == -1 : 
            return 'Sin borde'
        color = estilo[pos+8:pos+14]

        return color

    #Devuelve el nombre del color mas cercano en el diccionario de colores
    @staticmethod
    def colorCercano(color, diferenciaMax) :
        cercano = []
        rgb = simplestyle.parseColor('#'+color)
        for key, value in simplestyle.svgcolors.iteritems() :

            rgbDiccionario = simplestyle.parseColor(value)
            diferencia = math.sqrt((rgbDiccionario[0]-rgb[0])**2 + (rgbDiccionario[1]-rgb[1])**2 + (rgbDiccionario[2]-rgb[2])**2)
            if diferencia < diferenciaMax :
                if cercano == [] :
                    cercano.append(key)
                    cercano.append(diferencia)
                elif  diferencia < cercano[1] :
                    cercano[0] = key
                    cercano[1] = diferencia
        
        if cercano == [] :
            return None
        else :
            return cercano[0]
    
    def effect(self):

        # Accedemos al arbol de elementos
        svg = self.document.getroot()

        #Se crea el diccionario y la lista de capas originales
        diccionario = {}        #Nombre de las capas que se van a crear con sus respectivos elementos
        capasOriginales = []    #Capas que borraremos
        gestionados = []        #Elementos gestionados para evitar gestionar las cajas3d
        diferenciaMax = 30      #Diferencia máxima entre colores para asignar un nombre
         
        #Miramos los grupos antes de nada
         
        for objeto in svg.iter() :
            
            style = objeto.get('style') #Cogemos el estilo del elemento
            
            if objeto not in gestionados :
                
                if objeto.tag == '{http://www.w3.org/2000/svg}g' :                                              #Grupos 
                    if (objeto.get(inkex.addNS('groupmode', 'inkscape')) == 'layer') == False :                 #Capas
                        if (objeto.get(inkex.addNS('type', 'sodipodi')) == 'inkscape:box3d') == False :         #Cajas3d
                            #Comprobamos si todos los elementos del grupo son del mismo color de borde para no deshacer el grupo
                            todosIguales = True
                            color = None
                            for hijo in objeto.getchildren() :
                                colorPropio = self.color(hijo.get('style'))
                                if color == None :
                                    color = colorPropio
                                elif colorPropio != color :
                                    todosIguales = False
                                    break
                            if todosIguales :
                                for hijo in objeto.getchildren() :
                                    gestionados.append(hijo)
                                
                                rgb = simplestyle.parseColor(color)
                                colorDiccionario = self.colorCercano(color, diferenciaMax)
                                if colorDiccionario != None :
                                    nombre = colorDiccionario
                                else :
                                    nombre = color
                    
                                #Si el color no existe creamos una entrada en el diccionario
                                if nombre not in diccionario:
                                    lista = []
                                    diccionario[nombre] = lista
                                    
                                #Añadimos el elemento a la entrada de su color
                                diccionario[nombre].append(objeto)
                                    
                        else :
                            #Creamos una entrada en el diccionario para crear las capa de Cajas3d con sus elementos
                            if 'Cajas3d' not in diccionario:
                                lista=[]
                                diccionario['Cajas3d'] = lista
                            diccionario['Cajas3d'].append(objeto)
                            for hijo in objeto.getchildren() :
                                gestionados.append(hijo)
                    #Guardamos las capas originales para eliminarlas
                    else :
                        capasOriginales.append(objeto)

                #En caso de que sea cualquier otro objeto analizamos su color de borde
                elif style != None :
                    
                    #Cogemos el color del objeto
                    color = self.color(style)

                    #En colorDiccionario se guardará el nombre del color y la distancia a la que está
                    colorDiccionario = self.colorCercano(color, diferenciaMax)
                    if colorDiccionario != None :
                        nombre = colorDiccionario
                    else :
                        nombre = color
                    
                    #Si el color no existe creamos una entrada en el diccionario
                    if nombre not in diccionario:
                        lista = []
                        diccionario[nombre] = lista
                        
                    #Añadimos el elemento a la entrada de su color
                    diccionario[nombre].append(objeto)                    
        
        #Eliminamos las capas originales
        for capas in capasOriginales:
            capas.getparent().remove(capas)
            
        #Creamos una nueva capa por cada clave del diccionario
        for key, value in diccionario.iteritems() :
            capa = inkex.etree.Element("g")
            capa.set(inkex.addNS('label', 'inkscape'), '%s' % (key))
            capa.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
            
            #Añadimos cada uno de los elementos de la lista a su color
            for i in value:
                capa.append(i)
            
            #Colgamos la capa creada de la raiz
            svg.append(capa)

# Create effect instance and apply it.
effect = capaporcolor()
effect.affect() 
