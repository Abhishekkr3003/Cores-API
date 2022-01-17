import pymysql
from flask import Blueprint, request, jsonify

from config import bcrypt, mysql

adminRoutes = Blueprint('admin_routes', __name__)


@adminRoutes.route("/list")
def list_admins():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM admin"
        cursor.execute(query)
        rows = cursor.fetchall()
        # print(rows[0]["userId"])
        response = jsonify(rows)
        response.status_code = 200

    except Exception as e:
        print(e)
        response = str(e)
        response.status_code = 500

    finally:
        cursor.close()
        conn.close()
        return response


@adminRoutes.route("/register", methods=['POST'])
def add_admin():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _json = request.json
        _passw = _json['passw']
        _userId = _json['userId']
        _name = _json['name']
        _hash_pw = bcrypt.generate_password_hash(_passw, 10)
        sqlQuery = "INSERT INTO admin VALUES (%s, %s, %s);"
        bindData = (_userId, _name, _hash_pw)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = jsonify('success')
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@adminRoutes.route("/verify", methods=["POST"])
def verify_admin():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _json = request.json
        _passw = _json['passw']
        _userId = _json['userId']
        query = "SELECT * FROM admin WHERE userId=%s"
        bindData = (_userId)
        cursor.execute(query, bindData)
        row = cursor.fetchone()
        if row is None:
            response = jsonify("User Not Found")
            return response
        else:
            if bcrypt.check_password_hash(row["passw"], _passw):
                response = {
                    "name": row['name'],
                    "userId": row['userId']
                }
                return response
            else:
                return jsonify("Incorrect Password")
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@adminRoutes.route("/updatePassword", methods=["POST"])
def update_password():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _json = request.json
        _passw = _json['passw']
        _new_pass = _json['newpassw']
        _userId = _json['userId']
        query = "SELECT * FROM admin WHERE userId=%s"
        bindData = (_userId)
        cursor.execute(query, bindData)
        row = cursor.fetchone()
        if row is None:
            response = jsonify("User Not Found")
            return response
        else:
            if bcrypt.check_password_hash(row["passw"], _passw):
                _new_pass_hash = bcrypt.generate_password_hash(_new_pass, 10)
                query = "UPDATE admin SET passw=%s WHERE userId=%s"
                bindData = (_new_pass_hash, _userId)
                cursor.execute(query, bindData)
                conn.commit()
                response = jsonify("Success")
                return response
            else:
                return jsonify("Incorrect Password")
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()

