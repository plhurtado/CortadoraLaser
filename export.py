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

import sys, inkex, subprocess, re
sys.path.append('/usr/share/inkscape/extensions')
   
class export(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        
        #Guardamos los parametros pasados desde la interfaz
        self.OptionParser.add_option("--tab", action="store", type="string", dest="tab")
        self.OptionParser.add_option('--path', action = 'store', type = 'string', dest = 'path', default = '/tmp/', help = 'Ruta donde se guardarán los ficheros EPS')
        self.OptionParser.add_option('--opacity', action = 'store', type = 'inkbool', dest = 'opacity', help = 'Configurar todas las oacidades al máximo')
        self.OptionParser.add_option('--fill', action = 'store', type = 'inkbool', dest = 'fill', help = 'Borrar el relleno de todas las piezas')
        self.OptionParser.add_option('--text', action = 'store', type = 'inkbool', dest = 'text', help = 'Pasar los objetos de texto a path')

    def effect(self):
        
        #Parametros que se le pasa a la linea de comando
        INKSCAPE_WITHOUT_GUI = "--without-gui"
        INKSCAPE_EXPORT_EPS = "--export-eps"
        INKSCAPE_EXPORT_ID = "--export-id"
        INKSCAPE_EXPORT_AREA_DRAWING = "--export-area-drawing"
        INKSCAPE_EXPORT_FILTERS = "--export-ignore-filters"
        #En caso de que se pasen los textos a path
        INKSCAPE_EXPORT_TEXT = "--export-text-to-path"

        #Guardamos en svg el elemento raiz de donde cuelgan todas las figuras, clases, etc
        svg = self.document.getroot()
        
        #Si se quiere eliminar el relleno o poner la opacidad a 100% recorremos todos los elementos buscando las figuras
        if self.options.opacity or self.options.fill :
            for objeto in svg.iter() :
                #Comprobamos que sea una pieza
                if objeto.tag == inkex.addNS('text','svg') or objeto.tag == inkex.addNS('path','svg') or objeto.tag == inkex.addNS('ellipse','svg') or objeto.tag == inkex.addNS('rect','svg') or objeto.tag == inkex.addNS('circle','svg') or objeto.tag == inkex.addNS('line','svg') or objeto.tag == inkex.addNS('polygon','svg') or objeto.tag == inkex.addNS('polyline','svg'):
                    
                    estilo = objeto.get('style')
                    
                    #Si queremos poner al 100% la opacidad del borde
                    if self.options.opacity :
                        pos = estilo.find('stroke-opacity:')
                        if pos != -1 :
                            if estilo[pos + 15] != "1" :
                                final = estilo[:pos + 15] + "1"
                                aux = estilo[pos:].rfind(";") + pos
                                if aux > pos :
                                    final = final + estilo[aux:]
                                estilo = final
                    #Si queremos eliminar el relleno de las figuras
                    if self.options.fill :
                        pos = estilo.find('fill:')
                        if pos != -1 :
                            if estilo [pos + 5] != "n" :
                                final = estilo[:pos + 5] + "none"
                                aux = estilo[pos:].find(";") + pos
                                if aux > pos : 
                                    final = final + estilo[aux:]
                                estilo = final
                                #Se notificará al usuario en caso de que haya un texto al que quitarle el relleno
                                if objeto.tag == inkex.addNS('text','svg'):
                                    inkex.debug('Hay un elemento de texto al que se le quitará el relleno, si no tiene relleno se hará invisible')
                    objeto.set('style', estilo)

        #Ruta absoluta del archivo svg
        svg_file_path = self.args[-1]

        for objeto in svg.iter():
            #En caso de que tengamos una capa
            if objeto.tag == inkex.addNS('g','svg') and objeto.get(inkex.addNS('groupmode', 'inkscape')) == 'layer':  
                #Ruta de destino de los archivos .eps (se pondrá de nombre de archivo el nombre de las capas)
                dest = self.options.path + objeto.get(inkex.addNS('label', 'inkscape')) + '.eps'

                #Si vamos a pasar los textos a path tendremos que añadir un parámetro mas
                if self.options.text :
                    parameters = [
                            "inkscape",
                            INKSCAPE_WITHOUT_GUI,
                            INKSCAPE_EXPORT_EPS, dest,
                            INKSCAPE_EXPORT_ID, objeto.get('id'),
                            INKSCAPE_EXPORT_AREA_DRAWING,
                            INKSCAPE_EXPORT_FILTERS,
                            INKSCAPE_EXPORT_TEXT,
                            svg_file_path,
                    ]
                else :
                    parameters = [
                            "inkscape",
                            INKSCAPE_WITHOUT_GUI,
                            INKSCAPE_EXPORT_EPS, dest,
                            INKSCAPE_EXPORT_ID, objeto.get('id'),
                            INKSCAPE_EXPORT_AREA_DRAWING,
                            INKSCAPE_EXPORT_FILTERS,
                            svg_file_path,
                    ]
                #Llamada a la linea de comandos
                p = subprocess.Popen(parameters,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                (stdoutdata, stderrdata) = p.communicate()
                p.stdout.close()
                p.stdin.close()
                p.stderr.close()
        
effect = export()
effect.affect() 
