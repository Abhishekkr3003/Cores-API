# Cores-API

## Endpoints

## Student

| Type |                Route                |                            Path Parameters                             |                             Description                             |
| :--: | :---------------------------------: | :--------------------------------------------------------------------: | :-----------------------------------------------------------------: |
| GET  |            /student/list            |                                   -                                    |                Get all the entries in student table                 |
| POST |          /student/register          |         userId, name, joining_year, Student_DOB, Branch, passw         |                       Register a new student                        |
| POST |      /student/registerMultiple      | .xlsx file of (userId, name, joining_year, Student_DOB, Branch, passw) |                     Register multiple students                      |
| POST |           /student/verify           |                             userId, passw                              |                    Verify password for a student                    |
| POST |       /student/updatePassword       |                        userId, passw, newpassw                         |      update password with new password using existing password      |
| POST |           /student/delete           |                                 userId                                 |                           Delete student                            |
| POST |           /student/update           |            userId, name, joining_year, Student_DOB, Branch             |                           Update student                            |
| POST |    /student/getStudentsByBranch     |                                 Branch                                 |                 List of students with given branch                  |
| POST |     /student/getStudentsByYear      |                              joining_year                              |              List of students with given Joining Year               |

## Admin

| Type |         Route         |     Path Parameters      |                        Description                        |
| :--: | :-------------------: | :----------------------: | :-------------------------------------------------------: |
| GET  |      /admin/list      |            -             |            Get all the entries in admin table             |
| POST |    /admin/register    | userId, name, DOB, passw |                   Register a new admin                    |
| POST |     /admin/verify     |      userId, passw       |                Verify password for a admin                |
| POST | /admin/updatePassword | userId, passw, newpassw  | update password with new password using existing password |

## Course

| Type |               Route                |                        Path Parameters                        |                                       Description                                        |
| :--: | :--------------------------------: | :-----------------------------------------------------------: | :--------------------------------------------------------------------------------------: |
| GET  |            /course/list            |                               -                               |                           Get all the entries in course table                            |
| POST |        /course/addNewCourse        |             course_id, coursename, type, credits              |                              Add New course in course table                              |
| POST |    /course/addMultipleNewCourse    |     .xlsx file of ( course_id, coursename, type, credits)     |                         Add Multiple New course in course table                          |
| POST |        /course/updateCourse        |             course_id, coursename, type, credits              |                          Update Exisitng course in course table                          |
| POST |        /course/deleteCourse        |                           course_id                           | Delete all entries of course_id from courseEnrollment, availableCourses and course table |
| POST |     /course/addAvailableCourse     |         course_id, semester, branch, totalSeats, grp          |               Add new availibility for a course in availableCourses table                |
| POST |     /course/getAvailableSeats      |                  course_id, semester, branch                  |                             Get Seats available for a course                             |
| POST |   /course/decreaseAvailableSeats   |                  course_id, semester, branch                  |                   Decreases seats available in a course by 1 if not 0                    |
| POST |   /course/increaseAvailableSeats   |                  course_id, semester, branch                  |                        Increases seats available in a course by 1                        |
| POST |      /course/updateTotalSeats      |                  course_id, semester, branch                  |                                    Update Total Seats                                    |
| GET  |  /course/deleteAllAvailableCourse  |                               -                               |                      Delete all entries in availableCourses tables                       |
| POST |     /course/courseAvailibility     |                           course_id                           |                  Get all different availibility for a particular course                  |
| POST |   /course/availableCoursesInSem    |                           semester                            |                              Get all courses in a semester                               |
| POST | /course/availableCoursesForBranch  |                            branch                             |                               Get all courses for a branch                               |
| POST |       /course/getCoreCourses       |                        branch,semester                        |                 Get list of all the Core courses for a sem branch combo                  |
| POST |     /course/getElectiveCourses     |                        branch,semester                        |               Get list of all the elective courses for a sem branch combo                |
| POST |       /course/addEnrollment        |                     student_id, course_id                     |                               Add Enrollment for a student                               |
| POST |      /course/deleteEnrollment      |                     student_id, course_id                     |                             Delete Enrollment for a student                              |
| POST |     /course/isEnrolledInCourse     |                     student_id, course_id                     |                If student is enrolled in a course return true else false                 |

---

# Database Design

![Database Design](/assets/dbdesign.png)

---

## Env Variable

```
CORES_USERNAME=""
CORES_PASSWORD=""
CORES_DB_NAME=""
CORES_DB_HOST=""                                    
```

---

# Tech Used

- Flask
- Python3
- MySQL

---

# Links

[Mobile App Code](https://github.com/Abhishekkr3003/Course-Registration)
