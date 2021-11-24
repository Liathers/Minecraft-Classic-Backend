from flask import Response, abort
import json
from io import BytesIO
from PIL import Image
import requests
import base64

''' Reguster skin routes '''
def register_routes(app):
    @app.route('/skin/<username>.png')
    @app.route('/MinecraftSkins/<username>.png')
    def skin(username):
        try:
            profile = json.loads(requests.get("https://api.mojang.com/users/profiles/minecraft/" + username).content)
            profile = json.loads(requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + profile["id"]).content)
            skinUrl = json.loads(base64.b64decode(profile["properties"][0]["value"]))["textures"]["SKIN"]["url"]
            skinBytes = BytesIO(requests.get(skinUrl).content)
            skinBytes.flush()
            skinBytes.seek(0)
            skin = Image.open(skinBytes)
            croppedSkin = BytesIO()
            skin = skin.crop((0, 0, 64, 32))
            skin.save(croppedSkin, "PNG")
            skinBytes.flush()
            croppedSkin.seek(0)

            response = Response(croppedSkin.read(), mimetype="image/png")
            
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            response.headers['Cache-Control'] = 'public, max-age=0'

            return response
        except Exception as e:
            abort(404)