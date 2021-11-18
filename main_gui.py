import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image, ImageGrab

from graph_part import Grafo_circuito
from time import sleep


ventana = tk.Tk()

ventana.geometry("1200x650")


frame_superior = tk.Frame(ventana)
frame_superior.pack()

frame_inferior = tk.Frame(ventana)
frame_inferior.pack()

frame_herramientas = tk.Frame(frame_superior)
frame_herramientas.grid(row=0,column=0)

frame_materiales = tk.Frame(frame_inferior)
frame_materiales.grid(row=0,column=0)

frame_canvas = tk.Frame(frame_inferior)
frame_canvas.grid(row=0,column=1)


# canvas
img_fondo_canvas = Image.open("Imagenes/fondo_canvas.png")
fondo_canvas = ImageTk.PhotoImage(img_fondo_canvas)


canvas_circuito = tk.Canvas(frame_canvas, width=1024,height=512, bg="white", cursor="tcross")
canvas_circuito.pack()

canvas_circuito.create_image(0, 0, anchor="nw", image=fondo_canvas, tags="fondo_canvas")
# ---------------------------------------------


# funciones de los botones

# la clave del diccionario es el tag, se guarda una tupla
# con tres elementos, valor, conexion1, conexion2

elementos_circuito = {}

tag_num = 0
contador_resistencias = 0
contador_voltajes = 0

btn = False
btn_conexion = False

creando_conexion = False
eleme = ""

rotar = False

valor_material = None
win = None

tag_elemento_actual = ""

conexion_desde = ""
conexion_hasta = ""

def es_numero(event):
    valor = event.widget.get()
    try:
        int(valor[-1])
    except:
        event.widget.delete(len(valor)-1)

def guardar_cambios(event=None):
    global valor_material, win, tag_elemento_actual

    try:
        if int(valor_material.get()) != 0:
            elementos_circuito[tag_elemento_actual] = []
            elementos_circuito[tag_elemento_actual].append(valor_material.get())
            win.destroy()
        
        else:
            pass
    except:
        pass

def definir_valores(elemento):
    global valor_material, win

    win = tk.Toplevel()
    win.wm_title("Definir valores")

    ventana.eval(f'tk::PlaceWindow {str(win)} center')

    frame_u = tk.Frame(win)
    frame_u.pack()

    frame_d = tk.Frame(win)
    frame_d.pack()

    if elemento == 'r':
        valor = tk.Label(frame_u, text="Valor resistencia: ")
        valor.grid(row=0, column=0, pady=10)

        unidad = tk.Label(frame_u, text=" Ohms ")
        unidad.grid(row=0, column=3, pady=10)

    
    elif elemento == 'v':
        valor = tk.Label(frame_u, text="Valor voltaje: ")
        valor.grid(row=0, column=0, pady=10) 

        unidad = tk.Label(frame_u, text=" Volts ")
        unidad.grid(row=0, column=3, pady=10)      

    valor_material = tk.Entry(frame_u)
    valor_material.grid(row=0,column=2, pady=10)

    valor_material.focus()

    valor_material.bind("<KeyRelease>", es_numero)
    win.bind('<Return>', guardar_cambios)
    
    b = ttk.Button(frame_d, text="Aceptar", command=guardar_cambios)
    b.grid(row=0, column=0, pady=10)

    win.focus()
    win.transient(ventana)
    win.grab_set()
    ventana.wait_window(win)

def colocar_material(elemento):
    global tag_num, contador_resistencias, contador_voltajes, btn, eleme, tag_elemento_actual

    tag_elemento = ""
    if elemento == "r":
        tag_elemento = elemento + str(tag_num-contador_voltajes)
        canvas_circuito.create_image(-100, -100, anchor="nw", image=imagen_resistencia, tags='r' + str(tag_num-contador_voltajes))
        contador_resistencias += 1

    elif elemento == "v":
        tag_elemento = elemento + str(tag_num-contador_resistencias)
        canvas_circuito.create_image(-100, -100, anchor="nw", image=imagen_fuente_poder, tags='v' + str(tag_num-contador_resistencias))
        contador_voltajes += 1

    tag_num += 1
    btn = True
    eleme = elemento
    tag_elemento_actual = tag_elemento

