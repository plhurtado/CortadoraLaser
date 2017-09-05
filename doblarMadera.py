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

import sys, copy
import inkex, simpletransform
import simplestyle
import math

#Funcion que dibuja una linea en vertical con una longitud a partir de una coordenada
def draw_SVG_line( x1, y1, largura, altura, especial, sobrante, inverso):
    
    #Si vamos en sentido inverso
    if inverso :
        y2 = y1 - largura
        if y1 > altura + sobrante :

            y1 = altura + sobrante
        if y2 < 0 :
            y2 = -sobrante
        if y2 > y1 :
            return ""
    else :
        if y1 > altura :
            inkex.debug('hola')
            return ""
        if y1 + largura - altura < sobrante :
            y2 = y1 + largura
        else :
            y2 = altura + sobrante
        
        #Especial será la distancía a la que empezará la linea de las líneas impares
        if especial != None :
            y2 = y1 + especial
            y1 = - sobrante
        
        if y2 < y1 :
            return ""
    
    #Devolvemos el conjunto de puntos
    puntos = ' M ' + str(x1) + ',' + str(y1) + ' L ' + str(x1) + ',' + str(y2)
    return puntos

#Función utilizada para dibujar una caja que englobe el conjunto de lineas
def boxPoints(anchura, altura):

    puntos = 'M 0,0 ' + str(anchura) + ',0 ' + str(anchura) + ',' + str(altura) + ' 0,' + str(altura) + 'z'
    return puntos

