import json
import os
import mysql.connector

# Connect database
def connect():

    curPath = os.path.dirname(__file__)
    dbVarsPath = os.path.join(curPath, "dbVars.json")
    dbVarsFile = open(dbVarsPath)
    dbVars = json.load(dbVarsFile)
    dbVarsFile.close()

    connection = mysql.connector.connect(
        host = dbVars["DB_HOST"],
        user = dbVars["DB_USERNAME"],
        password = dbVars["DB_PASSWORD"]
    )
    
    return connection