# OEMS (Online Education Management System) Backend

_This project serves as backend for [OEMS (Online Education Management System) frontend](https://github.com/VirajPatidar/oems-frontend)._

_Online Education Management System is a project that serves as the all-in-one place for teaching and learning.
Our easy-to-use and secure tools helps educators manage, measure, and enrich learning experiences._

<br/>

**Link to the website:** [https://oems.netlify.app/](https://oems.netlify.app/)
<br/>
**Link to frontend repo:** [https://github.com/VirajPatidar/oems-backend](https://github.com/VirajPatidar/oems-frontend)


### Tech Stack ###
* Django
* Django REST framework
* SQL
* simplejwt


### API Endpoints ###
**Authentication:**
| Method | URL | Description |
| :---         | :---         | :---         
| `POST`   | `/auth/register`     | To register or sign-up user (student and teacher)    |
| `GET`     | `/auth /email-verify`       |  To verify user's email      |
| `POST`     | `/auth/login`       |  To log into OEMS     |
| `POST`     | `/auth/token/refresh`       | To refresh access token by sending refresh token      |
| `POST`     | `/auth/logout`       |    To log out from OEMS   |
| `PATCH/PUT`     | `/auth/change-password`       | To change user’s password      |
| `POST`     | `/auth/request-reset-email`       | To post email to get password reset link      |
| `GET` | `/auth/password-reset/{uidb64}/{token}` | To Verify User using uidb64 and token |
| `PATCH` | `/auth /password-reset-complete` | To set new password |
| `PUT/PATCH` | `/auth /change-avatar` | To change user’s profile picture |

<br/>

**Class:**
| Method | URL | Description |
| :---         | :---         | :--- 
| `POST` | `/class/manage-class` | Used by teacher to create a class |
| `DELETE` | `/class/manage-class` | Used by teacher to delete a class |
| `POST` | `/class/member-class` | Used by student to join a class using joining code |
| `DELETE` | `/class/member-class` | Used by student to leave a class |
| `POST` | `/class/manage-student` | Used by teacher to add a student in a class |
| `DELETE` | `/class/manage-student` | Used by teacher to remove a student from a class |
| `GET` | `/class/class-list/{class_id}` | To get list of class members |
| `GET` | `/class/{id}` | To get a list of joined or created classes |

<br/>

**Assignment**
| Method | URL | Description |
| :---         | :---         | :--- 
|`POST`| `/assignment/create-assignment`| Used by teacher to create assignment
|`GET`| `/assignment/{class_id}/list`| Used by teacher to get all created assignments
|`GET`| `/assignment/{assign_id}/teacher`| Used by teacher to get assignment details of specific assignment
|`PUT`| `/assignment /{assign_id} /update-assignment`| Used by teacher to update assignment details
|`GET`| `/assignment/{stu_id}/{class_id}/list`| Used by student to get all pending and assigned assignment list
|`GET`| `/assignment/{assign_id}/student/pending`| Used by student to get details of specific pending assignment
|`POST`| `/assignment/{assign_id}/{student_id}/submit`| Used by student to submit assigned assignment
|`GET`| `/assignment /{assign_id} /{student_id} /submitted`| Used by student to get details of specific submitted assignment 
|`PUT`| `/assignment/{response_id}/update-response`| Used by student to update response of submitted assignment
|`GET`| `/assignment /{assign_id} /response-list`| Used by teacher to get all submitted but not graded reponses list
|`GET`| `/assignment /{response_id} /response`| Used by teacher to get details of specific response submitted by student
|`POST`| `/assignment/grade-assignment`| Used by teacher to grade student response
|`GET`| `/assignment/{assign_id}/graded-response-list`| Used by teacher to get all graded responses list of specific assignment
|`GET`| `/assignment/{response_id}/graded-response`| Used by teacher to get details of grade given to student for specific assignment response
|`PUT`| `/assignment/{grade_id}/update-grade`| Used by teacher to update grade given to student for specific assignment response

<br/>

**Quiz**
| Method | URL | Description |
| :---         | :---         | :--- 
| `POST` | `/quiz/make-quiz` | Used by teacher to create quiz |
| `POST` | `/quiz/make-question` | Used by teacher to make questions for specific quiz |
| `GET` | `/quiz/{class_id}` | Used by teacher to get list of created quizzes |
| `GET` | `/quiz/{class_id}/{student_id}` | Used by Student to get list of pending and submitted quizzes list |
| `GET` | `/quiz /question /{quiz_id}` | Used by teacher to get questions of specific quiz |
| `GET` | `/quiz/question/{quiz_id}/{student_id}` | Used by student to get questions or status of specific quiz |
| `POST` | `/quiz /response /{quiz_id} /{student_id}` | Used by student to submit quiz response |
| `POST` | `/quiz /result /{quiz_id}` | Used by teacher to release marks & responses of specific quiz |
| `GET` | `/quiz/statistics/{class_id}/{quiz_id}` | Used to get statistics for specific quiz |

<br/>

**Chat:**
| Method | URL | Description |
| :---         | :---         | :--- 
| `POST` | `/chat/message` | To POST messages in class` group chat |
| `GET` | `/chat/message/{class_id}` | To GET all messages of class` group chat |

<br/>

**Shared Folder:**
| Method | URL | Description |
| :---         | :---         | :--- 
| `POST` | `/sharedfolder/uploadfile` | To upload a file in shared folder |
| `GET` | `/sharedfolder /{class_id}` | To get all shared folder files of a class |
| `DELETE` | `/sharedfolder/delete-shared-file/{file_id}` | To delete file in shared folder (only if owned)  |

  
<br/>
<br/>
