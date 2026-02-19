import os
import sys
import django

# ✅ Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main2.settings")
django.setup()

from app2.models import Attendance, User  # adjust if your app name is different
from django.utils import timezone

import cv2

import os

import tkinter as tk

from tkinter import messagebox

import pandas as pd

from datetime import datetime

from deepface import DeepFace

import tensorflow as tf

from PIL import Image, ImageTk

from playsound import playsound

# 📂 Paths

dataset_dir = "ImagesAttendance"

attendance_file = "Attendance.csv"

bg_image_path = os.path.join(os.path.dirname(__file__), 'cyber_bg.png')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

gpus = tf.config.list_physical_devices('GPU')

print("✅ GPU detected" if gpus else "⚠ Running on CPU")


# face_attendance.py

import os
import pytz
import pandas as pd
from datetime import datetime
from app2.models import AttendanceLog, User
from django.utils.timezone import make_aware

def mark_attendance(name):
    name = name.strip()
    current_time = datetime.now()
    current_date = current_time.date()
    time_str = current_time.strftime("%H:%M:%S")

    # ✅ CSV Logging
    log_file = f"VisitLog_{current_date}.csv"
    columns = ["Name", "Date", "Time", "Event"]
    if not os.path.exists(log_file):
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.read_csv(log_file)

    person_logs_today = df[(df["Name"] == name) & (df["Date"] == str(current_date))]

    if not person_logs_today.empty:
        last_time_str = person_logs_today["Time"].iloc[-1]
        last_logged_time = pd.to_datetime(f"{current_date} {last_time_str}")
        time_diff = (current_time - last_logged_time).total_seconds()

        if time_diff < 180:
            print(f"⏳ Skipping log for {name} — last entry {int(time_diff)}s ago")
            return

    # ✅ Write to DB
    try:
        user = User.objects.get(username=name)
        AttendanceLog.objects.create(user=user, date=current_date, time=current_time.time(), event="Repeat" if not person_logs_today.empty else "First Entry")
    except User.DoesNotExist:
        print(f"❌ User '{name}' not found in database")
        return

    # ✅ Write to CSV
    entry = pd.DataFrame([[name, str(current_date), time_str, "First Entry" if person_logs_today.empty else "Repeat"]], columns=columns)
    df = pd.concat([df, entry], ignore_index=True)
    df.to_csv(log_file, index=False)
    print(f"✅ Logged {name} at {time_str}")










from mtcnn import MTCNN

detector = MTCNN()



def capture_images():

    os.makedirs(dataset_dir, exist_ok=True)

    name = name_entry.get().strip()



    if not name or any(char.isspace() for char in name) or not name.isalnum():

        messagebox.showerror("Invalid Name", "Please enter a valid name (no spaces or special characters).")

        return



    path = os.path.join(dataset_dir, name)

    os.makedirs(path, exist_ok=True)



    cap = cv2.VideoCapture(0)

    count = 0



    messagebox.showinfo("Started", f"📸 Capturing images for '{name}' — Press 'q' to finish early.")



    while True:

        ret, frame = cap.read()

        if not ret:

            break



        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = detector.detect_faces(rgb_frame)



        for result in results:

            x, y, w, h = result['box']

            x, y = max(0, x), max(0, y)

            roi = frame[y:y+h, x:x+w]

            count += 1



            filename = f"{name}_{count}.jpg"

            cv2.imwrite(os.path.join(path, filename), roi)



            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.putText(frame, f"{count}/50", (x, y-10),

                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)



        cv2.imshow("📷 Image Capture", frame)

        if cv2.waitKey(1) == ord('q') or count >= 50:

            break



    cap.release()

    cv2.destroyAllWindows()

    messagebox.showinfo("Completed", f"✅ Saved {count} face images to '{path}'")