def rotar_material():
    global rotar

    if btn == True:
        canvas_circuito.delete(tag_elemento_actual)

        if rotar == False:
            if tag_elemento_actual[0] == "r":
                canvas_circuito.create_image(-100, -100, anchor="nw", image=imagen_resistencia_90, tags=tag_elemento_actual)
            
            elif tag_elemento_actual[0] == "v":
                canvas_circuito.create_image(-100, -100, anchor="nw", image=imagen_fuente_poder_90, tags=tag_elemento_actual)

            rotar = True
        else:
            if tag_elemento_actual[0] == "r":
                canvas_circuito.create_image(-100, -100, anchor="nw", image=imagen_resistencia, tags=tag_elemento_actual)

            elif tag_elemento_actual[0] == "v":
                canvas_circuito.create_image(-100, -100, anchor="nw", image=imagen_fuente_poder, tags=tag_elemento_actual)

            rotar = False

def mover_mouse(event):
    global btn, btn_conexion, eleme, contador_resistencias, contador_voltajes, tag_elemento_actual, rotar
    
    x_fix = 64 * int((event.x+32)/64)
    y_fix = 64 * int((event.y+32)/64)

    if x_fix == 0:
        x_fix = 64

    if y_fix == 0:
        y_fix = 64

    if btn:
        x1, y1 = canvas_circuito.coords(tag_elemento_actual)
        if rotar:
            if x_fix == 1024:
                x_fix = 960
            if y_fix == 448 or y_fix == 512:
                y_fix = 386

            canvas_circuito.move(tag_elemento_actual, x_fix-x1-32, y_fix-y1)
        else:
            if x_fix == 960 or x_fix == 1024:
                x_fix = 896
            if y_fix == 512:
                y_fix = 448

            canvas_circuito.move(tag_elemento_actual, x_fix-x1, y_fix-y1-32)

    if btn_conexion:
        x1, y1, x2, y2 = canvas_circuito.coords("pre_punto")
        canvas_circuito.move("pre_punto", x_fix-x1-4, y_fix-y1-4)
    
    if creando_conexion:
        x1, y1, x2, y2 = canvas_circuito.coords("pre_linea")
        canvas_circuito.delete("pre_linea")

        canvas_circuito.create_line(x1,y1,x_fix,y_fix, width=2, tags="pre_linea", fill="blue")       

