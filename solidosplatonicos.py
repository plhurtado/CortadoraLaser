#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Pedro Hurtado González

import sys, simplestyle, inkex, math
sys.path.append('/usr/share/inkscape/extensions')

#Conversor entre rgb y exadecimal
def rgbToHex(r,g,b):
        return '%02x%02x%02x' % (int(round(r)),int(round(g)),int(round(b)))

#Este método nos permite crear una pestaña a partir de la coordenada facilitada con la configuración pasada como parámetros
def creadorPestana (x1, y1, grado, grosor, anchoPestana):

    
    x3 = math.cos(math.radians(grado-90)) * grosor + x1
    y3 = math.sin(math.radians(grado-90)) * grosor + y1
            
    x4 = math.cos(math.radians(grado-0)) * anchoPestana + x3
    y4 = math.sin(math.radians(grado-0)) * anchoPestana + y3
            
    x5 = math.cos(math.radians(grado+90)) * grosor * 2 + x4
    y5 = math.sin(math.radians(grado+90)) * grosor * 2 + y4
    
    x6 = math.cos(math.radians(grado-0)) * anchoPestana + x5
    y6 = math.sin(math.radians(grado-0)) * anchoPestana + y5
    
    x7 = math.cos(math.radians(grado-90)) * grosor + x6
    y7 = math.sin(math.radians(grado-90)) * grosor + y6
    
    resultado = (' L ' + str(x3) + ',' + str(y3) + ' L ' + str(x4) + ',' + str(y4) + ' L ' + str(x5) + ',' + str(y5) + ' L ' + str(x6) + ',' + str(y6) + ' L ' + str(x7) + ',' + str(y7))

    return resultado

#Crea las paredes de un polígono a partir del punto señalado, con la longitud y numero de pestañas indicado
def creadorLado (x1, y1, longitud, grado, grosor, anchoPestana, numPestana):
    
    resultado = []
    
    #Guardamos los puntos finales antes de crear nuevas coordenadas
    xfin = (math.cos(math.radians(grado)) * longitud) + x1
    yfin = (math.sin(math.radians(grado)) * longitud) + y1
    
    cadena = ''
    
    #Entramos en el bucle tantas veces como pestañas tenga nuestra figura
    i = 1
    while i <= numPestana:
        #Buscamos el punto donde empezamos la pestaña
        x2 = math.cos(math.radians(grado)) * ((longitud/(numPestana+1) * i) - anchoPestana) + x1
        y2 = math.sin(math.radians(grado)) * ((longitud/(numPestana+1) * i) - anchoPestana) + y1
        
        p = creadorPestana(x2, y2, grado, grosor, anchoPestana)
        cadena += ' L ' + str(x2) + ',' + str(y2) + p
        
        i+=1
    
    
    cadena += ' L ' + str(xfin) + ',' + str(yfin)
            
    resultado.append(cadena)
    resultado.append(xfin)
    resultado.append(yfin)
    return resultado

def creadorTriangulo (x1, y1, longitud, grado, grosor, anchoPestana, numPestana, isCalado, distanciaCalado):
            
    #Configuración de las coordenadas del polígono
    linea = 'M ' + str(x1) + ',' + str(y1)
    s = creadorLado (x1, y1, longitud, grado, grosor, anchoPestana, numPestana)                   #Primer trazo
    linea += s[0]
    s = creadorLado (s[1], s[2], longitud, grado -120, grosor, anchoPestana, numPestana)          #Segundo trazo
    linea += s[0]
    s = creadorLado (s[1], s[2], longitud, grado -(120*2), grosor, anchoPestana, numPestana)      #Tercer trazo
    linea += s[0] + ' Z ' 
    
    if isCalado == True:
        
        longitudInterna = longitud - 2 * distanciaCalado/(math.tan(math.radians(30)))
        
        if grado == 0 :
            x = x1 + distanciaCalado/(math.tan(math.radians(30))) 
            y =  (y1 - distanciaCalado)
        else :
            x = x1
            y = (y1 - (math.sqrt(distanciaCalado ** 2 + (distanciaCalado/(math.tan(math.radians(30)))) ** 2)))

        linea += 'M ' + str(x) + ',' + str(y) 
        s = creadorLado (x, y, longitudInterna, grado, 0, 0, 0)                         #Primer trazo
        linea += s[0]
        s = creadorLado (s[1], s[2], longitudInterna, grado -120, 0, 0, 0)              #Segundo trazo
        linea += s[0]
        s = creadorLado (s[1], s[2], longitudInterna, grado -(120*2), 0, 0, 0)          #Tercer trazo
        linea += s[0] + ' Z ' 
    
    return linea

