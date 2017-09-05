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

import sys, simplepath, inkex, re, subprocess
sys.path.append('/usr/share/inkscape/extensions')

#Pasamos como atributo un path y la funcion elimina el ultimo trazo
def eliminarUltimoTrazo (letra) :
    d = letra.get('d')
    d = simplepath.formatPath( simplepath.parsePath(d) )
    dd=re.split(r'(i?)M',d)                                                            #Separa la cadena que le pases por los caracteres indicados en la 1 parte
    dd=filter(None, dd)                                                                #Crea una lista de elementos sin nulos, ni ceros
    for i, stri in enumerate(dd):
        dds=re.split(r'\s',stri)
        if 'L' in dds[-2]:#..yval..z last, ..yval..L..xval.. second last
            dds.pop()
            lastList=re.split(r'L',dds[-1])
            dds[-1]=lastList[0]
        dd[i]=' '.join(dds)
    d='M'+'M'.join(dd)

    letra.set('d',d)
    
class singleLine(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        seleccionados = self.selected
        #En caso de que no se haya seleccionado nada se devolverá un error
        if seleccionados == {} :
            inkex.errormsg('No se ha seleccionado ningún elemento')
            error=1
            exit()
        for id, elemento in seleccionados.iteritems():
            
            ########
            #if elemento.tag == inkex.addNS('text','svg'):
            ########
            
            #Si es un path se elimnará el último trazo
            if elemento.tag == inkex.addNS('path','svg'):   #Entrará en caso de que sean un conjunto de paths
                eliminarUltimoTrazo(elemento)
            #Si es un grupo de paths se iterará dentro de este
            elif elemento.tag == inkex.addNS('g','svg'):    #Entrará si hay un grupo de paths
                for letra in elemento.iter() :
                    if letra.tag == inkex.addNS('path','svg'):
                        eliminarUltimoTrazo(letra)

# Create effect instance and apply it.
effect = singleLine()
effect.affect() 
