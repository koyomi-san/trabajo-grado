import numpy as np
import os
import pandas as pd






# funcion principal

def ingresoDeDatos(ruta, nutrientes_moviles, nutrientes_no_moviles, delimitador = ','):
    
    # carga df
    df, nutrientes = cargarDf(ruta, delimitador)

    # relaciones moviles
    dfRelaciones_moviles, relaciones_moviles = dfRelacionesDivision(df, nutrientes_moviles)

    # relaciones no moviles
    dfRelaciones_noMoviles, relaciones_noMoviles = dfRelacionesDivision(df, nutrientes_no_moviles)

    # relaciones moviles - no moviles
    dfRelaciones_moviles_noMoviles, relaciones = dfRelacionesMovilesNoMoviles(df, nutrientes_moviles, nutrientes_no_moviles)

    # construir bd !!!!!!
    df_relaciones = pd.concat([df, dfRelaciones_moviles, dfRelaciones_noMoviles, dfRelaciones_moviles_noMoviles], axis=1)
    df_relaciones[df_relaciones.columns[2:]] = df_relaciones[df_relaciones.columns[2:]].round(3)
    

    return df_relaciones, nutrientes

# df

def cargarDf(ruta, delimitador = ","):
    df = pd.read_csv(ruta, delimiter = delimitador)
    nutrientes = list(df.columns)[3:]
    return df, nutrientes

def dataframeRelaciones(matrizA, matrizB, relaciones):
    dfRelaciones = pd.DataFrame(
                            calcularRelaciones(matrizA, matrizB),
                            columns = relaciones) 
    return dfRelaciones, relaciones

def dfRelacionesDivision(df, nutrientes):
    matrixA = df[nutrientes] 
    matrixB = 1/df[nutrientes] 
    relaciones = nombresRelaciones(nutrientes)
    dfRelaciones, relaciones = dataframeRelaciones(matrixA, matrixB, relaciones)
    return dfRelaciones, relaciones

def dfRelacionesMovilesNoMoviles(df, nutrientes_moviles, nutrientes_no_moviles):
    df_uraba_moviles = df[nutrientes_moviles]
    df_uraba_noMoviles = df[nutrientes_no_moviles]

    relaciones = nombresRelacionesMovilesNoMoviles(nutrientes_moviles, nutrientes_no_moviles)

    arrayRelaciones = calcularRelacionesMovilesNoMoviles(df_uraba_moviles, df_uraba_noMoviles)

    dfRelaciones = pd.DataFrame(arrayRelaciones, columns = relaciones)
    return dfRelaciones, relaciones

# calculos

def calcularRelaciones(matrizA, matrizB):
    # matriz de relaciones
    filas, columnas = matrizA.shape
    

    # calculo de kronecker (revisar optimizacion para calcular solo filas necesarias)
    kronecker = np.kron(matrizA, matrizB)
    filasKronecker, columnasKronecker = kronecker.shape

    # filtrado de filas y columnas
    filasIncluidas = np.linspace(0, filasKronecker - 1, filas, dtype = np.int16) # filas a incluir
    columnasBorradas = np.linspace(0, columnasKronecker - 1, columnas, dtype = np.int16) # columnas a borrar
    
    columnasRelaciones = columnas**2 - len(columnasBorradas)

    relaciones = np.zeros((filas, columnasRelaciones))
    relaciones = np.delete(kronecker, columnasBorradas, axis = 1)[filasIncluidas, :]

    return relaciones

def calcularRelacionesMovilesNoMoviles(matrizA, matrizB):
    kronecker = np.kron(matrizA, matrizB)
    filas, columnas = matrizB.shape
    filasKronecker, columnasKronecker = kronecker.shape

    # filtrado de filas y columnas
    filasIncluidas = np.linspace(0, filasKronecker - 1, filas, dtype = np.int16) # filas a incluir
    Relaciones = kronecker[filasIncluidas, :]
    return Relaciones


# utilidades

def nombresRelaciones(nutrientes):
    relaciones = []
    for i in nutrientes:
        for j in nutrientes:
            if i == j:
                pass
            else:
                relaciones = relaciones + ["{0}:{1}".format(i, j)]
    return relaciones

def nombresRelacionesMovilesNoMoviles(moviles, noMoviles):
    relaciones = []
    numRelaciones = len(moviles)*len(noMoviles)
    for i in moviles:
        for j in noMoviles:
            relaciones = relaciones + ["{0}:{1}".format(i, j)]
    return relaciones