def dejar_objeto(event):
    global btn, btn_conexion, eleme, tag_num, contador_resistencias, contador_voltajes, rotar, creando_conexion, conexion_desde, conexion_hasta

    if btn:
        btn = False


        definir_valores(eleme)
        eleme = ""

        try:
            if tag_elemento_actual[0] == "r":
                texto = str(elementos_circuito[tag_elemento_actual][0]) + " Ω"
            elif tag_elemento_actual[0] == "v":
                texto = str(elementos_circuito[tag_elemento_actual][0]) + " v"

            x1, y1 = canvas_circuito.coords(tag_elemento_actual)

            if rotar:
                canvas_circuito.create_text(x1+70,y1+14,fill="black", font="Times 12 italic bold", text=tag_elemento_actual, tags=tag_elemento_actual)
                canvas_circuito.create_text(x1+70,y1+32,fill="black", font="Times 12 italic bold", text=texto, tags=tag_elemento_actual)

                canvas_circuito.create_text(x1-5,y1+14,fill="green", font="Times 12 italic bold", text="  ", tags=tag_elemento_actual)
                canvas_circuito.create_text(x1-5,y1+32,fill="green", font="Times 12 italic bold", text="    ", tags=tag_elemento_actual)
            else:
                canvas_circuito.create_text(x1+32,y1-12,fill="black", font="Times 12 italic bold", text=tag_elemento_actual, tags=tag_elemento_actual)
                canvas_circuito.create_text(x1+32,y1+6,fill="black", font="Times 12 italic bold", text=texto, tags=tag_elemento_actual)

                canvas_circuito.create_text(x1+32,y1+60,fill="green", font="Times 12 italic bold", text="  ", tags=tag_elemento_actual)
                canvas_circuito.create_text(x1+32,y1+78,fill="green", font="Times 12 italic bold", text="    ", tags=tag_elemento_actual)
        except:
            if tag_elemento_actual[0] == "r":
                contador_resistencias -= 1
            if tag_elemento_actual[0] == "v":
                contador_voltajes -= 1

            canvas_circuito.delete(tag_elemento_actual)
            tag_num -= 1

        rotar = False

    if btn_conexion:
        x1, y1, x2, y2 = canvas_circuito.coords("pre_punto")

        
        id_seleccion = canvas_circuito.find_overlapping(x1, y1, x2, y2)

        lista_tags_filtrada = []
        for i in id_seleccion:
            if canvas_circuito.gettags(i)[0][0] == "r" or canvas_circuito.gettags(i)[0][0] == "v" :
                lista_tags_filtrada.append(canvas_circuito.gettags(i)[0])
        
        lista_tags_filtrada.sort(reverse=True, key=len)
        
        for i in lista_tags_filtrada:
            if i[0] == "r" or i[0] == "v" :
                conexion_desde = i
                canvas_circuito.create_line(x1+4,y1+4,x1+4,y1+4, width=2, tags="pre_linea", fill="blue")

                canvas_circuito.itemconfigure("pre_punto",  tags="conexion_tmp")
                creando_conexion = True
                btn_conexion = False

                return 0
    
    if creando_conexion:
        x1, y1, x2, y2 = canvas_circuito.coords("pre_linea")

        id_seleccion = canvas_circuito.find_overlapping(x2-10, y2-10, x2+10, y2+10)

        lista_tags_filtrada = []
        for i in id_seleccion:
            if canvas_circuito.gettags(i)[0][0] == "r" or canvas_circuito.gettags(i)[0][0] == "v" :
                lista_tags_filtrada.append(canvas_circuito.gettags(i)[0])
        
        lista_tags_filtrada.sort(reverse=True, key=len)

        for i in lista_tags_filtrada:
            if i[0] == "r" or i[0][0] == "v" :
                conexion_hasta = i

                tag_conexion = conexion_desde+conexion_hasta

                canvas_circuito.create_oval(x2-4,y2-4,x2+4,y2+4,fill="blue", tags=tag_conexion)
                canvas_circuito.itemconfigure("pre_linea",  tags=tag_conexion)
                canvas_circuito.itemconfigure("conexion_tmp",  tags=tag_conexion)

                print("Desde: {0} ----> Hasta: {1}".format(conexion_desde,conexion_hasta))
                print("El tag de conexion es: ", tag_conexion)

                elementos_circuito[conexion_desde[0:2]].append(tag_conexion)
                elementos_circuito[conexion_hasta[0:2]].append(tag_conexion)

                conexion_desde = ""
                conexion_hasta = ""
                creando_conexion = False

                return 0

        canvas_circuito.delete("pre_linea")
        canvas_circuito.create_line(x2,y2,x2,y2, width=2, tags="pre_linea", fill="blue")

        canvas_circuito.create_line(x1,y1,x2,y2, width=2, tags="conexion_tmp", fill="blue")
    
def unir_objetos():
    global btn_conexion

    canvas_circuito.create_oval(20,20,28,28,fill="blue", tags="pre_punto")
    btn_conexion = True

def pantallazo(widget, nombre):
    x=ventana.winfo_rootx()
    y=ventana.winfo_rooty()
    x1=x+ventana.winfo_width()
    y1=y+ventana.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save(nombre)

