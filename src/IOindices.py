from flask import Flask, jsonify, request, Blueprint
from pymongo import MongoClient
import pandas as pd
import pymongo
from variables import insumos
from engine import db
from conexionmongo import dataframeToMongo, retornarEngine, crearColeccion, mongoToDataframe, mongoToJson, requestToMongo
from calculosdris import calcularIndices
from cargadatos import ingresoDeDatos

IO_indices = Blueprint('IO_indices', __name__, url_prefix = '/indices')

@IO_indices.route('/', methods = ['POST'])
def retornar_indices():
    df =  mongoToDataframe(db)
    archivo = request.files['file']
    relaciones_muestra, nutrientes = ingresoDeDatos(archivo, insumos['nutrientes_moviles'], insumos['nutrientes_no_moviles'], delimitador = ',')
    print(relaciones_muestra.head())
    df = pd.concat([df, relaciones_muestra])
    print(df.head())
    indices = calcularIndices(df)
    return indices.to_json(orient="columns")

'''
archivo = request.files['file']
relaciones_muestra, nutrientes = ingresoDeDatos(archivo, nutrientes_moviles, nutrientes_no_moviles, delimitador = ',')
df = pd.concat([df, relaciones_muestra])

'''
