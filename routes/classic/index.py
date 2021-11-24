from routes.classic.levels import register_routes as register_levels_routes
from routes.classic.skins import register_routes as register_skins_routes

def register_routes(app):
    register_levels_routes(app)
    register_skins_routes(app)