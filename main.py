from os import truncate
import pathlib
import random

import names

import pandas as pd
import matplotlib.pyplot as plt

random.seed(250)

#Manejo de excepción
def try_int(msg):
    try:
        return int(input(msg))
    except ValueError:
        print("Error: Ingrese una valor válido!")


def get_pilotos():
    set(df["Piloto"].values)

def agregar_carrera():
    piloto = input("Ingrese el nombre del piloto: ")

    if piloto not in get_pilotos():
        print("Error: El piloto no existe")


file = input("Ingrese el nombre del archivo principal [default: datos.csv]: ")

if file.replace("\n", "").replace(" ", "") == "":
    file = "datos.csv"

df = None
primer_corrida = False
#Crea el archivo en caso de que este no haya sido creado con anterioridad
if not pathlib.Path("datos.csv").exists():
    with open("datos.csv", "x+") as f, open("num_carreras.txt", "x+") as g:
        f.write("Piloto")

        g.write("0")

        f.close()
        g.close()
        primer_corrida = True

df = pd.read_csv(file,  index_col=0)
conteo = pd.read_csv("num_carreras.txt")

#Función que crea un registro con posición, VMedia y VMax
def crear_registro(nombre):
    with open(nombre+".csv", 'x+') as k:
        k.write("Posición,Velocidad Media,Velocidad Max")
        k.close()

        return pd.read_csv(nombre+".csv")

#Función que genera posiciones en la carrera
def generar_posiciones(n_carreras, n_pilotos):
    carreras = []
    for _ in range(n_carreras):
        Posicións = [num + 1 for num in range(n_pilotos)]
        random.shuffle(Posicións)
        carreras.append(Posicións)

    return carreras

#Función que genera velocidades de los participantes
def generar_velocidades(n_carreras, n_pilotos):
    velocidades = []
    for _ in range(n_carreras):
        velocidades_de_carrera = [random.randrange(150, 250) for _ in range(n_pilotos)]
        velocidades_de_carrera.sort()
        velocidades.append(velocidades_de_carrera)

    return velocidades


if primer_corrida:
    global carrera
    print("Warning: Primera ejecución del programa detectada!")

    carrera: int = try_int("Ingrese el número de carreras que va a registrar por piloto: ")

    with open("num_carreras.txt", "w") as f:
        f.truncate(0)

        f.write(str(carrera))

        f.close()


    num_pilotos = input("Ingrese el número de pilotos que desea generar aleatoriamente [default: rand]: ")

    if num_pilotos.isalnum():
        num_pilotos = int(num_pilotos)
    else:
        num_pilotos = random.randint(5,20)

    posiciones_carreras = generar_posiciones(carrera, num_pilotos)
    velocidades_carreras = generar_velocidades(carrera, num_pilotos)
    for i in range(num_pilotos):

        nombre = names.get_full_name()
        df_piloto = crear_registro(nombre)

        promedio_velocidad_carrera = 0
        promedio_posicion = 0
        for j in range(carrera):

            promedio_posicion += posiciones_carreras[j][i]
            promedio_velocidad_carrera += velocidades_carreras[j][posiciones_carreras[j][i]-1]
            df_piloto = pd.concat([df_piloto, pd.DataFrame({
                    "Velocidad Media": [velocidades_carreras[j][posiciones_carreras[j][i]-1]],
                    "Posición": [posiciones_carreras[j][i]],
                    "Velocidad Max": [velocidades_carreras[j][posiciones_carreras[j][i]-1] + random.randrange(10,25)]
                }, index=[j+1])])

        df = pd.concat([df, pd.DataFrame({
            "Piloto": [nombre],
            "Pos Promedio": promedio_posicion/carrera,
            "Vel Promedio": promedio_velocidad_carrera/carrera
            }
            , index=[i+1])]
        )

        df_piloto.to_csv(nombre + ".csv")
        df.to_csv("datos.csv")

opcion = -1
#Se abre el archivo
with open("num_carreras.txt", "r") as f:
    string = f.read()
    carrera = int(string)
#Menú del programa
while opcion != 6:
    print("Menu de opciones: \n"
          "    1. Consultar estadísticas\n"
          "    2. Graficar estadísticas\n"
          "    3. Comparar entre dos pilotos"
          "    4. Agregar datos de nueva carrera\n"
          "    5. Eliminar todo\n"
          "    6. Salir\n"
    )

    opcion = try_int("Ingrese una opción: ")

    if opcion == 1:
        print(df)
        
        while True:
            nombre = input("Ingrese el nombre o id del piloto del que desea graficar sus estadísticas: ")

            if nombre.isdecimal():
                print("Detectado índice de piloto")
                if df.loc[int(nombre)].empty:
                    print("Error: Ingrese un índice válido")
                else:
                    nombre = df.loc[int(nombre)]["Piloto"]
                    break

            if df.loc[df['Piloto'] == nombre].empty:
                print("Error: Ingrese un piloto válido")
            else:
                break
            
        df_piloto = pd.read_csv(nombre + ".csv", index_col=0)
        print(df_piloto)
    if opcion == 2:
        print(df)
        
        while True:
            nombre = input("Ingrese el nombre o id del piloto del que desea graficar sus estadísticas: ")

            if nombre.isdecimal():
                print("Detectado índice de piloto")
                if df.loc[int(nombre)].empty:
                    print("Error: Ingrese un índice válido")
                else:
                    nombre = df.loc[int(nombre)]["Piloto"]
                    break

            if df.loc[df['Piloto'] == nombre].empty:
                print("Error: Ingrese un piloto válido")
            else:
                break

        df_piloto = pd.read_csv(nombre + ".csv", index_col=0)
        
        #df_piloto2 = pd.read_csv("Phyllis Echevarria.csv", index_col=0)
        print(df_piloto)
        fig, ax= plt.subplots()


        while True:
            try:
                stat = input("Ingrese la estadística a graficar [Posición|Velocidad Media|Velocidad Max]: ")
                posiciones = df_piloto[stat].to_list()
                break
            except:
                print("Ingresa el nombre de una estadística válida")
        #posiciones2 = df_piloto2["Posición"].to_list()
        carreras = list(range(1, carrera+1))
        ax.plot(carreras, posiciones)
        #ax.plot(carreras, posiciones2)
        ax.set_title(stat, loc='center', fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
        plt.show()

