"""
Database module for Government Polytechnic Mahasi, Bahraich (PPP Mode)
SQLite database with full tables and realistic seed data.
"""
import sqlite3
import os
import hashlib
import json
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "polytechnic.db")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Admin Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT DEFAULT 'Super Admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Admissions / Applications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_no TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        father_name TEXT NOT NULL,
        mother_name TEXT,
        dob TEXT NOT NULL,
        gender TEXT NOT NULL,
        category TEXT DEFAULT 'General',
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        district TEXT NOT NULL,
        state TEXT DEFAULT 'Uttar Pradesh',
        pincode TEXT NOT NULL,
        branch TEXT NOT NULL,
        high_school_board TEXT NOT NULL,
        high_school_percent REAL NOT NULL,
        intermediate_percent REAL,
        jeecup_roll_no TEXT,
        jeecup_rank INTEGER,
        status TEXT DEFAULT 'Pending Review',
        admin_remarks TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Students Directory Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT UNIQUE NOT NULL,
        enrollment_no TEXT UNIQUE,
        full_name TEXT NOT NULL,
        branch TEXT NOT NULL,
        semester INTEGER NOT NULL,
        academic_year TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        fee_status TEXT DEFAULT 'Paid',
        attendance_percent REAL DEFAULT 85.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Notices & Circulars Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        content TEXT NOT NULL,
        published_date TEXT NOT NULL,
        is_urgent INTEGER DEFAULT 0,
        attachment_url TEXT,
        posted_by TEXT DEFAULT 'Academic Office'
    )
    """)

    # Faculty Directory Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        designation TEXT NOT NULL,
        department TEXT NOT NULL,
        qualification TEXT NOT NULL,
        experience_years INTEGER NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        is_hod INTEGER DEFAULT 0
    )
    """)

    # Public Enquiries / Grievances Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'New',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Campus Gallery Photos Table (Admin can add, edit, delete photos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gallery_photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT DEFAULT 'Campus Life',
        image_data TEXT NOT NULL,
        caption TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Site Settings Table (For dynamic Featured Campus Building Photo, titles, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Documents & PDF Downloads Table (Admin can upload, students can download)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_data TEXT NOT NULL,
        file_size_kb INTEGER DEFAULT 0,
        uploaded_date TEXT NOT NULL,
        description TEXT,
        download_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Ensure notices table has pdf_data and pdf_name columns
    notice_cols = [r[1] for r in cursor.execute("PRAGMA table_info(notices)").fetchall()]
    if "pdf_data" not in notice_cols:
        cursor.execute("ALTER TABLE notices ADD COLUMN pdf_data TEXT")
    if "pdf_name" not in notice_cols:
        cursor.execute("ALTER TABLE notices ADD COLUMN pdf_name TEXT")

    conn.commit()

    # Seed Admin User if not exists
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO admin_users (username, password_hash, full_name, role)
        VALUES (?, ?, ?, ?)
        """, ('admin', hash_password('admin123'), 'Principal / Admin Secretariat', 'Super Admin'))
        conn.commit()

    # Seed Notices if empty
    cursor.execute("SELECT COUNT(*) FROM notices")
    if cursor.fetchone()[0] == 0:
        today_str = date.today().strftime("%d %b %Y")
        initial_notices = [
            ("Diploma Admission 2026-27 Registrations Open (Direct & JEECUP Counseling)", "Admissions",
             "Online registration is now open for 3-Year Diploma courses in CSE, Civil, Mechanical, and Electrical & Electronics Engineering. Visit campus or apply online through this portal.",
             today_str, 1, "#admissions"),
            ("Even Semester Examination Schedule Announced by BTEUP Lucknow", "Examination",
             "All students of 2nd, 4th, and 6th semester are informed that Board examinations will commence from next month. Check the student notice board for admit cards.",
             "18 Oct 2026", 0, None),
            ("Special Placement Drive by Leading Infrastructure & IT Companies", "Placement",
             "Final year students of CSE, ME, Civil, and EEE are requested to submit updated resumes to the Training & Placement Cell by Friday.",
             "12 Oct 2026", 1, None),
            ("AICTE National Level Tech Fest & Science Model Exhibition", "Events",
             "Government Polytechnic Mahasi will organize the Annual Inter-College Technical Exhibition. Cash prizes and merit certificates will be awarded to winners.",
             "05 Oct 2026", 0, None),
            ("Industrial Training & Internship Guidelines for Summer 2026", "Academic",
             "Mandatory 4-week industrial summer training guidelines have been updated for Mechanical and Civil engineering departments.",
             "28 Sep 2026", 0, None)
        ]
        cursor.executemany("""
        INSERT INTO notices (title, category, content, published_date, is_urgent, attachment_url)
        VALUES (?, ?, ?, ?, ?, ?)
        """, initial_notices)
        conn.commit()

    # Seed Faculty if empty
    cursor.execute("SELECT COUNT(*) FROM faculty")
    if cursor.fetchone()[0] == 0:
        initial_faculty = [
            ("Er. Subodh Mishra", "Director", "Administration & Governance", "M.Tech, FIE, 24+ Yrs Exp.", 24, "director@gpmahasi.ac.in", "+91 9450000001", 1),
            ("Er. Rajan Singh", "Principal", "Administration & Academic Affairs", "M.Tech (Engineering), 18+ Yrs Exp.", 18, "principal@gpmahasi.ac.in", "+91 9450000002", 1),
            ("Er. Avinash Kumar", "Chief System Architect & Technical Lead", "Computer Science & IT Infrastructure", "B.Tech (CSE) / Full-Stack Engineer", 6, "avinash.tech@gpmahasi.ac.in", "+91 8423072439", 1),
            ("Er. Vivek Sharma", "HOD & Associate Professor", "Computer Science & Engineering", "M.Tech (CSE), B.Tech", 12, "cse.hod@gpmahasi.ac.in", "+91 9450000010", 1),
            ("Er. Anjali Verma", "Assistant Professor", "Computer Science & Engineering", "M.Tech (AI & Software Systems)", 7, "anjali.cse@gpmahasi.ac.in", "+91 9450000011", 0),
            ("Er. R. K. Maurya", "HOD & Associate Professor", "Civil Engineering", "M.Tech (Structural Engg.)", 15, "civil.hod@gpmahasi.ac.in", "+91 9450000020", 1),
            ("Er. Deepak Tiwari", "Assistant Professor & Survey Lab Incharge", "Civil Engineering", "B.Tech (Civil), M.Tech", 8, "deepak.civil@gpmahasi.ac.in", "+91 9450000021", 0),
            ("Er. Amit Srivastava", "HOD & Associate Professor", "Mechanical Engineering", "M.Tech (Thermal & Design)", 14, "me.hod@gpmahasi.ac.in", "+91 9450000030", 1),
            ("Er. Saurabh Yadav", "Workshop Superintendent", "Mechanical Engineering", "B.Tech (Mech), Cad/Cam Certified", 9, "saurabh.me@gpmahasi.ac.in", "+91 9450000031", 0),
            ("Er. Neha Pandey", "HOD & Assistant Professor", "Electrical & Electronics Engineering", "M.Tech (Power Electronics)", 10, "eee.hod@gpmahasi.ac.in", "+91 9450000040", 1),
            ("Er. Manoj Kumar", "Assistant Professor", "Electrical & Electronics Engineering", "B.Tech, M.Tech (Embedded Systems)", 6, "manoj.eee@gpmahasi.ac.in", "+91 9450000041", 0)
        ]
        cursor.executemany("""
        INSERT INTO faculty (name, designation, department, qualification, experience_years, email, phone, is_hod)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_faculty)
        conn.commit()

    # Seed Sample Students if empty
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        initial_students = [
            ("240891001", "E2408911001", "Aman Verma", "Computer Science & Engineering", 4, "2024-2027", "9876543210", "aman.v@example.com", "Paid", 92.5),
            ("240891002", "E2408911002", "Pooja Singh", "Computer Science & Engineering", 4, "2024-2027", "9876543211", "pooja.s@example.com", "Paid", 89.0),
            ("240892001", "E2408921001", "Rohan Tiwari", "Civil Engineering", 2, "2025-2028", "9876543212", "rohan.t@example.com", "Paid", 87.5),
            ("240892002", "E2408921002", "Shalini Patel", "Civil Engineering", 6, "2023-2026", "9876543213", "shalini.p@example.com", "Paid", 94.0),
            ("240893001", "E2408931001", "Vikram Rathore", "Mechanical Engineering", 4, "2024-2027", "9876543214", "vikram.r@example.com", "Pending", 78.5),
            ("240893002", "E2408931002", "Aditya Gupta", "Mechanical Engineering", 2, "2025-2028", "9876543215", "aditya.g@example.com", "Paid", 91.2),
            ("240894001", "E2408941001", "Priya Mishra", "Electrical & Electronics Engineering", 6, "2023-2026", "9876543216", "priya.m@example.com", "Paid", 96.0),
            ("240894002", "E2408941002", "Rahul Yadav", "Electrical & Electronics Engineering", 2, "2025-2028", "9876543217", "rahul.y@example.com", "Paid", 84.5)
        ]
        cursor.executemany("""
        INSERT INTO students (roll_no, enrollment_no, full_name, branch, semester, academic_year, phone, email, fee_status, attendance_percent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_students)
        conn.commit()

    # Seed Sample Applications if empty
    cursor.execute("SELECT COUNT(*) FROM applications")
    if cursor.fetchone()[0] == 0:
        initial_apps = [
            ("GPMB-2026-1001", "Mohit Pandey", "Surya Prakash Pandey", "Kusum Pandey", "2007-06-15", "Male", "General", "mohit.p@gmail.com", "9123456780", "Vill - Ramgaon, Mahasi", "Bahraich", "Uttar Pradesh", "271824", "Computer Science & Engineering", "UP Board", 84.6, 79.2, "2609812", 4520, "Approved", "All documents verified by Admission Committee"),
            ("GPMB-2026-1002", "Ananya Srivastava", "Satish Kumar Srivastava", "Sunita Srivastava", "2008-01-20", "Female", "General", "ananya.s@gmail.com", "9123456781", "Civil Lines, Near D.M. Office", "Bahraich", "Uttar Pradesh", "271801", "Civil Engineering", "CBSE", 88.2, None, "2608411", 3120, "Approved", "Merit verified. Seat allocated."),
            ("GPMB-2026-1003", "Sachin Verma", "Harish Chandra Verma", "Meena Devi", "2007-11-04", "Male", "OBC", "sachin.v@gmail.com", "9123456782", "Chilwariya Sugar Mill Colony", "Bahraich", "Uttar Pradesh", "271870", "Mechanical Engineering", "UP Board", 76.4, 72.0, "2612093", 11450, "Pending Review", "Awaiting 10th marksheet re-verification"),
            ("GPMB-2026-1004", "Shweta Gautam", "Ramesh Kumar Gautam", "Kamla Devi", "2007-09-12", "Female", "SC", "shweta.g@gmail.com", "9123456783", "Nanpara Road", "Bahraich", "Uttar Pradesh", "271865", "Electrical & Electronics Engineering", "UP Board", 81.5, 78.0, "2605510", 6890, "Under Review", "Counseling scheduled for Friday")
        ]
        cursor.executemany("""
        INSERT INTO applications (app_no, full_name, father_name, mother_name, dob, gender, category, email, phone, address, district, state, pincode, branch, high_school_board, high_school_percent, intermediate_percent, jeecup_roll_no, jeecup_rank, status, admin_remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_apps)
        conn.commit()

    # Seed Sample Enquiries
    cursor.execute("SELECT COUNT(*) FROM enquiries")
    if cursor.fetchone()[0] == 0:
        initial_enq = [
            ("Devendra Singh", "devendra.s@gmail.com", "9811223344", "Hostel Availability & Fees", "Kindly inform if boys hostel facilities are available for 1st year CSE students.", "Resolved"),
            ("Sunil Pathak", "sunil.p@yahoo.com", "9933445566", "Direct Admission Lateral Entry", "I have completed ITI (Fitter). Can I apply for 2nd year Mechanical Engineering lateral entry?", "New")
        ]
        cursor.executemany("""
        INSERT INTO enquiries (full_name, email, phone, subject, message, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, initial_enq)
        conn.commit()

    # Seed Initial Gallery Photos if empty
    cursor.execute("SELECT COUNT(*) FROM gallery_photos")
    if cursor.fetchone()[0] == 0:
        initial_photos = [
            ("Main Academic Building & Front Lawn", "Infrastructure", "/static/assets/campus-main.jpg", "Front elevation and entrance portico of Government Polytechnic Mahasi, Bahraich"),
            ("Diploma Engineering Scholars", "Students", "/static/assets/campus-students.jpg", "Classroom & laboratory session in official college uniform • Er. Avinash Kumar & Peers"),
            ("Academic Corridor Wing", "Campus", "/static/assets/campus-corridor.jpg", "Spacious, naturally lit corridors with safety railings connecting lecture halls"),
            ("Front Porch & Administrative Block", "Infrastructure", "/static/assets/campus-building-vert.jpg", "राजकीय पॉलिटेक्निक महसी (बहराइच) मुख्य द्वार एवं प्रशासनिक परिसर"),
            ("Multi-Story Campus Block", "Campus", "/static/assets/campus-hostel-block.jpg", "Multi-level wings housing specialized laboratories and workshops")
        ]
        cursor.executemany("""
        INSERT INTO gallery_photos (title, category, image_data, caption)
        VALUES (?, ?, ?, ?)
        """, initial_photos)
        conn.commit()

    # Seed Site Settings if empty
    cursor.execute("SELECT COUNT(*) FROM site_settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT image_data FROM gallery_photos ORDER BY id ASC LIMIT 1")
        photo_row = cursor.fetchone()
        default_img = photo_row[0] if photo_row else "/static/assets/campus-main.jpg"

        initial_settings = [
            ("featured_campus_image", default_img),
            ("featured_campus_title", "🏛️ Official Campus Building"),
            ("featured_campus_subtitle", "Multi-Story Academic Wing & Student Campus"),
            ("featured_campus_aspect", "16:9")
        ]
        cursor.executemany("""
        INSERT OR REPLACE INTO site_settings (key, value)
        VALUES (?, ?)
        """, initial_settings)
        conn.commit()

    # Seed Sample Academic PDF Documents if empty
    cursor.execute("SELECT COUNT(*) FROM documents")
    if cursor.fetchone()[0] == 0:
        import base64
        sample_pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\n5 0 obj\n<<\n/Length 75\n>>\nstream\nBT\n/F1 16 Tf\n50 720 Td\n(Government Polytechnic Mahasi, Bahraich - Official Document) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000261 00000 n \n0000000340 00000 n \ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n467\n%%EOF\n"
        sample_pdf_base64 = "data:application/pdf;base64," + base64.b64encode(sample_pdf_bytes).decode("utf-8")
        today_date = date.today().strftime("%d %b %Y")

        initial_docs = [
            ("Diploma Engineering Admission Prospectus 2026-27", "Admissions", "GPM_Admission_Prospectus_2026-27.pdf", sample_pdf_base64, 480, today_date, "Complete admission guide, eligibility, seat matrix & counseling schedule for CSE, Civil, ME & EEE branches.", 142),
            ("BTEUP Even Semester Examination Scheme & Schedule", "Examination", "BTEUP_Exam_Schedule_Semester_2026.pdf", sample_pdf_base64, 320, "22 Oct 2026", "Official Board of Technical Education UP date-sheet, timing and examination center guidelines.", 289),
            ("CSE Branch 3-Year Complete Curriculum & Syllabus (BTEUP)", "Syllabus", "BTEUP_CSE_Diploma_Syllabus.pdf", sample_pdf_base64, 615, "15 Oct 2026", "AICTE & BTEUP revised course syllabus, semester subjects, lab experiments and marking scheme.", 95),
            ("Polytechnic Scholarship & Fee Structure Notification", "Fee & Guidelines", "GPM_Scholarship_Fee_Structure.pdf", sample_pdf_base64, 250, "10 Oct 2026", "UP Post-Matric scholarship eligibility criteria, income guidelines and annual fee breakdown.", 178)
        ]
        cursor.executemany("""
        INSERT INTO documents (title, category, file_name, file_data, file_size_kb, uploaded_date, description, download_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_docs)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