def show_loading_screen():

    loading = tk.Toplevel(app)

    loading.title("Initializing Scanner")

    loading.geometry("300x150")

    loading.configure(bg="#0f0f1a")

    tk.Label(loading, text="🧠 Activating DeepFace Module...",

             font=("Segoe UI", 12), bg="#0f0f1a", fg="#00ffe1").pack(pady=20)

    tk.Label(loading, text="Please wait...", font=("Consolas", 10),

             bg="#0f0f1a", fg="white").pack()

    loading.update()

    return loading

from mtcnn import MTCNN

from deepface import DeepFace

import cv2, os, time

from datetime import datetime

from playsound import playsound



detector = MTCNN()

dataset_dir = "ImagesAttendance"

os.makedirs("UnknownFaces", exist_ok=True)



def start_recognition():

    os.makedirs(dataset_dir, exist_ok=True)



    loading = show_loading_screen()

    cap = cv2.VideoCapture(0)

    loading.destroy()



    messagebox.showinfo("Recognition", "Press 'q' to stop scanning.")



    last_alarm_time = 0

    cooldown_seconds = 5

    unknown_count = 0



    while True:

        ret, frame = cap.read()

        if not ret:

            break



        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = detector.detect_faces(rgb_frame)



        if results:

            # Use the first detected face

            box = results[0]['box']

            x, y, w, h = box

            x, y = max(0, x), max(0, y)

            face = frame[y:y+h, x:x+w]

            resized = cv2.resize(face, (224, 224))



            try:

                result = DeepFace.find(img_path=resized, db_path=dataset_dir,

                                       enforce_detection=False, model_name='ArcFace')

                if not result[0].empty:

                    match_row = result[0].iloc[0]

                    distance_col = [col for col in match_row.index if 'distance' in col.lower()]

                    distance = match_row[distance_col[0]] if distance_col else None

                    identity_path = match_row.get("identity", None)



                    print(f"🧪 Match distance: {distance:.4f}" if distance else "🔍 Distance not found")



                    threshold = 0.50 if distance < 0.55 else 0.45



                    if distance and identity_path and distance <= threshold:

                        name = os.path.basename(os.path.dirname(identity_path))

                        mark_attendance(name)

                        confidence_pct = (1 - distance) * 100

                        cv2.putText(frame, f"Welcome, {name} ({confidence_pct:.1f}%)", (40, 40),

                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

                    else:

                        unknown_count += 1

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                        filename = f"UnknownFaces/unknown_{unknown_count}_{timestamp}.jpg"

                        cv2.imwrite(filename, frame)

                        print(f"💾 Saved unknown face: {filename}")



                        current_time = time.time()

                        if current_time - last_alarm_time >= cooldown_seconds:

                            try:

                                playsound(r"C:\Users\verma\sd_venv\main2\app2\alarm.wav")


                                last_alarm_time = current_time

                                print("🔔 Alarm triggered")

                            except Exception as e:

                                print(f"❌ Alarm error: {e}")

                        else:

                            print("⏳ Alarm suppressed — cooldown active")



                        cv2.putText(frame, "Unknown Face", (40, 40),

                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

                else:

                    print("❌ No match found")

                    cv2.putText(frame, "No Match", (40, 40),

                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)



            except Exception as e:

                print(f"🔥 DeepFace error: {e}")

                cv2.putText(frame, "Recognition Error", (40, 40),

                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)



            # Draw bounding box

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)



        cv2.imshow("Recognition Scanner", frame)

        if cv2.waitKey(1) == ord('q'):

            break



    cap.release()

    cv2.destroyAllWindows()

def view_attendance():

    # 📂 List all attendance files matching pattern

    csv_files = [f for f in os.listdir() if f.startswith("Attendance_") and f.endswith(".csv")]



    if not csv_files:

        messagebox.showerror("Error", "No attendance files found.")

        return



    viewer = tk.Toplevel(app)

    viewer.title("Attendance Log Viewer")

    viewer.geometry("380x400")

    viewer.configure(bg="#0f0f1a")



    tk.Label(viewer, text="📋 Select Attendance Date", font=("Segoe UI", 12),

             bg="#0f0f1a", fg="#00ffe1").pack(pady=10)



    selected_file = tk.StringVar()

    selected_file.set(csv_files[-1])  # default to latest



    dropdown = tk.OptionMenu(viewer, selected_file, *csv_files)

    dropdown.config(font=("Consolas", 10), bg="#1c1f2d", fg="white", width=28)

    dropdown.pack(pady=5)



    text_area = tk.Text(viewer, wrap=tk.WORD, font=("Consolas", 10),

                        bg="#1c1f2d", fg="white")

    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)



    def load_csv():

        fname = selected_file.get()

        try:

            df = pd.read_csv(fname)

            if df.empty:

                log = "No records found."

            else:

                log = df.to_string(index=False)

        except Exception as e:

            log = f"❌ Could not read {fname}\n\n{e}"



        text_area.config(state='normal')

        text_area.delete(1.0, tk.END)

        text_area.insert(tk.END, log)

        text_area.config(state='disabled')



    tk.Button(viewer, text="📂 Load Log", command=load_csv,

              font=("Segoe UI", 10), bg="#007acc", fg="white",

              activebackground="#00bfff", relief="flat").pack(pady=5)



    # 🔄 Load default file on open

    load_csv()

