def register_routes(app):
    from routes.classic import register_routes as register_classic_routes

    register_classic_routes(app)
