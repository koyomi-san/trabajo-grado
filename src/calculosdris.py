import pandas as pd
import numpy as np





def calcularIndices(df_relaciones):
    # preparacion
    nutrientes = list(df_relaciones.columns[3:13])

    df_indices = pd.DataFrame(columns = nutrientes)

    cantidadRelacionesNutriente, nutrientesRegex = conteoRelaciones(nutrientes, df_relaciones.columns[14:])
    funcion_altoRendimiento = calcularFunciones(df_relaciones)



    for i in range(len(nutrientes)):
        df_indices[nutrientes[i]] = funcion_altoRendimiento.filter(regex = nutrientesRegex[i]).sum(axis=1)/cantidadRelacionesNutriente[nutrientes[i]]
    
    return df_indices

def conteoRelaciones(nutrientes, relaciones):

    apariciones = len(nutrientes)*[0]
    cantidadRelacionesNutriente = dict(zip(nutrientes, apariciones))

    nutrientesRegex = [nutriente + ":" for nutriente in nutrientes]
    
    for nutriente in nutrientes:
        for relacion in relaciones:
            if relacion.startswith(nutriente):
                cantidadRelacionesNutriente[nutriente] = cantidadRelacionesNutriente[nutriente] + 1

    return cantidadRelacionesNutriente, nutrientesRegex

def calcularFunciones(df, proporcion = 0.78, variable = "Pr"):
    dfPoblacion_altoRendimiento = extraerPoblacion(df, proporcion = proporcion, variable = variable)
    relacionesMovilesNoMoviles = list(dfPoblacion_altoRendimiento.columns[14:])

    matrizPromedio, matrizCoefVariacion = promediosYCoefVariacion(dfPoblacion_altoRendimiento, relacionesMovilesNoMoviles)

    indicesParcialesMayor = calcularIndicesParcialesMayor(dfPoblacion_altoRendimiento, relacionesMovilesNoMoviles, matrizPromedio, matrizCoefVariacion)
    indicesParcialesMenor = calcularIndicesParcialesMenor(dfPoblacion_altoRendimiento, relacionesMovilesNoMoviles, matrizPromedio, matrizCoefVariacion)
    
    return indicesParcialesMayor + indicesParcialesMenor

def extraerPoblacion(df, proporcion = 0.78, variable = "Pr", poblacion = "alto rendimiento"):
    quantil = df[variable].quantile(proporcion)

    # alto o bajo rendimiento
    if poblacion == "alto rendimiento":
        mascara = calcularMascara(df[variable], quantil)
    else:
        mascara = calcularMascara(quantil, df[variable])
    

    dfPoblacion = df[mascara]
    return dfPoblacion

def calcularMascara(mayor, menor):
    mascara = mayor >= menor
    return mascara

def promediosYCoefVariacion(df, relaciones):  
    df_relaciones = df[relaciones]
    filas, columnas = df_relaciones.shape
    # el promedio esta vacio y el df solo tiene los nutrientes
    promedio = df_relaciones.mean()
    matrizPromedios = pd.DataFrame(np.ones((filas, columnas)), columns = relaciones)*promedio

    coefVariacion = df_relaciones.std()/np.abs(promedio)
    matrizCoefVariacion = pd.DataFrame(np.ones((filas, columnas)), columns = relaciones)*coefVariacion

    return matrizPromedios, matrizCoefVariacion

def calcularIndicesParcialesMayor(df, relaciones, promedios, coefVariaciones):
    df_relaciones = df[relaciones].reset_index(drop=True) 
    comparacion = (df_relaciones.reset_index(drop=True) >= promedios)
    
    razonRelacionPromedio = (df_relaciones/promedios - 1).reset_index(drop=True)
    razonRelacionPromedio.fillna(0)

    indicesParciales = comparacion*razonRelacionPromedio/coefVariaciones
    indicesParciales.fillna(0)
    return indicesParciales

def calcularIndicesParcialesMenor(df, relaciones, promedios, coefVariaciones):
    df_relaciones = df[relaciones].reset_index(drop=True) 
    comparacion = (df_relaciones.reset_index(drop=True) < promedios)

    razonRelacionPromedio = (1 - promedios/df_relaciones).reset_index(drop=True)
    razonRelacionPromedio.fillna(0)

    indicesParciales = comparacion*razonRelacionPromedio/coefVariaciones
    indicesParciales.fillna(0)
    return indicesParciales