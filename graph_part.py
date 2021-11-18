#from main_gui import resolver_circuito

import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes import graph
from networkx.drawing.nx_pydot import write_dot
import copy
import ast
import sympy as sym

from networkx.generators.trees import prefix_tree

class Grafo_circuito(object):
    def __init__(self,vertices,relaciones):
        print("----------------- Iniciando grafo --------------------")

        self.vertices = vertices
        self.relaciones = relaciones

        self.grafo_inicial = nx.Graph()
        self.grafo_inicial.add_nodes_from(self.vertices)

        self.aristas = []
        self.pesos = {}

        contador_aristas_multiples = 0

        self.aristas_multiples = []

        for i in relaciones: # ('verticeA', 'verticeB') # ['r0r1r2','v0r0r1']
            vertice_inicial = str(self.vertices[int(i[0][0])])
            vertice_final = str(self.vertices[int(i[0][1])])

            arista = (vertice_inicial, vertice_final)

            if arista not in self.grafo_inicial.edges():
                self.grafo_inicial.add_edge(vertice_inicial, vertice_final)
        
            else: # Se encontro una arista multiple
                self.aristas_multiples.append(arista)
                nombre_vertice = "x"+ str(contador_aristas_multiples)
                self.grafo_inicial.add_node(nombre_vertice)
                contador_aristas_multiples += 1

                self.grafo_inicial.add_edge(vertice_inicial, nombre_vertice)
                self.grafo_inicial.add_edge(nombre_vertice, vertice_final)


                self.grafo_inicial.edges[nombre_vertice, vertice_final]["tipo"] = 0
                self.grafo_inicial.edges[nombre_vertice, vertice_final]["elemento"] = 0

                self.grafo_inicial.edges[nombre_vertice, vertice_final]["voltaje"] = 0
                self.grafo_inicial.edges[nombre_vertice, vertice_final]["resistencia"] = 0
                self.grafo_inicial.edges[nombre_vertice, vertice_final]["corriente"] = sym.var("i"+str(i[1][1]))

                self.grafo_inicial.edges[nombre_vertice, vertice_final]["informacion"] = [0,0,0,0,"i"+str(i[1][1])]

                vertice_final = nombre_vertice



            self.grafo_inicial.edges[vertice_inicial, vertice_final]["tipo"] = i[1][0] 
            self.grafo_inicial.edges[vertice_inicial, vertice_final]["elemento"] = i[1][1] 

            if i[1][0] == 'r':
                self.grafo_inicial.edges[vertice_inicial, vertice_final]["voltaje"] = "Nan"
                self.grafo_inicial.edges[vertice_inicial, vertice_final]["resistencia"] = i[2]
                self.grafo_inicial.edges[vertice_inicial, vertice_final]["corriente"] = sym.var("i"+str(i[1][1]))

                self.grafo_inicial.edges[vertice_inicial, vertice_final]["informacion"] = [i[1][0], i[1][1], "Nan", i[2],"i"+str(i[1][1])]
            else:
                self.grafo_inicial.edges[vertice_inicial, vertice_final]["voltaje"] = -1*int(i[2])
                self.grafo_inicial.edges[vertice_inicial, vertice_final]["resistencia"] = 0
                self.grafo_inicial.edges[vertice_inicial, vertice_final]["corriente"] = sym.var("iv"+str(i[1][1]))

                self.grafo_inicial.edges[vertice_inicial, vertice_final]["informacion"] = [i[1][0], i[1][1], -1*int(i[2]), 0, "iv"+str(i[1][1])]

    def encontrar_ciclos(self):
        ciclos_fundamentales = nx.cycle_basis(self.grafo_inicial)
        print("Los ciclos fundamentales son: ", ciclos_fundamentales)
        
        list_temp=[]

        dic= {}
        for i in ciclos_fundamentales:
            print(i)
            dic[str(i)] = 0

            h_temp= self.grafo_inicial.subgraph(i)
            list_temp.append(h_temp)

        
        for indx1, k in enumerate(list_temp):
            for indx2,x in enumerate(list_temp[indx1+1:]):
                for g in k.edges():
                    if g in x.edges():
                        dic[str(ciclos_fundamentales[indx1])] += 1
                        dic[str(ciclos_fundamentales[indx1+1+indx2])] += 1


        print("Antes de ordenar: ", dic)

        
        longitud = len(dic)

        if longitud > 1:
            dic_ordenado = {}

            for i in range(longitud):
                max=0
                clave = ""
                for p in dic.keys():
                    if dic[p] > max:
                        max = dic[p]
                        clave = p
                
                dic_ordenado[clave] = max
                dic.pop(clave)
        else:
            dic_ordenado = dic

        print("Despues de ordenar: ", dic_ordenado)

        ciclos_fundamentales = []

        for i in dic_ordenado.keys():
            ciclos_fundamentales.append(ast.literal_eval(i))

        print("Ciclos fundamentales despues", ciclos_fundamentales)
        
        self.lista_grafos = []
        first= True
        globales=[]
        for numero_ciclo, grafo in enumerate(ciclos_fundamentales):
            G_tmp = self.grafo_inicial.subgraph(grafo)

            G_tmp = nx.DiGraph(G_tmp)

            aristas =  list(G_tmp.edges())
            # dirige el primer ciclo fundamental 

            if first:
                for idx1, arista in enumerate(aristas):
                    for arista2 in aristas[idx1+1:]:
                        #print("Analizando: ", str(arista), str(arista2))
                        if arista[0]==arista2[1] and arista[1]==arista2[0]:
                           #print("ELIMINANDO: ", arista2[0],"-", arista2[1])
                            G_tmp.remove_edge(arista2[0], arista2[1])
                            aristas.remove(arista2)
                            pass
                        elif arista[0]==arista2[0]:
                           #print("ELIMINANDO: ", arista2[0],"-", arista2[1])
                            G_tmp.remove_edge(arista2[0], arista2[1])
                            aristas.remove(arista2)
                            pass
                        elif arista[1]==arista2[1]:
                            #print("ELIMINANDO: ", arista2[0],"-", arista2[1])
                            G_tmp.remove_edge(arista2[0], arista2[1])
                            aristas.remove(arista2)
                            pass
                        elif arista[1]==arista2[0]:
                            aristas.remove(arista2)
                            aristas.insert(idx1+1, arista2)
                            #print("La INDICADA", str(arista2))
                        else:
                            pass
                for i in G_tmp.edges():
                    globales.append(i)
                #print("PRUEBAAA FINAL", globales)
                first= False
            else:
                indicada= [aristaa for aristaa in aristas if aristaa in globales]
                nueva=(indicada[0][1], indicada[0][0])
                if len(self.aristas_multiples) == 0:
                    self.aristas_multiples.append(nueva)

                G_tmp.edges[nueva]["corriente"]= -1 * G_tmp.edges[nueva]["corriente"]
                
                G_tmp.edges[nueva]["informacion"][4]= "-"+ str(G_tmp.edges[nueva]["informacion"][4])
                aristas.remove(nueva)
                #print("CASI   ",indicada[0])
                aristas.insert(0, nueva)
                #print("CASI 2  ",aristas)

                for idx1, arista in enumerate(aristas):
                    for arista2 in aristas[idx1+1:]:
                        #print("Analizando: ", str(arista), str(arista2))
                        if arista[0]==arista2[1] and arista[1]==arista2[0]:
                            #print("ELIMINANDO: ", arista2[0],"-", arista2[1])
                            G_tmp.remove_edge(arista2[0], arista2[1])
                            aristas.remove(arista2)
                            pass
                        elif arista[0]==arista2[0]:
                            #print("ELIMINANDO: ", arista2[0],"-", arista2[1])
                            G_tmp.remove_edge(arista2[0], arista2[1])
                            aristas.remove(arista2)
                            pass
                        elif arista[1]==arista2[1]:
                            #print("ELIMINANDO: ", arista2[0],"-", arista2[1])
                            G_tmp.remove_edge(arista2[0], arista2[1])
                            aristas.remove(arista2)
                            pass
                        elif arista[1]==arista2[0]:
                            aristas.remove(arista2)
                            aristas.insert(idx1+1, arista2)
                            #print("La INDICADA", str(arista2))
                        else:
                            pass
                for i in G_tmp.edges():
                    globales.append(i)
                #print("PRUEBAAA FINAL", globales)
                first= False

            # dirige los demas grafos en funcion de los anteriores

                            
            self.lista_grafos.append(G_tmp)

            plt.figure("ciclo fundamental " + str(numero_ciclo))

            pos = nx.planar_layout(G_tmp)
            vertice_valor_material = nx.get_edge_attributes(G_tmp,"informacion")
            nx.draw_networkx_edge_labels(G_tmp,pos,edge_labels=vertice_valor_material,font_color='red')
            
            nx.draw(G_tmp ,pos,edge_color='black',width=1,linewidths=1,\
            node_size=1500,node_color='pink',alpha=0.9,\
            labels={node:node for node in G_tmp.nodes()})

            plt.savefig("circuito/ciclo fundamental " + str(numero_ciclo))
                

    def encontrar_ecuaciones(self):
        sistema_ecuaciones = []

        elemento_con_incognita = {}

        dic_vertice = {}
        for grafo in self.lista_grafos:

            ecuacion = 0
            for arista in grafo.edges():
                voltaje = grafo.edges[arista]["voltaje"]

                if arista in self.aristas_multiples or (arista[1],arista[0]) in self.aristas_multiples:

                    arista_incidente_0 = grafo.in_edges(arista[0])
                    arista_saliendo_0 = grafo.edges(arista[0])

                    arista_incidente_1 = grafo.in_edges(arista[1])
                    arista_saliendo_1 = grafo.edges(arista[1])

                    for i in arista_incidente_0:
                        arista_incidente_0 = i

                    for i in arista_saliendo_0:
                        arista_saliendo_0 = i

                    for i in arista_incidente_1:
                        arista_incidente_1 = i

                    for i in arista_saliendo_1:
                        arista_saliendo_1 = i         
   

                    valor_incidente_0 = grafo.edges[arista_incidente_0]["corriente"]
                    valor_saliendo_0 = -1 * grafo.edges[arista_saliendo_0]["corriente"]

                    valor_incidente_1 = grafo.edges[arista_incidente_1]["corriente"]
                    valor_saliendo_1 = -1 * grafo.edges[arista_saliendo_1]["corriente"]

                    try:
                        dic_vertice[arista[0]].add(valor_incidente_0)
                        dic_vertice[arista[0]].add(valor_saliendo_0)

                        dic_vertice[arista[1]].add(valor_incidente_1)
                        dic_vertice[arista[1]].add(valor_saliendo_1)
                    except:
                        dic_vertice[arista[0]] = {valor_incidente_0,valor_saliendo_0}
                        dic_vertice[arista[1]] = {valor_incidente_1,valor_saliendo_1}

                try:
                    if voltaje == "Nan":
                        voltaje =  grafo.edges[arista]["corriente"] * int(grafo.edges[arista]["resistencia"])
                        elemento_con_incognita[grafo.edges[arista]["corriente"]] = (grafo.edges[arista]["tipo"] + grafo.edges[arista]["elemento"], int(grafo.edges[arista]["resistencia"]))

                    ecuacion += voltaje
                except:
                    if voltaje != 0:
                        ecuacion = ecuacion + int(voltaje)
   
            sistema_ecuaciones.append(ecuacion)

        for i in dic_vertice.keys():
            
            if 'v' not in i:
                ecuacion = 0
                for x in dic_vertice[i]:
                    ecuacion += x
                
                sistema_ecuaciones.append(ecuacion)

        if len(sistema_ecuaciones) == 1:
            sistema_ecuaciones[0] = sistema_ecuaciones[0].subs('i1','i0')

        print("El sistema de ecuaciones es: ")
        print("")
        for i in sistema_ecuaciones:
            print(i)
            print("")
            
        print("los elementos con incognita son: ", elemento_con_incognita)

        corrientes = sym.solve(sistema_ecuaciones)

        print("La solucion es: ", corrientes)

        if len(sistema_ecuaciones) == 1:
            corrientes[sym.var('i1')] = corrientes['i0']

        self.colocar_valores_en_gui = {}
        for i in corrientes.keys():
            try:
                nombre_elemento = elemento_con_incognita[i][0]
                valor_resistencia = elemento_con_incognita[i][1]

                self.colocar_valores_en_gui[nombre_elemento] = (i, corrientes[i], corrientes[i]*valor_resistencia)
            except:
                pass
            

    def resultado_circuito(self):
        return self.colocar_valores_en_gui


    def dibujar(self):

        plt.figure("Grafo simple")
        pos = nx.planar_layout(self.grafo_inicial)

        vertice_valor_material = nx.get_edge_attributes(self.grafo_inicial,"informacion")
        

        nx.draw_networkx_edge_labels(self.grafo_inicial,pos,edge_labels=vertice_valor_material,font_color='red')
        
        nx.draw(self.grafo_inicial ,pos,edge_color='black',width=1,linewidths=1,\
        node_size=1500,node_color='pink',alpha=0.9,\
        labels={node:node for node in self.grafo_inicial.nodes()})
        plt.savefig("circuito/Grafo simple ")
        
        plt.show()
        


if __name__ == "__main__":

    vertices = ['v0r1r2', 'r0r1r2', 'v0r0']
    relaciones = [['02', 'v0', '30', 0], ['01', 'r1', '3', 0], ['01', 'r2', '6', 0], ['12', 'r0', '8', 0]]
    G1 = Grafo_circuito(vertices,relaciones)
    G1.encontrar_ciclos()
    G1.encontrar_ecuaciones()
    G1.dibujar()



