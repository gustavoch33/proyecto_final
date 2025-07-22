
import serial, serial.tools.list_ports
from threading import Thread, Event
from tkinter import StringVar

class Comunicacion():
    def __init__(self, *args):
        super().__init__(*args)
        self.datos_recibidos = StringVar()

        self.pic = serial.Serial()
        self.pic.timeout = 0.1

        self.baudrates = ["1200", "2400", "4800", "9600", "19200", "38400", "115200"]
        self.puertos = []

        self.señal = Event()
        self.hilo = None

    def puertos_disponibles(self):
        self.puertos = [port.device for port in serial.tools.list_ports.comports()]

    def conexion_serial(self):
        try:
            self.pic.open()
        except:
            pass

        if (self.pic.is_open):
            self.iniciar_hilo()
            print("Conectado")

    def enviar_datos(self, data):
        if (self.pic.is_open):
            self.datos = str(data) + "\n"
            self.pic.write(self.datos.encode())
        else:
            print("Error")

    def leer_datos(self):
        try:
            while (self.señal.isSet() and self.pic.is_open):
                data = self.pic.readline().decode("utf-8").strip()
                if(len(data) > 1):
                    self.datos_recibidos.set(data)
        except TypeError:
            pass

    def iniciar_hilo(self):
        self.hilo = Thread(target = self.leer_datos)
        self.hilo.setDaemon(1)
        self.señal.set()
        self.hilo.start()

    def stop_hilo(self):
        if(self.hilo is not None):
            self.señal.clear()
            self.hilo.join()
            self.hilo = None

    def desconectar(self):
        self.stop_hilo()
        self.pic.close()
        print("Desconectado")