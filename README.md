# Face-Pulse-AI

🧠🚆 **FacePulse — Face Recognition System for Server Room**  
A web-based, contactless in-time / out-time logging and monitoring system using **DeepFace (Facenet)**, **Django**, and **PostgreSQL**.

Project report submitted as part of **Summer Internship/Training at RDSO (Research Designs and Standards Organisation), Ministry of Railways, Government of India.**

---

# Project Overview 📘

FacePulse is a prototype biometric logging system that:

- 📸 Allows user registration via facial image upload or webcam capture  
- 🔗 Generates and stores facial embeddings (Facenet via DeepFace)  
- 🌐 Performs real-time identity verification through a browser webcam (MediaStream API)  
- 🕒 Automatically records entry (in-time) and exit (out-time) timestamps and duration  
- 💾 Stores logs in a relational database (PostgreSQL recommended; SQLite used for development)  

The system is intended for secure areas such as server rooms where contactless, auditable entry/exit logging is required.

---

# Problem Statement / Challenges Faced ❗

Organizations relying on traditional logging or access-control methods (manual registers, RFID cards, or legacy scanners) face several practical problems:

- ✍️ Manual dependency — paper registers are error-prone, hard to audit, and enable impersonation.  
- ⌛ Time inefficiency — card swipes or manual entries add delays and create queues for high-traffic areas.  
- 🔒 Tamper & security risk — physical tokens/cards can be lost, shared, or cloned; paper records can be altered.  
- 📉 Poor scalability & integration — legacy systems rarely integrate with centralized analytics or cloud services.  
- 🌙 Environmental & hygiene constraints — fingerprint scanners require contact; in pandemic contexts, contactless is preferred.  
- 🧩 Deployment complexity — installing and maintaining dedicated hardware across many locations increases cost and operational overhead.  

These challenges motivated the design of a contactless, centralized, and auditable logging solution that reduces human error and operational friction.

---

# Proposed Solution 💡

FacePulse — a web-accessible, FaceNet-based recognition and logging system — addresses the problems above with the following approach:

- **Contactless authentication:** Users register once (image or webcam) and can authenticate via browser webcam, eliminating physical tokens.  
- **Embedding-based identity:** FaceNet embeddings (via DeepFace) represent users as compact vectors stored server-side; matching uses cosine/Euclidean distance for reliable verification.  
- **Automated logging:** Entry and exit timestamps are recorded automatically; durations are computed and stored for analytics.  
- **Centralized datastore:** PostgreSQL (recommended for production) stores user metadata and logs, enabling reporting and audits.  
- **Minimal hardware footprint:** Runs on standard web browsers with webcam support — avoids expensive fingerprint or card infrastructure.  
- **Security-first design:** Server-side matching, HTTPS transport, RBAC-ready admin views, and support for encryption/retention policies.  

### Benefits:

- Faster check-ins and check-outs, reduced queues  
- Better auditability and tamper resistance  
- Easier scalability and integration with dashboards and analytics  
- Hygiene-friendly, contactless operation  

---

# Key Features ✅

| Feature | Description |
|--------|-------------|
| 🆔 Face registration | Register users with an image or webcam snapshot; embeddings stored server-side |
| 📷 Real-time recognition | Browser webcam capture via MediaStream → server-side DeepFace matching |
| 📏 Matching metrics | Cosine similarity / Euclidean distance thresholding for identity verification |
| 📝 Automated logging | Automatic entry/exit timestamps and duration calculation per session |
| 🖥️ Web UI | Lightweight HTML5/JS templates for registration, recognition, and admin |
| 🧩 Modular backend | Django models/views/helpers for easy extension and reporting |

---

# Tech Stack 🧩

| Component | Technology | Notes |
|----------|------------|------|
| Backend | Django (Python) | MVT architecture, ORM, admin |
| Face recognition | DeepFace (Facenet) | Embedding generation & verification |
| Image processing | OpenCV, NumPy, Pillow | Preprocessing, decoding, resizing |
| ML Backend | TensorFlow / Keras | DeepFace model runtime |
| DB (dev) | SQLite | Lightweight local testing |
| DB (prod) | PostgreSQL | Recommended for production concurrency |
| Frontend | HTML5, CSS3, JavaScript | MediaStream API for webcam |
| Reporting | python-docx | Document generation helpers present |

---

# Quick Setup (Development) 🛠️

## Prerequisites

