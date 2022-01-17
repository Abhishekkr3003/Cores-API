import os

from flask import Flask

from config import mysql, bcrypt
from routes.admin_routes import adminRoutes
from routes.course_routes import courseRoutes
from routes.index import index
from routes.student_routes import studentRoutes


def create_app():
    app = Flask(__name__)
    app.config['MYSQL_DATABASE_USER'] = os.getenv("CORES_USERNAME")
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("CORES_PASSWORD")
    app.config['MYSQL_DATABASE_DB'] = os.getenv("CORES_DB_NAME")
    app.config['MYSQL_DATABASE_HOST'] = os.getenv("CORES_DB_HOST")
    mysql.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(adminRoutes, url_prefix='/admin')
    app.register_blueprint(studentRoutes, url_prefix='/student')
    app.register_blueprint(courseRoutes, url_prefix='/course')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
