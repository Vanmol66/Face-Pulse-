# 🎓 Face Recognition Attendance System with Role-Based Access (Django)

A fully functional **Face Detection Attendance System integrated with Django**, featuring **role-based dashboards** for different user types:

- **SuperAdmin**
- **Admin**
- **SubAdmin**
- **User**

This project allows attendance marking using **Face Recognition (OpenCV + Python)** and stores attendance records directly into the **Django Database**, enabling secure access and management based on user roles.

---

## 📌 Repository Description

This project combines:

✅ A Django-based multi-user role management system  
✅ A Face Recognition attendance system built using OpenCV  
✅ Automatic attendance record storage in a database  
✅ Role-based attendance viewing and control dashboards  

SuperAdmins/Admins/SubAdmins can view all attendance records, while Users can only view their own attendance history.

---

## 🚀 Features

### 👥 Role-Based User System
| Role        | Access Level |
|------------|--------------|
| SuperAdmin | Full access to all data and controls |
| Admin      | View/manage all attendance records |
| SubAdmin   | View attendance records with limited permissions |
| User       | View only personal attendance records |

---

### 📷 Face Recognition Attendance
- Real-time face detection using webcam
- Attendance marking based on recognized face
- Attendance stored in Django database automatically

---

### 🗃️ Attendance Database Management
- Attendance records stored with:
  - Username
  - Timestamp
  - Status (Present/Absent)

---

### 📊 Dashboard Access
- Separate dashboards for each role
- Secure authentication and authorization

---

## 🛠️ Tech Stack

| Technology | Usage |
|----------|------|
| Django | Backend Framework |
| Python | Core Programming |
| OpenCV | Face Detection + Camera Processing |
| face_recognition / dlib | Face Encoding & Matching |
| SQLite / PostgreSQL | Attendance Database |
| HTML + CSS + Bootstrap | Frontend UI |

---

## 📂 Project Structure

```bash
Face-Attendance-Django/
│
├── attendance/                # Attendance app
│   ├── models.py              # AttendanceRecord model
│   ├── views.py               # Attendance views
│   ├── urls.py                # Attendance routing
│   └── templates/attendance/  # Attendance templates
│
├── face_attendance/           # Face recognition module
│   ├── detector.py            # Face detection + attendance marking
│   └── encodings/             # Stored face encodings
│
├── users/                     # Role-based user management
│
├── static/                    # CSS, JS, Images
├── db.sqlite3                 # Database
├── manage.py
└── README.md
