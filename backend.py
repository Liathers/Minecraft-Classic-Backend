from flask import Flask
from os import system
import routes

app = Flask(__name__,
            static_folder='public',
            template_folder='templates')

routes.register_routes(app)

if __name__ == '__main__':
    system(f"title Minecraft Classic Backend")
    app.run(host="0.0.0.0", port=80)