class doblarMadera(inkex.Effect):
    
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option( '--unidad', action='store', type='string', dest='unidad', default='mm', help='Unit')
        self.OptionParser.add_option('--anchura', action='store', type='float', dest='anchura', help='Anchura del lineado')
        self.OptionParser.add_option('--altura', action='store', type='float', dest='altura', help='Height')
        self.OptionParser.add_option('--separacionHorizontal', action='store', type='float', dest='separacionHorizontal', help='Separacion horizontal entre lineas')
        self.OptionParser.add_option('--separacionVertical', action='store', type='float', dest='separacionVertical', help='Separacion vertical entre lineas')
        self.OptionParser.add_option('--larguraMaxima', action='store', type='float', dest='larguraMaxima', help='Largura máxima de las lineas')
        self.OptionParser.add_option('--marcasInicio', action='store', type='inkbool', dest='marcasInicio', help='Añadir marcas al inicio de cada linea')
        self.OptionParser.add_option('--grupo', action='store', type='inkbool', dest='grupo', help='Grupo que engloba a las lineas')
        self.OptionParser.add_option('--path', action='store', type='string', dest='path', default='unico', help='Estructura interna de paths')
        self.OptionParser.add_option('--caja', action='store', type='inkbool', dest='caja', help='Caja que engloba las lineas')
        self.OptionParser.add_option('--sobrante', action='store', type='float', dest='sobrante', help='Trozo de línea sobrante')
        self.OptionParser.add_option('--orden', action='store', type='string', dest='orden', default='igual', help='Orden en el que se dibujarán las líneas')
        
    
    def effect(self):
        unidad = str(self.options.unidad)
        anchura = self.unittouu(str(self.options.anchura) + unidad)
        altura = self.unittouu(str(self.options.altura) + unidad)
        separacionHorizontal = self.unittouu(str(self.options.separacionHorizontal) + unidad)
        separacionVertical = self.unittouu(str(self.options.separacionVertical) + unidad)
        larguraMaxima = self.unittouu(str(self.options.larguraMaxima) + unidad)
        marcasInicio = self.options.marcasInicio
        grupo = self.options.grupo
        path = self.options.path
        caja = self.options.caja
        sobrante = self.unittouu(str(self.options.sobrante) + unidad)
        orden = self.options.orden
        grosor = 0.1
        
        parent = self.current_layer

        if grupo: 
            parent = inkex.etree.SubElement(parent, 'g')
        
        columnas = int(anchura / ((grosor + separacionHorizontal))) + 1             #Numero de columnas (+1 para que llegue al tope)
        lineasPorColumna = int(math.ceil(altura/larguraMaxima)) + 1                 #Numero de filas por columna
        largura = altura / lineasPorColumna                                         #Longitud de las lineas
 
        style   = { 'stroke-width':grosor, 'stroke':'#000000' }                     #El estilo será negro

        #Si todos los puntos van en un unico path
        if path == 'unico':
            name = 'Lines'
            puntos = ''
            for x in range(0, columnas):
                #if marcasInicio:
                    #draw_SVG_line(x * separacionHorizontal, -3, 1, altura, None, sobrante, False)
                
                #Lineas en posiciones pares
                if x % 2 == 0:
                    posy = 0
                    for y in range(0, lineasPorColumna):
                        if x * separacionHorizontal + grosor < anchura :
                            puntos += draw_SVG_line(x * (separacionHorizontal + grosor), posy + y * (largura + separacionVertical), largura, altura, None, sobrante, False)
                #Lineas en posiciones impares
                else:
                    if orden == 'igual' :
                        posy = (largura + separacionVertical) / 2
            
                        #Con este incremeto tenemos en cuenta algunos casos en los que se necesita una linea mas
                        if altura > (largura + separacionVertical) * (lineasPorColumna -1) + largura / 2 + separacionVertical / 2:
                            incremento = 1
                        else :
                            incremento = 0
                        
                        for y in range(0, lineasPorColumna + incremento):
                            if x * separacionHorizontal + grosor < anchura :
                                if y == 0 :
                                    puntos += draw_SVG_line(x * (separacionHorizontal + grosor), y, largura, altura, posy - separacionVertical, sobrante, False)
                                else :
                                    puntos += draw_SVG_line(x * (separacionHorizontal + grosor), posy + (largura + separacionVertical) * (y - 1), largura, altura, None, sobrante, False)
                    else :
                        yInicio = (largura + separacionVertical) * lineasPorColumna - separacionVertical/2 + largura/2
                        if yInicio - largura > altura :
                            yInicio = (largura + separacionVertical) * lineasPorColumna - largura / 2 - 1.5 * separacionVertical
                        if altura >= (largura + separacionVertical) * (lineasPorColumna -1) + largura / 2 + separacionVertical / 2:
                            incremento = 1
                        else :
                            incremento = 0
                        
                        for y in range(0, lineasPorColumna + incremento) :
                            puntos += draw_SVG_line(x * (separacionHorizontal + grosor), yInicio - (largura + separacionVertical) * y, largura, altura, None, sobrante, True)
                            
            line_attribs = {'style' : simplestyle.formatStyle(style), inkex.addNS('label','inkscape') : name, 'd' : puntos}
            inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )
        #En el else tendremos en cuenta el caso en el que no todos los puntos vaya en un unico path
        else :
            name = 'Line'
            for x in range(0, columnas):
                if x % 2 == 0:
                    posy = 0
                    for y in range(0, lineasPorColumna):
                        if x * separacionHorizontal + grosor < anchura :
                            puntos = draw_SVG_line(x * (separacionHorizontal + grosor), posy + y * (largura + separacionVertical), largura, altura, None, sobrante, False)
                            line_attribs = {'style' : simplestyle.formatStyle(style), inkex.addNS('label','inkscape') : name, 'd' : puntos}
                            inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )
                else:
                    if orden == 'igual' :
                        posy = (largura + separacionVertical) / 2
                        
                        if altura > (largura + separacionVertical) * (lineasPorColumna -1) + largura / 2 + separacionVertical / 2:
                            incremento = 1
                        else :
                            incremento = 0
                            
                        for y in range(0, lineasPorColumna + incremento):
                            if x * separacionHorizontal + grosor < anchura :
                                if y == 0 :
                                    puntos = draw_SVG_line(x * (separacionHorizontal + grosor), y, largura, altura, posy - separacionVertical, sobrante, False)
                                    line_attribs = {'style' : simplestyle.formatStyle(style), inkex.addNS('label','inkscape') : name, 'd' : puntos}
                                    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )
                                else :
                                    puntos = draw_SVG_line(x * (separacionHorizontal + grosor), posy + (largura + separacionVertical) * (y - 1), largura, altura, None, sobrante, False)
                                    line_attribs = {'style' : simplestyle.formatStyle(style), inkex.addNS('label','inkscape') : name, 'd' : puntos}
                                    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )
                    else :
                        yInicio = (largura + separacionVertical) * lineasPorColumna - separacionVertical/2 + largura/2
                        
                        if yInicio - largura > altura :
                            yInicio = (largura + separacionVertical) * lineasPorColumna - largura / 2 - 1.5 * separacionVertical
                        if altura >= (largura + separacionVertical) * (lineasPorColumna -1) + largura / 2 + separacionVertical / 2:
                            incremento = 1
                        else :
                            incremento = 0
                            
                        for y in range(0, lineasPorColumna + incremento):

                            puntos = draw_SVG_line(x * (separacionHorizontal + grosor), yInicio - (largura + separacionVertical) * y, largura, altura, None, sobrante, True)
                            line_attribs = {'style' : simplestyle.formatStyle(style), inkex.addNS('label','inkscape') : name, 'd' : puntos}
                            inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )
        
        #En caso de que se quiera dibujar una caja contenedora llamaeremos a la función encargada
        if caja :
            style   = { 'stroke-width':'0.1', 'stroke':'#FF0000', 'fill':'none'}
            puntos = boxPoints(anchura, altura)
            line_attribs = {'style' : simplestyle.formatStyle(style), inkex.addNS('label','inkscape') : 'Box', 'd' : puntos}
            inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )

effect = doblarMadera()
effect.affect()
