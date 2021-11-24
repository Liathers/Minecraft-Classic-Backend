def register_routes(app):
    from routes.legacy import register_routes as register_legacy_routes

    register_legacy_routes(app)
