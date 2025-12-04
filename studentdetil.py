# create by Harish D


import streamlit as st
import pandas as pd
import tempfile
import os
import datetime
import uuid

# Simple Streamlit college management single-file app
# Run: streamlit run streamlit_college_app.py

st.set_page_config(page_title="College Portal", layout="wide")

# Initialize session state
if "students" not in st.session_state:
    st.session_state.students = {}  # student_id -> dict
if "uploads" not in st.session_state:
    st.session_state.uploads = {}  # student_id -> list of (name, path)
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# Utility functions
def make_student_id():
    return str(uuid.uuid4())[:8]

def save_uploaded_file(uploaded_file, student_id):
    # Save file to a temp directory and store path
    tmpdir = tempfile.gettempdir()
    student_dir = os.path.join(tmpdir, "college_portal_files", student_id)
    os.makedirs(student_dir, exist_ok=True)
    file_path = os.path.join(student_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.uploads.setdefault(student_id, []).append((uploaded_file.name, file_path))
    return file_path

# Top-level layout: sidebar navigation
st.sidebar.title(" 📚 MENU")
page = st.sidebar.radio("Go to", ["Home", "👤 Student", "Academics", "Exam", "Report"])

# Small helper to pick active student
st.markdown("---")
student_ids = list(st.session_state.students.keys())
selected_student = None
if student_ids:
    sel = st.sidebar.selectbox("Logged-in student (select)", ["-- Choose --"] + student_ids)
    if sel != "-- Choose --":
        selected_student = sel
else:
    st.sidebar.info("No students registered yet. Use Student → Register to add one.")

# ---------- HOME PAGE ----------
if page == "Home":
    
    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="https://www.freepik.com/free-vector/hand-drawn-high-school-logo-design_31746352.htm#fromView=keyword&page=1&position=19&uuid=bf26f565-6b3e-4463-99c8-c0066968ab72&query=Student+logo" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("Welcome to your college")
    st.subheader("Portal Home")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("View my Admission Details"):
            if selected_student:
                st.success("Showing admission details for: {}".format(selected_student))
                st.write(st.session_state.students[selected_student])
            else:
                st.warning("Please select a student from the sidebar to view details.")

    with col2:
        uploaded = st.file_uploader("Upload Documentation (PDF/JPG/PNG)", type=["pdf", "png", "jpg", "jpeg"], key="home_upload")
        if uploaded is not None:
            if selected_student:
                path = save_uploaded_file(uploaded, selected_student)
                st.success(f"Uploaded {uploaded.name} for student {selected_student}")
            else:
                st.warning("Select or register a student first (sidebar).")

    with col3:
        if st.button("Admission Updates"):
            # Placeholder: in real app, fetch updates from DB or API
            st.info("No new updates. (This is a demo placeholder.)")

    
# -------------------- STUDENT PAGE --------------------
elif page == "Student":
    st.header("👨‍🎓 Student Services")

    student_menu = st.selectbox(
        "Select Student Option",
        [
            "Register Student",
            "View / Edit Profile",
            "Upload Profile Files",
            "Scholarship",
            "Internship & Training",
            "Cultural / Sports",
            "Bus Pass Upload",
            "Uploaded Documents",
            "Aadhaar Revalidate",
            "Final Submission"
        ]
    )

    # 1. REGISTER STUDENT
    if student_menu == "Register Student":
        st.subheader("📝 Register Student")

        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")

        if st.button("Submit Registration"):
            st.success("Student registered successfully!")

    # 2. VIEW / EDIT PROFILE
    elif student_menu == "View / Edit Profile":
        st.subheader("👤 View & Edit Profile")
        st.info("Profile details will be shown from database.")

        st.text_input("Full Name")
        st.text_input("Email")
        st.text_input("Phone")
        st.text_area("Address")

        if st.button("Save Changes"):
            st.success("Profile updated successfully!")

    # 3. UPLOAD PROFILE FILES
    elif student_menu == "Upload Profile Files":
        st.subheader("📁 Upload Profile Files")
        files = st.file_uploader("Upload Profile Documents", accept_multiple_files=True)

        if st.button("Save Files"):
            st.success("Files uploaded successfully!")

    # 4. SCHOLARSHIP
    elif student_menu == "Scholarship":
        st.subheader("🎓 Scholarship Form")
        st.text_input("Scholarship Type")
        st.text_input("Income Certificate Number")
        st.file_uploader("Upload Income Certificate")
        if st.button("Apply Scholarship"):
            st.success("Scholarship application submitted!")

    # 5. INTERNSHIP & TRAINING
    elif student_menu == "Internship & Training":
        st.subheader("💼 Internship / Training")
        st.text_input("Company Name")
        st.date_input("Start Date")
        st.date_input("End Date")
        st.file_uploader("Upload Offer Letter")
        if st.button("Submit"):
            st.success("Internship details saved!")

    # 6. CULTURAL & SPORTS
    elif student_menu == "Cultural / Sports":
        st.subheader("🏆 Cultural / Sports Registration")
        st.text_input("Event Name")
        st.file_uploader("Upload Participation Proof")
        if st.button("Submit"):
            st.success("Event participation submitted!")

    # 7. BUS PASS UPLOAD
    elif student_menu == "Bus Pass Upload":
        st.subheader("🚌 Bus Pass")
        st.text_input("Route Number")
        st.file_uploader("Upload Bus Pass Document")
        if st.button("Save Bus Pass"):
            st.success("Bus Pass details saved!")

    # 8. UPLOADED DOCUMENTS
    elif student_menu == "Uploaded Documents":
        st.subheader("📄 Uploaded Documents")
        st.info("All your submitted documents will appear here.")

    # 9. AADHAAR REVALIDATE
    elif student_menu == "Aadhaar Revalidate":
        st.subheader("🔐 Aadhaar Revalidation")
        st.text_input("Aadhaar Number")
        st.file_uploader("Upload Aadhaar File")
        if st.button("Revalidate"):
            st.success("Aadhaar revalidated successfully!")

    # 10. FINAL SUBMISSION
    elif student_menu == "Final Submission":
        st.subheader("✅ Final Submission")
        st.warning("Please ensure all details & documents are uploaded.")
        if st.button("Submit to College"):
            st.success("All student details submitted successfully!")

# ---------- ACADEMICS PAGE ----------
elif page == "Academics":
    st.header("Academics")
    tab = st.selectbox("Select Academic Option", ["Course Registration", "Academic Calendar", "View Timetable"
                            ]) 

    if tab == "Course Registration":
        st.subheader("📝 Course Registration")

        course_code = st.text_input("Course Code")
        course_name = st.text_input("Course Name")
        department = st.selectbox("Department", 
                                ["CSE", "ECE", "Mechanical", "Civil", "IT", "AI & DS"])
        semester = st.selectbox("Semester", 
                                ["1", "2", "3", "4", "5", "6", "7", "8"])

        if st.button("Register Course"):
            st.success("Course Registered Successfully!")

    elif tab == "Academic Calendar":
        st.subheader("Academic Calendar of Events")
        # demo calendar as table
        calendar = pd.DataFrame([
            {"Date": "2025-08-01", "Event": "Semester begins"},
            {"Date": "2025-10-15", "Event": "Midterm Exams"},
            {"Date": "2025-12-20", "Event": "Semester ends"},
        ])
        st.dataframe(calendar)
        st.download_button("Download Calendar as CSV", calendar.to_csv(index=False), file_name="academic_calendar.csv")

    elif tab == "View Timetable":
        st.subheader("View Timetable")
        # placeholder timetable
        timetable = pd.DataFrame({
            "Time": ["09:00-10:00", "10:00-11:00", "11:00-12:00"],
            "Monday": ["Math", "Physics", "Free"],
            "Tuesday": ["English", "Chemistry", "Lab"],
        })
        st.table(timetable)

# ---------- EXAM PAGE ----------
elif page == "Exam":
    st.header("Exams & Services")
    action = st.selectbox("Choose", ["Exam Application", "Fee Payment", "Re-evaluation / Challenge", "Convocation", "Student Services"])

    if action == "Exam Application":
        st.subheader("Exam Application")
        sid = st.selectbox("Student", ["-- Choose --"] + list(st.session_state.students.keys()))
        if sid and sid != "-- Choose --":
            with st.form("exam_app"):
                exam_name = st.text_input("Exam Name")
                subjects = st.text_area("Subjects (comma separated)")
                submit = st.form_submit_button("Apply")
                if submit:
                    st.success("Exam application submitted (demo).")

    elif action == "Fee Payment":
        st.subheader("Student Fee Payment")
        sid = st.selectbox("Student", ["-- Choose --"] + list(st.session_state.students.keys()))
        if sid and sid != "-- Choose --":
            amount = st.number_input("Amount", min_value=0.0, value=1000.0, step=100.0)
            if st.button("Pay Now"):
                tx = {"id": str(uuid.uuid4())[:10], "student": sid, "amount": amount, "time": datetime.datetime.now().isoformat()}
                st.session_state.transactions.append(tx)
                st.success(f"Payment successful. Transaction id: {tx['id']}")

    elif action == "Re-evaluation / Challenge":
        st.subheader("Re-evaluation & Result Challenges")
        sid = st.selectbox("Student", ["-- Choose --"] + list(st.session_state.students.keys()))
        if sid and sid != "-- Choose --":
            with st.form("reeval"):
                subject = st.text_input("Subject")
                reason = st.text_area("Reason / Note")
                kind = st.selectbox("Type", ["Re-evaluation", "Challenge Valuation", "Rejection of Result"])
                submit = st.form_submit_button("Submit")
                if submit:
                    st.success(f"{kind} request submitted for {subject} (demo).")

    elif action == "Convocation":
        st.subheader("Convocation")
        sid = st.selectbox("Student", ["-- Choose --"] + list(st.session_state.students.keys()))
        if sid and sid != "-- Choose --":
            attend = st.checkbox("I will attend the convocation")
            if st.button("Confirm"):
                st.success("Convocation attendance confirmed (demo).")

    elif action == "Student Services":
        st.subheader("Student Services")
        st.write("Contact: studentservices@college.edu | Phone: 0123-456789")

# ---------- REPORT PAGE ----------
elif page == "Report":
    st.header("Reports")
    choice = st.selectbox("Report", ["Student List", "Transactions", "Uploaded Files Summary"])

    if choice == "Student List":
        st.subheader("All Registered Students")
        rows = []
        for sid, p in st.session_state.students.items():
            rows.append({"student_id": sid, "first": p.get("first"), "last": p.get("last"), "email": p.get("email"), "course": p.get("course")})
        df = pd.DataFrame(rows)
        st.dataframe(df)
        st.download_button("Download Students CSV", df.to_csv(index=False), file_name="students.csv")

    elif choice == "Transactions":
        st.subheader("Payment Transactions")
        df = pd.DataFrame(st.session_state.transactions)
        if df.empty:
            st.info("No transactions yet.")
        else:
            st.dataframe(df)
            st.download_button("Download Transactions CSV", df.to_csv(index=False), file_name="transactions.csv")

    elif choice == "Uploaded Files Summary":
        st.subheader("Uploaded Files Summary")
        rows = []
        for sid, files in st.session_state.uploads.items():
            for name, path in files:
                rows.append({"student_id": sid, "filename": name, "path": path})
        df = pd.DataFrame(rows)
        if df.empty:
            st.info("No uploaded files yet.")
        else:
            st.dataframe(df)
            st.download_button("Download Files CSV", df.to_csv(index=False), file_name="uploaded_files.csv")

# Footer
st.markdown("---")
st.caption("Demo Streamlit College Portal — use this as a starting point and connect to a real database for production.")