def creadorCuadrado (x1, y1, longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado):
    
    linea = 'M ' + str(x1) + ',' + str(y1)
    s = creadorLado (x1, y1, longitud, 0, grosor, anchoPestana, numPestana)                 #Primer trazo
    linea += s[0]
    s = creadorLado (s[1], s[2], longitud, -90, grosor, anchoPestana, numPestana)         #Segundo trazo
    linea += s[0]   
    s = creadorLado (s[1], s[2], longitud, -(90*2), grosor, anchoPestana, numPestana)     #Tercer trazo
    linea += s[0]                                                              
    s = creadorLado (s[1], s[2], longitud, -(90*3), grosor, anchoPestana, numPestana)     #Cuarto trazo
    linea += s[0] + ' Z '
    
    if isCalado == True:
        x = x1 + distanciaCalado
        y = y1 - distanciaCalado
        linea += 'M ' + str(x) + ',' + str(y) 
        
        longitudInterna = longitud - 2 * distanciaCalado
        s = creadorLado (x, y, longitudInterna, 0, 0, 0, 0)                 #Primer trazo
        linea += s[0]
        s = creadorLado (s[1], s[2], longitudInterna, -90, 0, 0, 0)         #Segundo trazo
        linea += s[0]   
        s = creadorLado (s[1], s[2], longitudInterna, -(90*2), 0, 0, 0)     #Tercer trazo
        linea += s[0]                                                              
        s = creadorLado (s[1], s[2], longitudInterna, -(90*3), 0, 0, 0)     #Cuarto trazo
        linea += s[0] + ' Z '
    
    return linea

def creadorPentagono (x1, y1, longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado):
    
    linea = 'M ' + str(x1) + ',' + str(y1)
    s = creadorLado (x1, y1, longitud, 0, grosor, anchoPestana, numPestana)                 #Primer trazo
    linea += s[0]
    s = creadorLado (s[1], s[2], longitud, -72, grosor, anchoPestana, numPestana)         #Segundo trazo
    linea += s[0]
    s = creadorLado (s[1], s[2], longitud, -(72*2), grosor, anchoPestana, numPestana)     #Tercer trazo
    linea += s[0]
    s = creadorLado (s[1], s[2], longitud, -(72*3), grosor, anchoPestana, numPestana)     #Cuarto trazo
    linea += s[0]           
    s = creadorLado (s[1], s[2], longitud, -(72*4), grosor, anchoPestana, numPestana)     #Quinto trazo 
    linea += s[0] + ' Z '
    
    if isCalado == True:
        x = x1 + distanciaCalado/(math.tan(math.radians(54)))
        y = y1 - distanciaCalado
        linea += 'M ' + str(x) + ',' + str(y) 
        
        
        
        longitudInterna = longitud - 2 * (distanciaCalado/math.tan(math.radians(54)))        
        
        s = creadorLado (x, y, longitudInterna, 0, 0, 0, 0)                 #Primer trazo
        linea += s[0]
        s = creadorLado (s[1], s[2], longitudInterna, -72, 0, 0, 0)         #Segundo trazo
        linea += s[0]   
        s = creadorLado (s[1], s[2], longitudInterna, -(72*2), 0, 0, 0)     #Tercer trazo
        linea += s[0]                                                              
        s = creadorLado (s[1], s[2], longitudInterna, -(72*3), 0, 0, 0)     #Cuarto trazo
        linea += s[0] 
        s = creadorLado (s[1], s[2], longitudInterna, -(72*4), 0, 0, 0)     #Cuarto trazo
        linea += s[0] + ' Z '
    
    return linea




