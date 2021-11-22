from flask import Flask, Response, request
from datetime import datetime
from datahandler import *
from os import system

app = Flask(__name__,
            static_folder='resources',
            template_folder='templates')

@app.route("/listmaps.jsp")
def listmaps():
    return Response(getusermaps(request.args['user']))

@app.route("/level/save.html", methods=['POST'])
def savelevel():
    username = None
    sessionId = None
    mapId = None
    mapLength = None
    mapName = None

    try:
        requestData = request.stream.read()

        username_length = int.from_bytes(requestData[1 : 2], byteorder='big')
        username = requestData[2 : 2 + username_length]
        sessionId_length = int.from_bytes(requestData[2 + username_length + 1 : 2 + username_length + 2], byteorder='big')
        sessionId = requestData[2 + username_length + 2 : 2 + username_length + 2 + sessionId_length]
        mapName_length = int.from_bytes(requestData[2 + username_length + 2 + sessionId_length + 1 : 2 + username_length + 2 + sessionId_length + 2], byteorder='big')
        mapName = requestData[2 + username_length + 2 + sessionId_length + 2 : 2 + username_length + 2 + sessionId_length + 2 + mapName_length]
        mapId = requestData[2 + username_length + 2 + sessionId_length + 2 + mapName_length]
        mapLength = int.from_bytes(requestData[2 + username_length + 2 + sessionId_length + 2 + mapName_length + 1 : 2 + username_length + 2 + sessionId_length + 2 + mapName_length + 1 + 4], byteorder='big')
        mapData = requestData[2 + username_length + 2 + sessionId_length + 2 + mapName_length + 1 + 4 : len(requestData)]

        username = str(username, 'utf-8')
        sessionId = str(sessionId, 'utf-8')
        mapName = str(mapName, 'utf-8')

        version = 2 if mapData[0:2] == bytes([0x1F, 0x8B]) else 1
    except:
        return Response("Something went wrong!", 500)

    try:
        mapJsonData = {
            "name": mapName,
            "length": mapLength,
            "data": f"./maps/{username}_{mapId}.dat",
            "createdAt": str(datetime.utcnow()),
            "version": version
        }
        updateusermap(username, mapId, mapJsonData)
        saveusermap(username, mapId, mapData)
    except:
        return Response("Failed to save data.", 500)

    return Response("ok")

@app.route("/level/load.html")
def loadlevel():
        response = Response(bytes([0x00, 0x02, 0x6F, 0x6B]) + getusermapdata(request.args['user'], request.args['id']), mimetype='application/x-mine')
        return response

if __name__ == '__main__':
    system("title Minecraft Classic API Remake")
    app.run(host='0.0.0.0', port=80)
