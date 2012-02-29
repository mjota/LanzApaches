#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# LanzApaches - Lanzador de comandos ab para AESI
# Copyright (c) 2011 - Manuel Joaquin Díaz Pol
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
#==============================================================================
#

import commands
import random
from gi.repository import Gtk
from gi.repository import Notify
import threading


class main:
    def __init__(self):
        #Crea la ventana de trabajo principal y obtiene los objetos en Glade
        builder = Gtk.Builder();
        builder.add_from_file("ventana.glade")
        
        dict = {"on_Salir_Clicked": self.Salir,
                "on_Test_Clicked": self.Test,
                "on_pruebas_clicked": self.Pruebas,
                "on_click_about": self.Acerca}
        
        builder.connect_signals(dict)
        
        self.textoResultado1 = builder.get_object("textview1")
        self.textoTiempos = builder.get_object("textview2")
        self.textoProd = builder.get_object("textview3")
        self.entryCargas1 = builder.get_object("entry1")
        self.entryCargas2 = builder.get_object("entry2")
        self.entryCargas3 = builder.get_object("entry3")
        self.entryDir1 = builder.get_object("entry4")
        self.entryDir2 = builder.get_object("entry5")
        self.entryDir3 = builder.get_object("entry6")
        self.entryNLanz = builder.get_object("entry7")
        self.resultlist = builder.get_object("liststore1")
        self.about = builder.get_object("aboutdialog1")
        
        self.Inicia()
        Notify.init("LanzApaches")
    
    #Inicializa las listas
    def Inicia(self):
        self.Trequest=[]  
        self.Prod=[]
        self.Peso=[]        
        
    #Salir
    def Salir(self,widget):    
        Gtk.main_quit()
    
    #Lanza ventana about 
    def Acerca(self,widget):
        self.about.run()
        self.about.hide()
    
    #Botón de pruebas
    def Pruebas(self,widget):
        t1 = threading.Thread(target=self.Test)
        t1.start()
        #t1.join()
    
    #Recoge los datos y los calcula
    def Test(self,widget):
        #Muestra notificación de inicio
        Notif = Notify.Notification.new ("LanzApaches","Se ha iniciado el lanzamiento de comandos AB","dialog-information")
        Notif.show()
        
        #Recoge los datos de las entradas
        a = float(self.entryCargas1.get_buffer().get_text())
        b = float(self.entryCargas2.get_buffer().get_text())
        c = float(self.entryCargas3.get_buffer().get_text())
        tpx = int(self.entryNLanz.get_buffer().get_text())
        
        #Asigna un peso a cada carga
        tot = a+b+c
        a = int((tpx/tot)*a)
        b = int(((tpx/tot)*b)+a)
        c = int(((tpx/tot)*c)+b)
                
        #Realiza el lanzamiento de cargas de forma aleatoria, añade el peso correspondiente a la lista
        for n in range(tpx):
            ran = random.randint(0,c)
            if (ran<=a):
                self.Lanzador(self.entryDir1.get_buffer().get_text())
                self.Peso.append((float(a)/float(tpx)))
            elif (ran<=b):
                self.Lanzador(self.entryDir2.get_buffer().get_text())
                self.Peso.append(float(b-a)/float(tpx))
            else:
                self.Lanzador(self.entryDir3.get_buffer().get_text())
                self.Peso.append(float(c-b)/float(tpx))
    
        #Media aritmética de tiempos de respuesta
        TotReq = 0.0
        for el in self.Trequest:
            TotReq = TotReq + el
        FinalR = TotReq / tpx
        
        #Media aritmética de tiempos de respuesta ponderada
        TotReqPon = 0.0
        n = 0
        for el in self.Trequest:
            TotReqPon = TotReqPon + el * self.Peso[n]
            n+=1
        
        #Media armónica de productividad
        TotProd = 0.0
        for el in self.Prod:
            TotProd = TotProd + (1/el)
        FinalP = tpx / TotProd
        
        #Desviación típica de tiempos de respuesta
        DesvT = 0.0
        for el in self.Trequest:
            DesvT = (el-FinalR)**2 + DesvT
        DesvT = (DesvT/tpx)**0.5
        
        #Desviación típica de productividad
        DesvP = 0.0
        for el in self.Prod:
            DesvP = (el-FinalP)**2 + DesvP
        DesvP = (DesvP/tpx)**0.5
        
        #Carga los resultados en la tabla
        self.resultlist.append(["Tiempo de respuesta total: " + str(TotReq/1000) + " s"])
        self.resultlist.append(["Número de peticiones: " + str(tpx)])
        self.resultlist.append(["Tiempo de respuesta medio: " + str(FinalR)+ " ms"] )
        self.resultlist.append(["Tiempo de respuesta ponderado: " + str(TotReqPon) + " ms"])
        self.resultlist.append(["Desviación típica de tiempo de respuesta: " + str(DesvT) + " ms"])
        self.resultlist.append(["Productividad: " + str(FinalP) + " pet/sec" ])
        self.resultlist.append(["Desviación típica de productividad: " + str(DesvP) + " pet/sec"])

        #Muestra notificación de final
        Notif.update("LanzApaches","Finalizado el lanzamiento de comandos AB","dialog-information")
        Notif.show()
        
        #Añade los tiempos y productividad a las pestañas
        self.textoTiempos.get_buffer().set_text('\n'.join(map(str , self.Trequest)))
        self.textoProd.get_buffer().set_text('\n'.join(map(str , self.Prod)))
        
        self.Inicia()
    
    #Realiza el lanzamiento individual y guarda los resultados en listas   
    def Lanzador(self,link):
                
        Comando = "ab -k -n 1 " + link
        result = commands.getoutput(Comando)
        self.textoResultado1.get_buffer().set_text(result)
        
        tupla = result.split("Requests per second:    ")
        tupla = tupla[1].split(" [#/sec]")
        self.Prod.append(float(tupla[0])) 
        
        tupla = tupla[1].split("Time per request:       ")
        tupla = tupla[1].split(" [ms]")
        self.Trequest.append(float(tupla[0]))  
         

if __name__ == '__main__':
    main()
    Gtk.main()

    