def control_panel():

    global app, name_entry

    app = tk.Tk()

    app.title("Cyber Face Recognition System")

    app.geometry("480x360")

    app.resizable(False, False)

    bg_img = Image.open(bg_image_path).resize((480, 360))

    bg_photo = ImageTk.PhotoImage(bg_img)

    canvas = tk.Canvas(app, width=480, height=360, highlightthickness=0)

    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    title_font = ("Orbitron", 16, "bold")

    label_font = ("Segoe UI", 12)

    entry_font = ("Consolas", 12)

    button_font = ("Segoe UI", 11)

    entry_bg = "#1c1f2d"

    entry_fg = "white"

    btn_color = "#007acc"

    btn_hover = "#00bfff"

    canvas.create_text(240, 35, text="Face Recognition Control Panel", fill="#00ffe1", font=title_font)

    canvas.create_text(240, 85, text="Enter User Name", fill="white", font=label_font)

    name_entry = tk.Entry(app, font=entry_font, width=24, bg=entry_bg, fg=entry_fg,

                          relief="flat", insertbackground="white")

    canvas.create_window(240, 115, window=name_entry)

    def on_enter(e): e.widget.config(bg=btn_hover)

    def on_leave(e): e.widget.config(bg=btn_color)

    capture_btn = tk.Button(app, text="📸 Capture Images", command=capture_images,

                            font=button_font, width=20, bg=btn_color, fg="white",

                            activebackground=btn_hover, relief="flat", padx=8, pady=6)

    canvas.create_window(240, 165, window=capture_btn)

    capture_btn.bind("<Enter>", on_enter)

    capture_btn.bind("<Leave>", on_leave)

    recognition_btn = tk.Button(app, text="🎯 Start Recognition", command=start_recognition,

                                font=button_font, width=20, bg=btn_color, fg="white",

                                activebackground=btn_hover, relief="flat", padx=8, pady=6)

    canvas.create_window(240, 215, window=recognition_btn)

    recognition_btn.bind("<Enter>", on_enter)

    recognition_btn.bind("<Leave>", on_leave)

    log_btn = tk.Button(app, text="📋 View Attendance Logs", command=view_attendance,

                        font=button_font, width=20, bg=btn_color, fg="white",

                        activebackground=btn_hover, relief="flat", padx=8, pady=6)

    canvas.create_window(240, 265, window=log_btn)

    log_btn.bind("<Enter>", on_enter)

    log_btn.bind("<Leave>", on_leave)

    app.mainloop()

