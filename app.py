import streamlit as st
import cv2
from datetime import datetime
import os

from tracker import Tracker
from main import process_frame

# ------------------ SETUP ------------------
st.set_page_config(layout="wide")

# Create folder for alerts
os.makedirs("assets/captures", exist_ok=True)

# ------------------ LOGIN ------------------
def login():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state['logged_in'] = True
            st.success("Logged In!")
        else:
            st.error("Wrong Credentials")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🐕 Rabies Detection System")
    st.info("Login from sidebar")
    login()
    st.stop()

# ------------------ CAMERA MANAGEMENT ------------------
st.title("🚀 Smart CCTV Dashboard")

if 'cameras' not in st.session_state:
    st.session_state['cameras'] = {"Webcam": 0}

with st.expander("⚙️ Manage Cameras"):
    col1, col2 = st.columns(2)

    name = col1.text_input("Camera Name")
    url = col2.text_input("Camera Source (0 or RTSP)")

    if st.button("Add Camera"):
        st.session_state['cameras'][name] = int(url) if url.isdigit() else url
        st.success("Camera Added")

    remove = st.selectbox("Remove Camera", list(st.session_state['cameras'].keys()))
    if st.button("Delete Camera"):
        del st.session_state['cameras'][remove]
        st.warning("Camera Removed")

# ------------------ LAYOUT ------------------
main_col, alert_col = st.columns([3, 1])

# ------------------ LIVE FEED ------------------
with main_col:
    st.subheader("📺 Live Feed")

    cam_name = st.selectbox("Select Camera", list(st.session_state['cameras'].keys()))
    source = st.session_state['cameras'][cam_name]

    run = st.button("▶ Start Camera")

    frame_window = st.image([])

    if run:
        tracker = Tracker()
        cap = cv2.VideoCapture(source)

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Camera Error")
                break

            # -------- USE MAIN AI FUNCTION --------
            frame, alerts = process_frame(frame, tracker)

            # -------- HANDLE ALERTS --------
            for alert in alerts:
                filename = f"assets/captures/alert_{cam_name}_{datetime.now().strftime('%H%M%S')}.jpg"
                cv2.imwrite(filename, frame)

                st.session_state['last_alert'] = {
                    "id": alert["id"],
                    "cam": cam_name,
                    "time": datetime.now().strftime('%H:%M:%S'),
                    "img": filename
                }

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_window.image(frame)

# ------------------ ALERT PANEL ------------------
with alert_col:
    st.subheader("🚨 Alerts")

    if 'last_alert' in st.session_state:
        alert = st.session_state['last_alert']

        st.error("RABID DETECTED")
        st.image(alert["img"])
        st.write(f"ID: {alert['id']}")
        st.write(f"Camera: {alert['cam']}")
        st.write(f"Time: {alert['time']}")

        if st.button("Clear Alert"):
            del st.session_state['last_alert']
            st.success("Cleared")
    else:
        st.info("No alerts yet")