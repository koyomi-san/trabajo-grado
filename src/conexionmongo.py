import pandas as pd
from pymongo import MongoClient
from flask import jsonify
import pymongo


from cargadatos import ingresoDeDatos
from variables import insumos



def requestToMongo(db, request, coleccion = 'relaciones'):
    print("aaa")
    file = request.files['file']
    print("bbb")
    # df = pd.read_csv(file)
    df_relaciones, nutrientes = ingresoDeDatos(file, insumos['nutrientes_moviles'], insumos['nutrientes_no_moviles'])
    dataframeToMongo(db, df_relaciones, coleccion)
    return "datos insertados"

# guardar datos
def dataframeToMongo(db, df, coleccion = 'relaciones'):
    
    db[coleccion].insert_many(df.to_dict('records'))
    
    return 'Datos insertados'

# retornar datos 
def mongoToDataframe(db, coleccion = 'relaciones'):
    
    df = pd.DataFrame(list(db[coleccion].find()))
    df = df[df.columns[2:]]
    return df



def mongoToJson(db, excluidos, coleccion = "relaciones"):
    # Retrieve all documents from the users collection
    excluidos = {"_id": 0}
    relaciones = list(db.relaciones.find({}, excluidos))

    # Convert the list of user documents to a JSON response
    response = {coleccion: []}
    for relacion in relaciones:
        response['relaciones'].append(str(relacion))
    # Return the JSON response
    
    return jsonify(response)

# crear coleccion
def crearColeccion(db, nombreColeccion):
    # Create a new collection in MongoDB
    db.create_collection(nombreColeccion)

    # Return a message indicating that the collection was created
    return 'Collection created'

# retornar conexion a base de datos
def retornarEngine(nombreEngine, puerto = 27017):

    client = MongoClient(nombreEngine, puerto)
    db = client.mydatabase

    return db
