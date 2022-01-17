import pandas as pd
import pymysql
from flask import Blueprint, jsonify, request

from config import mysql, bcrypt

studentRoutes = Blueprint('student_routes', __name__)


@studentRoutes.route("/list", methods=['GET'])
def list_students():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM student"
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


@studentRoutes.route("/register", methods=['POST'])
def add_student():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _json = request.json
        _passw = _json['passw']
        _userId = _json['userId']
        _name = _json['name']
        _join_year = _json['joining_year']
        _branch = _json['Branch']
        _hash_pw = bcrypt.generate_password_hash(_passw, 10)
        sqlQuery = "INSERT INTO student VALUES (%s, %s, %s, %s, %s);"
        bindData = (_userId, _name, _join_year, _branch, _hash_pw)
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


@studentRoutes.route("/registerMultiple", methods=["POST"])
def register_multiple_students():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        file = request.files['file']
        data = pd.read_excel(file)
        print(data)
        print("here")
        query = "INSERT INTO student VALUES (%s, %s, %s, %s, %s)"
        success_count = 0
        failure_count = 0
        for row in data.index:
            try:
                _userId = data['userId'][row]
                _name = data['name'][row]
                _joining_year = data['joining_year'][row]
                _Branch = data['Branch'][row]
                _passw = data['passw'][row]
                _hash_pw = bcrypt.generate_password_hash(str(_passw), 10)
                bindData = (_userId, _name, _joining_year, _Branch, _hash_pw)
                cursor.execute(query, bindData)
                success_count += 1
            except Exception as e:
                print(e)
                failure_count += 1
        conn.commit()
        return jsonify(f"{success_count} students added, {failure_count} failed to add")

    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@studentRoutes.route("/verify", methods=["POST"])
def verify_student():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _json = request.json
        _passw = _json['passw']
        _userId = _json['userId']
        query = "SELECT * FROM student WHERE userId=%s"
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
                    "joining_year": row['joining_year'],
                    "Branch": row['Branch'],
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


@studentRoutes.route("/updatePassword", methods=["POST"])
def update_password():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _json = request.json
        _passw = _json['passw']
        _new_pass = _json['newpassw']
        _userId = _json['userId']
        query = "SELECT * FROM student WHERE userId=%s"
        bindData = (_userId)
        cursor.execute(query, bindData)
        row = cursor.fetchone()
        if row is None:
            response = jsonify("User Not Found")
            return response
        else:
            if bcrypt.check_password_hash(row["passw"], _passw):
                _new_pass_hash = bcrypt.generate_password_hash(_new_pass, 10)
                query = "UPDATE student SET passw=%s WHERE userId=%s"
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


@studentRoutes.route("/delete", methods=["POST"])
def delete_student():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "delete from courseEnrollment where student_id=%s"
        cursor.execute(query, (request.json['userId']))
        query = "delete from student where userid=%s;"
        cursor.execute(query, (request.json['userId']))
        conn.commit()
        return "success"
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@studentRoutes.route("/update", methods=["POST"])
def update():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "update student set name=%s, joining_year=%s, branch=%s where userid=%s"
        cursor.execute(query, (
            request.json['name'], request.json['joining_year'], request.json['Branch'], request.json['userId']))
        conn.commit()
        return "success"
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@studentRoutes.route("/getStudentsByBranch", methods=["POST"])
def student_list_by_branch():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "select * from student where branch=%s"
        cursor.execute(query, (request.json['Branch']))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@studentRoutes.route("/getStudentsByYear", methods=["POST"])
def student_list_by_joining_year():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "select * from student where joining_year=%s"
        cursor.execute(query, (request.json['joining_year']))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()
