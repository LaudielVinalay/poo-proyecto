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
    with open("datos.csv", "x+") as f, open("Conteo.csv", "x+") as g:
        f.write("Piloto")

        g.write("num_carreras\n")
        g.write("0")

        f.close()
        g.close()
        primer_corrida = True

df = pd.read_csv(file,  index_col=0)
conteo = pd.read_csv("Conteo.csv")

def crear_registro(nombre):
    with open(nombre+".csv", 'x+') as k:
        k.write("Posisión,Velocidad Media,Velocidad Max")
        k.close()

        return pd.read_csv(nombre+".csv")


def generar_posiciones(n_carreras, n_pilotos):
    carreras = []
    for _ in range(n_carreras):
        Posisións = [num + 1 for num in range(n_pilotos)]
        random.shuffle(Posisións)
        carreras.append(Posisións)

    return carreras


def generar_velocidades(n_carreras, n_pilotos):
    velocidades = []
    for _ in range(n_carreras):
        velocidades_de_carrera = [random.randrange(150, 250) for _ in range(n_pilotos)]
        velocidades_de_carrera.sort()
        velocidades.append(velocidades_de_carrera)

    return velocidades


if primer_corrida:
    print("Warning: Primera ejecución del programa detectada!")

    carrera: int = try_int("Ingrese el número de carreras que va a registrar por piloto: ")
    conteo.loc[conteo['num_carreras']] = carrera

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
                    "Posisión": [posiciones_carreras[j][i]],
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

while opcion != 6:
    print("Menu de opciones: \n"
          "    1. Consultar estadísticas\n"
          "    2. Agregar datos de nueva carrera\n"
          "    3. Eliminar todo\n"
          "    4. Salir\n"
    )

    opcion = try_int("Ingrese una opción: ")

    if opcion == 1:
        print(df)
        
        nombre = input("Ingrese el nombre del piloto del que desea conocer sus estadísticas: ")

        if df.loc[df['Piloto'] == nombre].empty:
            print("Error: Ingrese un piloto válido")
        else:
            df_piloto = pd.read_csv(nombre + ".csv", index_col=0)
            print(df_piloto)


fig, ax = plt.subplots()
velocidades=[]
carreras=[]
ax.plot(velocidades,carreras)
ax.set_title('Gráfica de velocidad promedio', loc='center', fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
plt.show()