def subadmin_panel(username):

    global app, name_entry

    app = tk.Tk()

    app.title("Subadmin Panel")

    app.geometry("480x360")

    app.resizable(False, False)

    bg_img = Image.open(bg_image_path).resize((480, 360))

    bg_photo = ImageTk.PhotoImage(bg_img)

    canvas = tk.Canvas(app, width=480, height=360, highlightthickness=0)

    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    title_font = ("Orbitron", 16, "bold")

    label_font = ("Segoe UI", 12)

    entry_font = ("Consolas", 12)

    button_font = ("Segoe UI", 11)

    entry_bg = "#1c1f2d"

    entry_fg = "white"

    btn_color = "#007acc"

    btn_hover = "#00bfff"

    canvas.create_text(240, 35, text=f"Welcome {username}", fill="#00ffe1", font=title_font)

    canvas.create_text(240, 85, text="Enter User Name", fill="white", font=label_font)

    name_entry = tk.Entry(app, font=entry_font, width=24, bg=entry_bg, fg=entry_fg,

                          relief="flat", insertbackground="white")

    canvas.create_window(240, 115, window=name_entry)

    def on_enter(e): e.widget.config(bg=btn_hover)

    def on_leave(e): e.widget.config(bg=btn_color)

    capture_btn = tk.Button(app, text="📸 Capture Images", command=capture_images,

                            font=button_font, width=20, bg=btn_color, fg="white",

                            activebackground=btn_hover, relief="flat", padx=8, pady=6)

    canvas.create_window(240, 165, window=capture_btn)

    capture_btn.bind("<Enter>", on_enter)

    capture_btn.bind("<Leave>", on_leave)

    recognition_btn = tk.Button(app, text="🎯 Start Recognition", command=start_recognition,

                                font=button_font, width=20, bg=btn_color, fg="white",

                                activebackground=btn_hover, relief="flat", padx=8, pady=6)

    canvas.create_window(240, 215, window=recognition_btn)

    recognition_btn.bind("<Enter>", on_enter)

    recognition_btn.bind("<Leave>", on_leave)

    # 🚫 No "View Attendance Logs" button here for subadmins

    app.mainloop()