def creadorSolidoTriangulo (longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado, distribucion, numero):
    
    lista = []
    
    x = 0
    y = 0
    
    if distribucion == "lineal" :
        i = 0
        while (i < numero) :
            if i%2 == 0 :
                puntos = creadorTriangulo(x, y, longitud, 0, grosor, anchoPestana, numPestana, isCalado, distanciaCalado)
                x += longitud + grosor * 2
            else :
                puntos = creadorTriangulo(x, y, longitud, -60, grosor, anchoPestana, numPestana, isCalado, distanciaCalado)
                x += grosor * 3
            lista.append(puntos)
            i+=1
    else :
        if numero == 4 :
            filas = 2
            columnas = 2
        elif numero == 8 :
            filas = 4
            columnas = 2
        else :
            filas = 5
            columnas = 4
        par = True    
        i = 0
        while (i < filas) :
            x = 0
            j = 0
            while (j < columnas) :
                if par :
                    puntos = creadorTriangulo(x, y, longitud, 0, grosor, anchoPestana, numPestana, isCalado, distanciaCalado)
                    x += longitud + grosor * 2
                    par = False
                else :
                    puntos = creadorTriangulo(x, y, longitud, -60, grosor, anchoPestana, numPestana, isCalado, distanciaCalado)
                    x += grosor * 3
                    par = True
                lista.append(puntos)
                j += 1
            y += longitud
            i += 1

    return lista
    
def creadorSolidoCuadrado (longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado, distribucion, separacion):
    
    lista = []
    
    x = 0
    y = 0
    
    if distribucion == "lineal" :
        
        i = 0
        while (i < 6) :
            puntos = creadorCuadrado (x, y, longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado)
            x += longitud + grosor*2 + separacion
            lista.append(puntos)
            i += 1
        
    else :
        i = 0
        j = 0
        while (i < 3) :
            j = 0
            x = 0
            while (j < 2) :
                puntos = creadorCuadrado (x, y, longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado)
                x += longitud + grosor*2 + separacion
                lista.append(puntos)
                j += 1
            y += longitud + grosor * 2 + separacion 
            i += 1
    return lista
def creadorSolidoPentagono (longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado, distribucion):
    lista = []
    
    x = 0
    y = 0
    
    if distribucion == "lineal" :
        
        i = 0
        while (i < 12) :
            puntos = creadorPentagono (x, y, longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado)
            x += 2 * longitud
            lista.append(puntos)
            i += 1
        
    else :
        i = 0
        j = 0
        while (i < 4) :
            j = 0
            x = 0
            while (j < 3) :
                puntos = creadorPentagono (x, y, longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado)
                x += 2 * longitud
                lista.append(puntos)
                j += 1
            y += 2 * longitud
            i += 1
    return lista





#En caso de error
def errorArg (mensaje):
    inkex.errormsg(mensaje)
    error=1
    exit()

