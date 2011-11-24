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
# LanzApaches - Lanzador de comandos ab para AESI
#
# @author : Manuel Joaquin Díaz Pol
# @date   : November 2011

import commands
import random
from gi.repository import Gtk

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
        #self.selCarga = builder.get_object("comboboxtext1")
        self.resultlist = builder.get_object("liststore1")
        self.about = builder.get_object("aboutdialog1")
        self.Trequest=[]  
        
    def Salir(self,widget):
        print "He presionado el boton salir"
        
        Gtk.main_quit()
        
    def Acerca(self,widget):
        self.about.run()
        self.about.hide()
    
    def Pruebas(self,widget):
        #self.Lanzador("http://130.206.134.121/carga1.php")
        #self.Lanzador("http://130.206.134.121/carga1.php")
        
        #TotReq = 0.0
        #for el in self.Trequest:
        #TotReq = TotReq + el
        #print TotReq
        self.resultlist.append(["Hola"])
        self.resultlist.append(["Adios"])
        self.resultlist.append(["Denuevo"])
        #self.textoFinal.get_buffer().set_text("Tiempo de respuesta: " + str(5) + "ms \nPrueba" + str(3))
        
    def Test(self,widget):
        print "He presionado el boton de test1"
        
        a = float(self.entryCargas1.get_buffer().get_text())
        b = float(self.entryCargas2.get_buffer().get_text())
        c = float(self.entryCargas3.get_buffer().get_text())
        #sel = self.selCarga.get_active_text()
        
        tot = a+b+c
        a = int((100/tot)*a)
        b = int((100/tot)*b)
        c = int((100/tot)*c)
        
        TotLan = a+b+c
        
        while ((a>0) or (b>0) or (c>0)):
            ran = random.randint(1,3)
            if (ran==1 and a>0):
                self.Lanzador("http://130.206.134.121/carga1.php")
                a -=1
            elif (ran==2 and b>0):
                self.Lanzador("http://130.206.134.121/carga2.php")
                b -=1
            elif (ran==3 and c>0):
                self.Lanzador("http://130.206.134.121/carga2.php")
                c -=1               
        
        TotReq = 0.0
        for el in self.Trequest:
            TotReq = TotReq + el
        Final = TotReq / TotLan 
        self.resultlist.append(["Tiempo de respuesta: " + str(TotReq)])
        self.resultlist.append(["Numero de peticiones: " + str(TotLan)])
        self.resultlist.append(["Productividad: " + str(Final)])
         
    def Lanzador(self,link):
        Comando = "ab -k -n 1 " + link
        result = commands.getoutput(Comando)
        self.textoResultado1.get_buffer().set_text(result)
        tupla = result.split("Time per request:       ")
        tupla = tupla[1].split(" [ms]")
        self.Trequest.append(float(tupla[0]))         
        
        
        

if __name__ == '__main__':
    main()
    Gtk.main()
           

    