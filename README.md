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

