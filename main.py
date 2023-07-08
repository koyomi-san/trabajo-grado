# python3 main.py
import sys
import numpy as np
import os
import pandas as pd
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(0, './src/cargadatos')
sys.path.insert(1, './src/adaptadormongo')

from cargadatos import ingresoDeDatos
from conexionmongo import dataframeToMongo, retornarEngine, crearColeccion, mongoToDataframe, mongoToJson

# insumos
# carga de archivos
carpeta_principal = "./data"
archivo_uraba = "Foliar_Pr_U.csv"
delimitador = ','

# columnas de interes
nutrientes_no_moviles = ["Ca","Fe","Mn","Cu","Zn","B"]
nutrientes_moviles = ["N","P","K","Mg","S"]


# filtros
proporcion = 0.78
variable = "Pr"

# ajustes
ruta_uraba = carpeta_principal + "/" + archivo_uraba

# preparar df
df_relaciones, nutrientes = ingresoDeDatos(ruta_uraba, nutrientes_moviles, nutrientes_no_moviles, delimitador = delimitador)


coleccion = 'relaciones'
host = "localhost"

# conectarse a la db
db = retornarEngine(host)


if False:
    print(crearColeccion(db, coleccion))


if False:
    print(dataframeToMongo(db, df_relaciones, coleccion))

#df = mongoToDataframe(db)

# guardar df
#df.to_csv("./data/generados/fromMongo.csv")


"""
python3 /home/araragi/Documents/tesis/python/trabajo-grado/main.py
"""