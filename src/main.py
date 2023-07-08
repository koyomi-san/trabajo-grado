from flask import Flask, jsonify, request
from pymongo import MongoClient
import pymongo
import pandas as pd
import sys



from cargadatos import ingresoDeDatos
from conexionmongo import dataframeToMongo, retornarEngine, crearColeccion, mongoToDataframe, mongoToJson

from IOdata import IO
from IOindices import IO_indices

from variables import insumos




app = Flask(__name__)
app.register_blueprint(IO)
app.register_blueprint(IO_indices)


host = "localhost"
#host = "0.0.0.0"
port = 80



if __name__ == "__main__":
    app.run(host = host, port = port, debug = False)
    


"""
python3 /home/araragi/Documents/tesis/python/trabajo-grado/src/main.py
"""