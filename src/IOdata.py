from flask import Flask, jsonify, request, Blueprint
from pymongo import MongoClient
import pandas as pd
import pymongo
from variables import insumos
from engine import db
from conexionmongo import dataframeToMongo, retornarEngine, crearColeccion, mongoToDataframe, mongoToJson, requestToMongo


IO = Blueprint('IO', __name__, url_prefix = '/data')

@IO.route('/', methods = ['GET'])
def prueba():
    print("prueba2")
    return jsonify({"response": "hello world"})

@IO.route('/coleccion')
def crearColeccion():
    # Create a new collection in MongoDB
    try:
        db.create_collection('relaciones')
        return 'Collection created'
    except:
        return "la coleccion ya existe"
    # Return a message indicating that the collection was created
    

@IO.route('/relaciones')
def get_relaciones():
    # Retrieve all documents from the users collection
    excluidos = {"_id": 0}
    relaciones = list(db.relaciones.find({}, excluidos))

    # Convert the list of user documents to a JSON response
    response = {'relaciones': []}
    for relacion in relaciones:
        response['relaciones'].append(str(relacion))

    # Return the JSON response
    return jsonify(response)

@IO.route('/relaciones', methods=['POST'])
def agregar_relaciones():
    #.get_json()
    print('iii')
    print(request.files.keys())
    requestToMongo(db, request)

    return 'Success'


@IO.route('/insumos', methods=['POST'])
def setInsumos():
    
    temp = request.get_json() 

    insumos["nutrientes_no_moviles"] = temp["nutrientes_no_moviles"]
    insumos["nutrientes_moviles"] = temp["nutrientes_moviles"]
    insumos["proporcion"] = temp["proporcion"]
    insumos["variable"] = temp["variable"]

    return jsonify({'success': True})

@IO.route('/insumos', methods=['GET'])
def getInsumos():
    return jsonify(insumos)

@IO.route('/borrar', methods=['DELETE'])
def borrar():

    db.relaciones.delete_many({})

    return 'borrado'