class solidosplatonicos(inkex.Effect):

    def __init__(self):

        # Call the base class constructor.
        inkex.Effect.__init__(self)
        
        #Recuperamos los parametros pasados desde la interfaz
        self.OptionParser.add_option("--tab",
            action="store", type="string",
            dest="tab")
        self.OptionParser.add_option("--unidad",
            action="store", type="string",
            dest="unidad", default='mm', help="Unidad que utilizada por el usuario")
        self.OptionParser.add_option("--figura",
            action="store", type="string",
            dest="figura", default='Hexaedro', help="Figura que queremos dibujar")
        self.OptionParser.add_option("--unico",
            action="store", type="inkbool",
            dest="unico", help="Se marcará esta casilla en caso de querer que solo se imprima una unica pieza")
        self.OptionParser.add_option("--longitud",
            action="store", type="float",
            dest="longitud", help="Longitud de los lados de las caras")
        self.OptionParser.add_option("--pestana",
            action="store", type="float",
            dest="pestana", help="Anchura de la pestaña")
        self.OptionParser.add_option("--grosor",
            action="store", type="float",
            dest="grosor", help="Grosor del material que utilizaremos para la largura de las pestañas")
        self.OptionParser.add_option("--numPestana",
            action="store", type="float",
            dest="numPestana", help="Posicion de las pestañas")
        self.OptionParser.add_option("--separacion", 
            action="store", type="float",
            dest="separacion", help ="Separación entre las piezas en el tablero")
        self.OptionParser.add_option("--isCalado",
            action="store", type="inkbool",
            dest="isCalado", default="false")
        self.OptionParser.add_option("--distribucion",
            action="store", type="string",
            dest="distribucion", default='rectangular', help="Distribución de las piezas por el tablero")
        self.OptionParser.add_option("--caladoValor",
            action="store", type="float",
            dest="distanciaCalado", help="Anchura de las paredes internas de la figura")
        self.OptionParser.add_option("--grupo",
            action="store", type="inkbool",
            dest="grupo", help="Se creará un grupo de donde cuelgue el sólido platónico generado")
        self.OptionParser.add_option("--s_r",
            action="store", type="float",
            dest="s_r")
        self.OptionParser.add_option("--s_g",
            action="store", type="float",
            dest="s_g")
        self.OptionParser.add_option("--s_b",
            action="store", type="float",
            dest="s_b")
        self.OptionParser.add_option("--th",
            action="store", type="float",
            dest="th")    
    
    def effect(self):

        # Guardamos el arbol en svg
        svg = self.document.getroot()
        
        #Guardamos las variables para poder trabajar con ellas.
        
        unidad = str(self.options.unidad)
        figura=self.options.figura
        unico=self.options.unico
        longitud=self.unittouu(str(self.options.longitud) + unidad)
        anchoPestana=self.unittouu(str(self.options.pestana) + unidad)
        grosor=self.unittouu(str(self.options.grosor) + unidad)
        numPestana=self.unittouu(str(self.options.numPestana))
        separacion=self.unittouu(str(self.options.separacion) + unidad)
        isCalado=self.options.isCalado
        distribucion=self.options.distribucion
        distanciaCalado=self.unittouu(str(self.options.distanciaCalado) + unidad)
        grupo=self.options.grupo
        red=self.options.s_r
        green=self.options.s_g
        blue=self.options.s_b
        trazo=self.unittouu(str(self.options.th) + unidad)

        #Control de posibles errores    
        
        if anchoPestana  > longitud :
            errorArg ('Las pestañas no pueden ser mas anchas que el lado')
        elif isCalado == True and distanciaCalado <= grosor :
            errorArg ('Las paredes internas deverán ser mas grandes que el grosor del material')
        elif (anchoPestana*2) * (numPestana +1) > longitud :
            errorArg ('No caben tantas pestañas en los laterales de las piezas')
            
        
        #Configuramos los valores de estilo y metemos las coordenadas de las figuras en d. Creamos el objeto dentro de la capa con la que estemos trabajando
        color = '#' + str(rgbToHex(red,green,blue))
        style={'stroke': color, 'stroke-width': trazo, 'fill': 'none'}
        
        puntos = []
        
        if figura == "Hexaedro" :
            
            #Ponemos como nombre la figura básica
            name = 'cuadrado'

            if unico == 1 :
                puntos.append(creadorCuadrado(0, 0, longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado))
            else :
                puntos = creadorSolidoCuadrado(longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado, distribucion, separacion)
            
        elif figura == "Tetraedro" or figura == "Octaedro" or figura == "Icosaedro":
            
            apotema = (math.sqrt(3) / 6) * longitud;
            if apotema < distanciaCalado :
                errorArg('La distancia de calado no puede ser mayor que el apotema del triangulo')
            
            ##Ponemos como nombre la figura básica
            name = 'triangulo'

            if unico == 1 :
                puntos.append(creadorTriangulo(0, 0, longitud, 0, grosor, anchoPestana, numPestana, isCalado, distanciaCalado))
            else : 
                if figura == "Tetraedro" :
                    numero = 4
                elif figura == "Octaedro" :
                    numero = 8
                else :
                    numero = 20
                puntos = creadorSolidoTriangulo(longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado, distribucion, numero)
  
        elif figura == "Dodecaedro" :
            
            #Ponemos como nombre la figura básica
            name = 'pentagono'
            
            if unico == 1 :
                puntos.append(creadorPentagono(0, 0, longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado))
            else :
                puntos = creadorSolidoPentagono(longitud, grosor, anchoPestana, numPestana, isCalado, distanciaCalado, distribucion)

        if grupo :
            
            objetoGrupo = inkex.etree.Element("g")
            self.current_layer.append(objetoGrupo)
            contenedor = objetoGrupo
        else :
            contenedor = self.current_layer
        
        for d in puntos :
            drw = {'style': simplestyle.formatStyle(style), inkex.addNS('label', 'inkscape'):name, 'd': d}
            inkex.etree.SubElement(contenedor, inkex.addNS('path', 'svg'), drw)

# Create effect instance and apply it.
effect = solidosplatonicos()
effect.affect() 
