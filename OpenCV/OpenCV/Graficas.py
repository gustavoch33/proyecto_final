from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(facecolor = "#000080")
plt.title("Grafica del voltaje", color = "red", size = 16, family = "Arial")
ax.set_xlabel("Time")
ax.set_ylabel("Voltage")
ax.set_ylim(-5, 5)

x = np.arange(0, np.pi, 0.1)
line, = ax.plot(x, np.sin(x), color = "g", marker = "o", linestyle = "solid",
               linewidth = 3, markersize = 1, markeredgecolor = "g")

def animate(i):
    line.set_ydata(np.sin(x+ i / 40))
    ax.set_xlim(ax.get_xlim())
    #print(line)
    return line,

def iniciar():
    global ani
    ani = animation.FuncAnimation(fig, animate, interval = 20, blit = True, save_count = 10)
    canvas.draw()

def pausar():
    ani.event_source.stop()

def reanudar():
    ani.event_source.start()

root = Tk()
root.geometry("645x535")
root.title("Grafica en Python")
root.minsize(width = 642, height = 535)

frm = Frame(root, bg = "white", bd = 3)
frm.pack(expand = 1, fill = "both")

canvas = FigureCanvasTkAgg(fig, master = frm)
canvas.get_tk_widget().pack(padx = 5, pady = 5, expand = 1, fill = "both")

Button(frm, text = "Graficar Datos", width = 15, bg = "purple4", fg = "white", command = iniciar).pack(
    pady = 5, side = "left", expand = 1)
Button(frm, text = "Pausar", width = 15, bg = "salmon", fg = "white", command = pausar).pack(
    pady = 5, side = "left", expand = 1)
Button(frm, text = "Reanudar", width = 15, bg = "green", fg = "white", command = reanudar).pack(
    pady = 5, side = "left", expand = 1)

root.mainloop()