| Tool | Purpose | Version / Notes |
|------|---------|----------------|
| Python | Runtime | 3.8+ (match TF/DeepFace compatibility) |
| pip | Package installer | Latest |
| virtualenv / venv | Isolate dependencies | Recommended |
| Git | Version control | — |
| (Prod) PostgreSQL | Production DB | Optional for dev |
| (Prod) TLS | Camera access over HTTPS | Required in production |

---

## Basic Steps

| Step | Command / Action |
|------|------------------|
| Clone repo | `git clone <repo-url>` |
| Create venv | `python -m venv venv` |
| Activate venv | `source venv/bin/activate` (Windows: `venv\Scripts\activate`) |
| Install dependencies | `pip install -r requirements.txt` |
| Configure env | Copy `.env.example → .env`, set DB and MEDIA paths |
| Migrate DB | `python manage.py migrate` |
| Create admin | `python manage.py createsuperuser` |
| Start server | `python manage.py runserver` |

🔒 Browsers require secure origins for camera access — serve over HTTPS in production. Localhost often allowed for testing.

⚙️ dlib/TensorFlow/OpenCV installs can be OS-sensitive — consult OS-specific guides or prebuilt wheels.

---

# Usage ▶️

| Page | Endpoint | Action |
|------|----------|--------|
| Registration | `/register/` | Upload image or capture webcam → embedding saved |
| Recognition | `/recognize/` | Capture snapshot → compare embeddings → log entry/exit |
| Admin | `/admin/` | Manage users, logs, export reports |

### Behavior:

- If no active session → record `entry_time` ⏱️  
- If active session exists → record `exit_time`, calculate duration, mark session complete ✅  

---

# Project Structure (High Level) 📁

| Path | Purpose |
|------|---------|
| manage.py | Django project management |
| myproject/ | Settings, URL routing, WSGI/ASGI |
| my_app/ | App logic: models.py, views.py, forms.py, word_helpers.py |
| my_app/templates/ | UI templates (data_entry.html, download_doc.html) |
| my_app/word_helpers.py | Utilities for .docx generation |
| media/ | Uploaded images & generated documents |
| static/ | Static assets: logos, CSS, JS |
| requirements.txt | Python packages |

---

# 🧠 Data Flow

```text
                ┌────────────────────────────┐
                │        Web Browser         │
                │ (MediaStream + JavaScript) │
                └────────────┬───────────────┘
                             │
                             ▼
              Capture user face via webcam
                             │
                             ▼
              ┌────────────────────────────┐
              │        Django Views        │
              │     (app2/views.py)        │
              └────────────┬───────────────┘
                           │
                           ▼
           Image preprocessing with OpenCV / DeepFace
                           │
                           ▼
              ┌────────────────────────────┐
              │     Face Embedding Engine  │
              │  (Facenet model via DeepFace) │
              └────────────┬───────────────┘
                           │
             Compare embeddings with registered profiles
                           │
                ┌──────────┴────────────┐
                │                       │
                ▼                       ▼
        ✅ Match Found             ❌ Unknown Face
        ─────────────             ─────────────
  Log entry/exit event        Store image in UnknownFaces/
  Update PostgreSQL DB        Play alarm.wav alert
  Generate VisitLog CSV       Notify admin if needed
                    │
                    ▼
       ┌────────────────────────────┐
       │        Django Models       │
       │  (Person, LoggingLog)      │
       └────────────┬───────────────┘
                    │
                    ▼
            PostgreSQL / SQLite Database
                    │
                    ▼
       ┌────────────────────────────┐
       │       Admin Dashboard      │
       │ (templates/dashboard.html) │
       └────────────────────────────┘
Face-Pulse-AI/
│
├── main2/                                   # Django Project Folder
│   ├── app2/                                # Main Application
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── admin.py
│   │   ├── alarm.wav                        # Alert sound for unknown face
│   │   ├── apps.py
│   │   ├── cyber_bg.png                     # Background image (UI asset)
│   │   ├── face_attendance.py               # Core facial recognition logic
│   │   ├── forms.py                         # Django forms
│   │   ├── models.py                        # Database models
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── ImagesAttendance/                    # Folder storing attendance snapshots
│   ├── UnknownFaces/                        # Stores unidentified captures
│   ├── main2/                               # Django Core (Project Settings)
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── media/                               # Uploaded images or data files
│   ├── static/                              # CSS, JS, and static assets
│   ├── templates/                           # HTML templates
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── login.html
│   │
│   ├── db.sqlite3                           # Database file (development)
│   │
│   ├── manage.py                            # Django management script
│   └── VisitLog_2025-07-24.csv              # Sample attendance log export
│
├── LICENSE
├── README.md
