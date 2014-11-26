#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
#import os.path
import os


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            Info = line.split(' ')
            Metodo = Info[0]
            Metodo = Metodo.upper()
            Lista_Metodos = ["INVITE", "BYE", "ACK"]
            Mensaje = line.split()
            IP_Cliente = str(self.client_address[0])
            if Metodo == 'INVITE':
                print line
                Envio = 'SIP/2.0 100 Trying\r\n\r\n'
                Envio += 'SIP/2.0 180 Ringing\r\n\r\n'
                Envio += 'SIP/2.0 200 OK\r\n\r\n'
                self.wfile.write(Envio)
            elif Metodo == 'ACK':
                print 'RTP......'
                #aEjecutar es un string con lo que se ejecuta en la shell
                #Añado la IP del cliente en el envio de audio. Quito la 127.0.0.1
                aEjecutar = './mp32rtp -i ' + IP_Cliente + ' -p 23032 < '
                aEjecutar += sys.argv[3]
                print "Vamos a ejecutar", aEjecutar
                os.system('chmod 755 mp32rtp')
                os.system(aEjecutar)
            elif Metodo == 'BYE':
                print line
                Envio = 'SIP/2.0 200 OK\r\n\r\n'
                self.wfile.write(Envio)
            elif not Metodo in Lista_Metodos:
                if line != '':
                    Envio = 'SIP/2.0 405 Method Not Allowed\r\n\r\n'
                    self.wfile.write(Envio)
            elif len(Mensaje) != 3:
                Envio = 'SIP/2.0 400 Bad Request\r\n\r\n'
                self.wfile.write(Envio)
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    if len(sys.argv) == 4:
        if os.path.exists(sys.argv[3]):
            serv = SocketServer.UDPServer(("", int(sys.argv[2])), EchoHandler)
            print "Listening..."
            serv.serve_forever()
        else:
            print 'El fichero no existe'
    else:
        print 'Usage: python server.py IP port audio_file'
