import pandas as pd
import pymysql
from flask import Blueprint, jsonify, request

from config import mysql

courseRoutes = Blueprint('course_routes', __name__)


@courseRoutes.route("/list")
def list_courses():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM course"
        cursor.execute(query)
        rows = cursor.fetchall()
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


@courseRoutes.route("/addNewCourse", methods=['POST'])
def add_new_course():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _json = request.json
        _course_id = _json['course_id']
        _coursename = _json['coursename']
        _type = _json['type']
        _credits = _json['credits']
        sqlQuery = "INSERT INTO course VALUES (%s, %s, %s,%s);"
        bindData = (_course_id, _coursename, _type, _credits)
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


@courseRoutes.route("/addMultipleNewCourse", methods=["POST"])
def add_multiple_courses():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        file = request.files['file']
        data = pd.read_excel(file)
        print(data)
        query = "INSERT INTO course VALUES (%s, %s, %s, %s)"
        success_count = 0
        failure_count = 0
        for row in data.index:
            try:
                _courseId = data['course_id'][row]
                _name = data['coursename'][row]
                _type = data['type'][row]
                _credits = data['credits'][row]
                bindData = (_courseId, _name, _type, _credits)
                cursor.execute(query, bindData)
                success_count += 1
            except Exception as e:
                print(e)
                failure_count += 1
        conn.commit()
        return jsonify(f"{success_count} courses added, {failure_count} failed to add")

    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/updateCourses", methods=["POST"])
def update_course():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "UPDATE course SET coursename=%s, type=%s, credits=%s WHERE course_id=%s"
        cursor.execute(query, (
            request.json['coursename'], request.json['type'], request.json['credits'],
            request.json['course_id']))
        conn.commit()
        return "success"
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/deleteCourse", methods=["POST"])
def delete_course():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "DELETE FROM availableCourses WHERE course_id= %s"
        cursor.execute(query, (request.json['course_id']))
        query = "DELETE FROM courseEnrollment WHERE course_id= %s"
        cursor.execute(query, (request.json['course_id']))
        query = "DELETE FROM course WHERE course_id=%s"
        cursor.execute(query, (request.json['course_id']))
        conn.commit()
        return "success"
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/addAvailableCourse", methods=['POST'])
def add_available_course():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlQuery = "INSERT INTO availableCourses VALUES (%s, %s, %s, %s, %s, %s);"
        bindData = (
            request.json['course_id'], request.json['semester'], request.json['branch'], request.json['totalSeats'],
            request.json['totalSeats'], request.json['grp'])
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        return jsonify('success')
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/updateTotalSeats", methods=["POST"])
def update_Total_Seats():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "UPDATE availableCourses SET availableSeats=%s, totalSeats=%s WHERE course_id=%s AND semester=%s AND branch=%s"
        cursor.execute(query, (
            request.json['totalSeats'], request.json['totalSeats'], request.json['course_id'], request.json['semester'],
            request.json['branch']))
        conn.commit()
        return "success"
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/getAvailableSeats", methods=["POST"])
def get_available_seats():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT availableSeats from availableCourses WHERE course_id=%s AND semester=%s AND branch=%s;"
        cursor.execute(query, (request.json['course_id'], request.json['semester'], request.json['branch']))
        row = cursor.fetchone()
        return jsonify(row['availableSeats'])

    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/decreaseAvailableSeats", methods=["POST"])
def decrease_available_seats():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT availableSeats from availableCourses WHERE course_id=%s AND semester=%s AND branch=%s;"
        cursor.execute(query, (request.json['course_id'], request.json['semester'], request.json['branch']))
        row = cursor.fetchone()
        if row['availableSeats'] == 0:
            return jsonify("Seats Not Available")
        else:
            query = "UPDATE availableCourses SET availableSeats=%s WHERE course_id=%s AND semester=%s AND branch=%s"
            cursor.execute(query, (row['availableSeats'] - 1, request.json['course_id'], request.json['semester'],
                                   request.json['branch']))
            conn.commit()
            return jsonify(row['availableSeats'] - 1)

    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/increaseAvailableSeats", methods=["POST"])
def increase_available_seats():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * from availableCourses WHERE course_id=%s AND semester=%s AND branch=%s;"
        cursor.execute(query, (request.json['course_id'], request.json['semester'], request.json['branch']))
        row = cursor.fetchone()
        if row['availableSeats'] == row['totalSeats']:
            return jsonify("Not Allowed")
        else:
            query = "UPDATE availableCourses SET availableSeats=%s WHERE course_id=%s AND semester=%s AND branch=%s"
            cursor.execute(query, (row['availableSeats'] + 1, request.json['course_id'], request.json['semester'],
                                   request.json['branch']))
            conn.commit()
            return jsonify(row['availableSeats'] + 1)

    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/deleteAllAvailableCourse", methods=["POST"])
def delete_all_available_courses():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "TRUNCATE TABLE availableCourses"
        cursor.execute(query)
        conn.commit()
        return jsonify("success")
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/courseAvailibility", methods=["POST"])
def course_availability():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM availableCourses WHERE course_id=%s"
        cursor.execute(query, (request.json['course_id']))
        rows = cursor.fetchall()
        if len(rows) == 0:
            return jsonify("No Data Available")
        else:
            return jsonify(rows)
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/availableCoursesInSem", methods=["POST"])
def available_courses_sem():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM availableCourses WHERE semester=%s"
        cursor.execute(query, (request.json['semester']))
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/availableCoursesForBranch", methods=["POST"])
def available_courses_branch():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM availableCourses WHERE branch=%s"
        cursor.execute(query, (request.json['branch']))
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/getCoreCourses", methods=["POST"])
def get_core_courses():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "select tbl1.course_id, coursename, credits from ( select * from course where type='CORE' ) tbl1 inner join ( select * from availableCourses where semester=%s and branch=%s ) tbl2 on tbl1.course_id = tbl2.course_id;"
        cursor.execute(query, (request.json['semester'], request.json['branch']))
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/getElectiveCourses", methods=["POST"])
def get_elective_courses():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "select tbl1.course_id, coursename, credits, availableseats, grp from ( select * from course where type='ELECTIVE' ) tbl1 inner join ( select * from availableCourses where semester=%s and branch=%s ) tbl2 on tbl1.course_id = tbl2.course_id;"
        cursor.execute(query, (request.json['semester'], request.json['branch']))
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/addEnrollment", methods=["POST"])
def add_enrollment():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "insert into courseEnrollment values (%s, %s);"
        cursor.execute(query, (request.json['course_id'], request.json['student_id']))
        conn.commit()
        return jsonify("success")
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/deleteEnrollment", methods=["POST"])
def delete_enrollment():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "delete from courseEnrollment where course_id=%s and student_id=%s"
        cursor.execute(query, (request.json['course_id'], request.json['student_id']))
        conn.commit()
        return jsonify("success")
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()


@courseRoutes.route("/isEnrolledInCourse", methods=["POST"])
def is_enrolled_in_course():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "select * from courseEnrollment where course_id=%s and student_id=%s;"
        cursor.execute(query, (request.json['course_id'], request.json['student_id']))
        row = cursor.fetchone()
        if row is None:
            return jsonify(False)
        else:
            return jsonify(True)
    except Exception as e:
        return jsonify("Error: " + str(e)), 500
    finally:
        cursor.close()
        conn.close()