def resolver_circuito():
    try:
        pantallazo(canvas_circuito, "circuito/circuito_sin_resolver.png")
        
        conexiones = []

        vertices = []
        aristas = []

        for i in elementos_circuito.keys():
            for j in elementos_circuito[i][1:]:
                conexiones.append(j)

        conexiones = list(dict.fromkeys(conexiones))
        conexiones.sort(reverse=True, key=len)
        
        print("Conexiones: ", conexiones)
        conexiones_copia = conexiones
        for idx,i in enumerate(conexiones_copia):
            if len(i) >= 3:
                if i in conexiones:
                    for idxj, j in enumerate(conexiones_copia[idx+1:]):
                        if j in i:
                            conexiones.remove(j)
        
        conexiones = list(dict.fromkeys(conexiones))
        vertices = conexiones

        for idx, i in enumerate(vertices):
            division = len(i)/2
            for x in range(int(division)):
                material = i[x*2:(x+1)*2]
                for idxj,j in enumerate(vertices[idx+1:]):
                    if material in j:
                        aristas.append([str(idx)+str(idxj+idx+1),material,elementos_circuito[material][0],0])


        print("vertices: ", vertices)
        print("aristas: ", aristas)

        grafo = Grafo_circuito(vertices,aristas)
        grafo.encontrar_ciclos()
        grafo.encontrar_ecuaciones()

        resultado = grafo.resultado_circuito()

        
        
        for i in resultado.keys():
            #canvas_circuito.create_text(x1+32,y1+6,fill="black", font="Times 12 italic bold", text=texto, tags=tag_elemento_actual)
                    for id in canvas_circuito.find_withtag(i):
                        if canvas_circuito.type(id) == "text":
                            if canvas_circuito.itemcget(id,"text") == "  ":
                                canvas_circuito.itemconfigure(id,text=str(resultado[i][2]) + " V")

                            elif canvas_circuito.itemcget(id,"text") == "    ":
                                canvas_circuito.itemconfigure(id,text=str(resultado[i][1]) + " A")

        canvas_circuito.update()
        print("El resultado del circuito es: ", resultado)

        sleep(1)
        pantallazo(canvas_circuito, "circuito/circuito_resuelto.png")
        
        grafo.dibujar()
        

    except:
        print("Ocurrio un error en la solucion del circuito, verifique que el circuito este bien modelado")

canvas_circuito.bind("<Motion>", mover_mouse)
canvas_circuito.bind("<Button-1>", dejar_objeto)


# Imagenes y botones de la barra de herramientas
imagen_seleccionar = tk.PhotoImage(file="Imagenes/solution.png")
boton_seleccionar = tk.Button(frame_herramientas, image=imagen_seleccionar,padx=40,pady=40, command=resolver_circuito)
boton_seleccionar.grid(row=0,column=0, padx=10, pady=10)

imagen_rotar = tk.PhotoImage(file="Imagenes/rotate.png")
boton_rotar = tk.Button(frame_herramientas, image=imagen_rotar,padx=40,pady=40, command=rotar_material)
boton_rotar.grid(row=0,column=1, padx=10, pady=10)

# imagen_borrar = tk.PhotoImage(file="Imagenes/borrar.png")
# boton_borrar = tk.Button(frame_herramientas, image=imagen_borrar,padx=40,pady=40)
# boton_borrar.grid(row=0,column=2, padx=10, pady=10)

# imagen_editar = tk.PhotoImage(file="Imagenes/editar.png")
# boton_editar = tk.Button(frame_herramientas, image=imagen_editar,padx=40,pady=40)
# boton_editar.grid(row=0,column=3, padx=10, pady=10)

# --------------------------------------------------

# Imagenes y botones de la barra de materiales

imagen_linea_conexion = tk.PhotoImage(file="Imagenes/linea_conexion.png")
boton_linea_conexion = tk.Button(frame_materiales, image=imagen_linea_conexion, padx=40,pady=40, command=unir_objetos)
boton_linea_conexion.grid(row=0, column=0, padx=10, pady=10)

img_resistencia = Image.open("Imagenes/resistor.png")

imagen_resistencia = ImageTk.PhotoImage(img_resistencia)
imagen_resistencia_90 = ImageTk.PhotoImage(img_resistencia.rotate(90))

boton_resistencia = tk.Button(frame_materiales, image=imagen_resistencia, padx=40,pady=40, command=lambda : colocar_material("r"))
boton_resistencia.grid(row=1, column=0, padx=10, pady=10)

img_fuente_poder = Image.open("Imagenes/fuente_poder.png")
img_fuente_poder = img_fuente_poder.resize((64,64))

imagen_fuente_poder = ImageTk.PhotoImage(img_fuente_poder)
imagen_fuente_poder_90 = ImageTk.PhotoImage(img_fuente_poder.rotate(-90))

boton_fuente_poder = tk.Button(frame_materiales, image=imagen_fuente_poder, padx=40,pady=40, command=lambda : colocar_material("v"))
boton_fuente_poder.grid(row=2, column=0, padx=10, pady=10)
# ----------------------------------------------

ventana.mainloop()

