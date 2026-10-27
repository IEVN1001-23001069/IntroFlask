from blueprint.alumnos.routes import alumnos_bp
from blueprint.maestros.routes import maestros_bp
 
 
def registrar_blueprint(app):
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(maestros_bp)
 