def login_screen(role):

    login = tk.Tk()

    login.title(f"{role.capitalize()} Login")

    login.geometry("320x350")

    login.configure(bg="#0f0f1a")

    tk.Label(login, text=f"🔐 {role.capitalize()} Login", font=("Segoe UI", 14, "bold"),

             bg="#0f0f1a", fg="#00ffe1").pack(pady=10)

    tk.Label(login, text="Username", bg="#0f0f1a", fg="white").pack()

    user_entry = tk.Entry(login, font=("Consolas", 12), bg="#1c1f2d", fg="white", relief="flat")

    user_entry.pack(pady=5)

    tk.Label(login, text="Password", bg="#0f0f1a", fg="white").pack()

    pass_entry = tk.Entry(login, font=("Consolas", 12), bg="#1c1f2d", fg="white", show="*", relief="flat")

    pass_entry.pack(pady=5)

    user_roles = {

        "admin1": {"password": "pass123", "role": "admin"},

        "admin2": {"password": "pass456", "role": "admin"},

        "sub1": {"password": "sub123", "role": "subadmin"},

        "sub2": {"password": "sub456", "role": "subadmin"},

        "sub3": {"password": "sub789", "role": "subadmin"},

        "sub4": {"password": "sub321", "role": "subadmin"}

    }

    def forgot_password():

        recovery = tk.Toplevel(login)

        recovery.title("Password Recovery")

        recovery.geometry("300x180")

        recovery.configure(bg="#0f0f1a")

        tk.Label(recovery, text="🔐 Recover Password", font=("Segoe UI", 12, "bold"),

                 bg="#0f0f1a", fg="#00ffe1").pack(pady=10)

        tk.Label(recovery, text="Enter Username", bg="#0f0f1a", fg="white").pack()

        uname_entry = tk.Entry(recovery, font=("Consolas", 11), bg="#1c1f2d", fg="white", relief="flat")

        uname_entry.pack(pady=5)

        def retrieve():

            uname = uname_entry.get().strip()

            if uname in user_roles and user_roles[uname]["role"] == role:

                recovered_pass = user_roles[uname]["password"]

                messagebox.showinfo("Recovered", f"Your password is: {recovered_pass}")

                recovery.destroy()

            else:

                messagebox.showerror("Error", "Username not found or mismatched role")

        tk.Button(recovery, text="Recover", command=retrieve,

                  font=("Segoe UI", 11), bg="#007acc", fg="white",

                  activebackground="#00bfff", relief="flat").pack(pady=10)

    def show_loading():

        loading = tk.Toplevel(login)

        loading.title("Loading Panel")

        loading.geometry("300x150")

        loading.configure(bg="#0f0f1a")

        tk.Label(loading, text="🔧 Initializing Dashboard...", font=("Segoe UI", 12),

                 bg="#0f0f1a", fg="#00ffe1").pack(pady=20)

        tk.Label(loading, text="Please wait...", font=("Consolas", 10),

                 bg="#0f0f1a", fg="white").pack()

        loading.update()

        return loading

    def validate_login():

        username = user_entry.get().strip()

        password = pass_entry.get().strip()

        expected_prefix = "admin" if role == "admin" else "sub"

        if username.startswith(expected_prefix) and username in user_roles and user_roles[username][

            "password"] == password:

            # Create a new root for loading instead of linking it to login

            loading_root = tk.Tk()

            loading_root.title("Loading Panel")

            loading_root.geometry("300x150")

            loading_root.configure(bg="#0f0f1a")

            tk.Label(loading_root, text="🔧 Initializing Dashboard...",

                     font=("Segoe UI", 12), bg="#0f0f1a", fg="#00ffe1").pack(pady=20)

            tk.Label(loading_root, text="Please wait...", font=("Consolas", 10),

                     bg="#0f0f1a", fg="white").pack()

            # Close login window after loading screen is created

            login.destroy()

            def launch_panel():

                loading_root.destroy()

                if role == "admin":

                    control_panel()

                else:

                    subadmin_panel(username)

            loading_root.after(1500, launch_panel)

            loading_root.mainloop()

        else:

            messagebox.showerror("Access Denied", "Invalid credentials!")

    tk.Button(login, text="Login", command=validate_login,

              font=("Segoe UI", 11), bg="#007acc", fg="white",

              activebackground="#00bfff", relief="flat", padx=8, pady=6).pack(pady=15)

    tk.Button(login, text="Forgot Password?", command=forgot_password,

              font=("Segoe UI", 10), bg="#1c1f2d", fg="#00ffe1",

              activebackground="#00bfff", relief="flat").pack(pady=2)

    login.mainloop()

def role_selector():

    selector = tk.Tk()

    selector.title("Select Role")

    selector.geometry("300x250")

    selector.configure(bg="#0f0f1a")

    tk.Label(selector, text="🚀 Choose Your Role", font=("Segoe UI", 14, "bold"),

             bg="#0f0f1a", fg="#00ffe1").pack(pady=30)

    tk.Button(selector, text="🛡 Admin", font=("Segoe UI", 11),

              bg="#007acc", fg="white", activebackground="#00bfff",

              relief="flat", padx=10, pady=6, command=lambda: [selector.destroy(), login_screen("admin")]).pack(pady=5)

    tk.Button(selector, text="🧑‍💼 Subadmin", font=("Segoe UI", 11),

              bg="#007acc", fg="white", activebackground="#00bfff",

              relief="flat", padx=10, pady=6, command=lambda: [selector.destroy(), login_screen("subadmin")]).pack(pady=5)

    selector.mainloop()

# 🔚 Start the app with login

role_selector()