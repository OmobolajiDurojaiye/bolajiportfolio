def register_blueprints(app):
    from .main import main_bp
    from .admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
