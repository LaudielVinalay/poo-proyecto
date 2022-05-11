from os import truncate
import pathlib
import random

import names

import pandas as pd
import matplotlib.pyplot as plt

random.seed(250)

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

if not pathlib.Path("datos.csv").exists():
    with open("datos.csv", "x+") as f, open("num_carreras.txt", "x+") as g:
        f.write("Piloto")

        g.write("0")

        f.close()
        g.close()
        primer_corrida = True

df = pd.read_csv(file,  index_col=0)
conteo = pd.read_csv("num_carreras.txt")


def crear_registro(nombre):
    with open(nombre+".csv", 'x+') as k:
        k.write("Posición,Velocidad Media,Velocidad Max")
        k.close()

        return pd.read_csv(nombre+".csv")


def generar_posiciones(n_carreras, n_pilotos):
    carreras = []
    for _ in range(n_carreras):
        Posiciones = [num + 1 for num in range(n_pilotos)]
        random.shuffle(Posiciones)
        carreras.append(Posiciones)

    return carreras


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

with open("num_carreras.txt", "r") as f:
    string = f.read()
    carrera = int(string)


def cargar_piloto(nombre_piloto):
    return pd.read_csv(nombre_piloto + ".csv", index_col=0)


def pedir_piloto(msg, df_):
    while True:
        nombre_piloto = input(msg)

        if nombre_piloto == "terminar":
            return "terminar"

        if nombre_piloto.isdecimal():
            print("Detectado índice de piloto")
            if df_.loc[int(nombre_piloto)].empty:
                print("Error: Ingrese un índice válido")
            else:
                nombre_piloto = df_.loc[int(nombre_piloto)]["Piloto"]
                break

        if df_.loc[df_['Piloto'] == nombre_piloto].empty:
            print("Error: Ingrese un piloto válido")
        else:
            break

    return nombre_piloto


def pedir_stat(msg, df_):
    while True:
        try:
            nombre_stat = input(msg)

            if nombre_stat == "terminar":
                return "terminar"

            _ = df_[nombre_stat].to_list()
            return nombre_stat
        except:
            print("Ingresa el nombre de una estadística válida")



while opcion != 4:
    print("Menu de opciones: \n"
          "    1. Consultar estadísticas\n"
          "    2. Agregar datos de nueva carrera\n"
          "    3. Eliminar todo\n"
          "    4. Salir\n"
    )

    opcion = try_int("Ingrese una opción: ")

    if opcion == 1:
        print(df)

        print("Selección de pilotos:\n"
              "Ingrese el nombre de los pilotos que desee o 'terminar' para continuar")

        df_pilotos = []
        while True:
            piloto = pedir_piloto("Ingrese el nombre o id del piloto: ", df)

            if piloto == "terminar":
                break

            df_pilotos += [(piloto, cargar_piloto(piloto))]

        if not df_pilotos:
            exit(0)

        for piloto in df_pilotos:
            print(piloto[0])
            print(piloto[1])

        if input("Deseas graficar una estadística en específico: [si|no]").lower() == "si":
            print("Selección de stats:\n"
                  "Ingrese el nombre de las estadísticas que desee graficar o 'terminar' para continuar")

            df_stats = []
            while True:
                stat = pedir_stat("Ingrese una estadística a graficar: ", df_pilotos[0][1])

                if stat == "terminar":
                    break

                df_stats += [stat]

            carreras = list(range(1, carrera + 1))

            if not df_stats:
                exit(0)

            for stat in df_stats:
                fig, ax = plt.subplots()
                for piloto in df_pilotos:
                    ax.plot(carreras, piloto[1][stat].to_list())

                ax.set_title(stat, loc='center', fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
                plt.show()

