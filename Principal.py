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
import time

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
        self.textoResultado2 = builder.get_object("textview2")
        self.textoResultado3 = builder.get_object("textview3")
        self.textoFinal = builder.get_object("textview4")
        self.entryCargas1 = builder.get_object("entry1")
        self.entryCargas2 = builder.get_object("entry2")
        self.entryCargas3 = builder.get_object("entry3")
        self.entryDir1 = builder.get_object("entry4")
        self.entryDir2 = builder.get_object("entry5")
        self.entryDir3 = builder.get_object("entry6")
        self.resultlist = builder.get_object("liststore1")
        self.about = builder.get_object("aboutdialog1")
        
        self.Trequest=[]  
        self.Prod=[]
        
        Notify.init("LanzApaches")
        
    def Salir(self,widget):    
        Gtk.main_quit()
        
    def Acerca(self,widget):
        self.about.run()
        self.about.hide()
    
    def Pruebas(self,widget):
        Notif = Notify.Notification.new ("LanzApaches","Se ha iniciado el lanzamiento de comandos AB","dialog-information")
        Notif.show()
        print self.entryCargas1.get_buffer().get_text()
        print self.entryCargas2.get_buffer().get_text()
        print self.entryCargas3.get_buffer().get_text()
        print self.entryDir1.get_buffer().get_text()
        print self.entryDir2.get_buffer().get_text()
        print self.entryDir3.get_buffer().get_text()
        time.sleep(3)
        #self.Lanzador("http://130.206.134.121/carga1.php")
        #self.Lanzador("http://130.206.134.121/carga1.php")
        
        #TotReq = 0.0
        #for el in self.Trequest:
        #TotReq = TotReq + el
        #print TotReq
        self.resultlist.append(["Hola"])
        self.resultlist.append(["Adios"])
        self.resultlist.append(["Denuevo"])
        self.resultlist.append(["Ycuatro"])
        #self.textoFinal.get_buffer().set_text("Tiempo de respuesta: " + str(5) + "ms \nPrueba" + str(3))
        Notif.update("LanzApaches","Finalizado el lanzamiento de comandos AB","dialog-information")
        Notif.show()
        
    def Test(self,widget):
        Notif = Notify.Notification.new ("LanzApaches","Se ha iniciado el lanzamiento de comandos AB","dialog-information")
        Notif.show()
        
        a = float(self.entryCargas1.get_buffer().get_text())
        b = float(self.entryCargas2.get_buffer().get_text())
        c = float(self.entryCargas3.get_buffer().get_text())
        
        tot = a+b+c
        a = int((100/tot)*a)
        b = int(((100/tot)*b)+a)
        c = int(((100/tot)*c)+b)
        
        for n in range(c):
            ran = random.randint(1,c)
            if (ran<=a):
                self.Lanzador(self.entryDir1.get_buffer().get_text())
            elif (ran<=b):
                self.Lanzador(self.entryDir2.get_buffer().get_text())
            else:
                self.Lanzador(self.entryDir3.get_buffer().get_text())
    
        TotReq = 0.0
        for el in self.Trequest:
            TotReq = TotReq + el
        FinalR = TotReq / c
        
        TotProd = 0.0
        for el in self.Prod:
            TotProd = TotProd + (1/el)
        FinalP = c / TotProd
        
        self.resultlist.append(["Tiempo de respuesta total: " + str(TotReq/1000) + " s"])
        self.resultlist.append(["Número de peticiones: " + str(c)])
        self.resultlist.append(["Tiempo de respuesta medio: " + str(FinalR)+ " ms"] )
        self.resultlist.append(["Productividad: " + str(FinalP) + " pet/sec" ])
        self.Trequest=[]
        self.Prod=[]

        Notif.update("LanzApaches","Finalizado el lanzamiento de comandos AB","dialog-information")
        Notif.show()
         
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
           

    