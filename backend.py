from flask import Flask, Response, request
from datetime import datetime
from datahandler import *
from os import system

app = Flask(__name__,
            static_folder='public',
            template_folder='templates')

@app.route("/listmaps.jsp")
def listmaps():
    return Response(getusermaps(request.args['user']))

@app.route("/level/save.html", methods=['POST'])
def savelevel():
    username = None
    session_id = None
    map_id = None
    map_length = None
    map_name = None

    try:
        request_data = request.stream.read()

        username_length = int.from_bytes(request_data[1 : 2], byteorder='big')
        username = request_data[2 : 2 + username_length]
        session_id_length = int.from_bytes(request_data[2 + username_length + 1 : 2 + username_length + 2], byteorder='big')
        session_id = request_data[2 + username_length + 2 : 2 + username_length + 2 + session_id_length]
        map_name_length = int.from_bytes(request_data[2 + username_length + 2 + session_id_length + 1 : 2 + username_length + 2 + session_id_length + 2], byteorder='big')
        map_name = request_data[2 + username_length + 2 + session_id_length + 2 : 2 + username_length + 2 + session_id_length + 2 + map_name_length]
        map_id = request_data[2 + username_length + 2 + session_id_length + 2 + map_name_length]
        map_length = int.from_bytes(request_data[2 + username_length + 2 + session_id_length + 2 + map_name_length + 1 : 2 + username_length + 2 + session_id_length + 2 + map_name_length + 1 + 4], byteorder='big')
        map_data = request_data[2 + username_length + 2 + session_id_length + 2 + map_name_length + 1 + 4 : len(request_data)]

        username = str(username, 'utf-8')
        session_id = str(session_id, 'utf-8')
        map_name = str(map_name, 'utf-8')

        version = 2 if map_data[0:2] == bytes([0x1F, 0x8B]) else 1
    except:
        return Response("Something went wrong!", 500)

    try:
        map_json_data = {
            "name": map_name,
            "length": map_length,
            "data": None,
            "createdAt": str(datetime.utcnow()),
            "version": version
        }
        updateusermap(username, map_id, map_json_data)
        saveusermap(username, map_id, map_data)
    except:
        return Response("Failed to save data.", 500)

    return Response("ok")

@app.route("/level/load.html")
def loadlevel():
    response = Response(bytes([0x00, 0x02, 0x6F, 0x6B]) + getusermapdata(request.args['user'], request.args['id']), mimetype='application/x-mine')
    return response

if __name__ == '__main__':
    system(f"title Minecraft Classic Backend")
    app.run(host="0.0.0.0", port=80)
