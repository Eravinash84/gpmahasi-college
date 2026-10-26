"""
Production Full-Stack Web Server for:
Government Polytechnic Mahasi, Bahraich (PPP Mode)
Features:
- REST API Engine
- SQLite Database Operations
- Session Management for Admin Portal
- High performance ThreadingHTTPServer
"""

import http.server
import socketserver
import os
import json
import sqlite3
import mimetypes
import secrets
import hashlib
from urllib.parse import urlparse, parse_qs
from datetime import datetime, date

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "polytechnic.db")

# In-memory active admin sessions
ACTIVE_SESSIONS = set()

def resolve_file(rel_path):
    """
    Bulletproof file locator.
    Searches STATIC_DIR, BASE_DIR, and any nested subdirectories.
    Prevents 'File Not Found' regardless of how files were uploaded to GitHub/Render.
    """
    clean = rel_path.lstrip("/").replace("\\", "/")
    if clean.startswith("static/"):
        sub = clean[7:]
    else:
        sub = clean

    candidates = [
        os.path.join(STATIC_DIR, sub),
        os.path.join(STATIC_DIR, clean),
        os.path.join(BASE_DIR, sub),
        os.path.join(BASE_DIR, clean),
        os.path.join(BASE_DIR, "govt-polytechnic-mahasi", "static", sub),
        os.path.join(BASE_DIR, "govt-polytechnic-mahasi", sub),
    ]

    for c in candidates:
        if os.path.exists(c) and os.path.isfile(c):
            return c

    # Fallback: search recursively in BASE_DIR for the exact filename
    target = os.path.basename(clean)
    if target:
        for root, _, files in os.walk(BASE_DIR):
            if target in files:
                return os.path.join(root, target)

    return None

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_pass(pwd: str) -> str:
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()

MIME_MAP = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
    ".json": "application/json; charset=utf-8",
    ".ico": "image/x-icon",
    ".txt": "text/plain; charset=utf-8",
}

class PolytechnicRequestHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Concise logging
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]} - {args[1]}")

    def send_json(self, data, status_code=200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status_code=400):
        self.send_json({"success": False, "error": message}, status_code)

    def parse_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw_data = self.rfile.read(content_length).decode("utf-8")
            return json.loads(raw_data)
        return {}

    def is_admin_authenticated(self):
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            return token in ACTIVE_SESSIONS
        return False

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # API Endpoints
        if path.startswith("/api/"):
            return self.handle_api_get(path, query)

        # Clean routing for pages
        if path == "/" or path == "" or path == "/index.html":
            target = resolve_file("index.html")
            if target:
                return self.serve_file(target)
        elif path == "/admin" or path == "/admin/" or path == "/admin.html":
            target = resolve_file("admin.html")
            if target:
                return self.serve_file(target)

        # Static asset serving
        resolved_file = resolve_file(path)
        if resolved_file:
            return self.serve_file(resolved_file)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def handle_api_get(self, path, query):
        conn = get_db()
        cursor = conn.cursor()

        try:
            # 1. Dashboard Statistics
            if path == "/api/stats":
                cursor.execute("SELECT COUNT(*) FROM students")
                total_students = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM applications")
                total_apps = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Approved'")
                approved_apps = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Pending Review'")
                pending_apps = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM notices")
                total_notices = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM faculty")
                total_faculty = cursor.fetchone()[0]

                # Branch breakdown of applications
                cursor.execute("SELECT branch, COUNT(*) as count FROM applications GROUP BY branch")
                branch_counts = {row["branch"]: row["count"] for row in cursor.fetchall()}

                self.send_json({
                    "success": True,
                    "stats": {
                        "total_students": total_students,
                        "total_applications": total_apps,
                        "approved_applications": approved_apps,
                        "pending_applications": pending_apps,
                        "total_notices": total_notices,
                        "total_faculty": total_faculty,
                        "branches_count": 4,
                        "branch_distribution": branch_counts
                    }
                })

            # 2. Notices
            elif path == "/api/notices":
                category = query.get("category", [None])[0]
                if category and category != "All":
                    cursor.execute("SELECT * FROM notices WHERE category = ? ORDER BY id DESC", (category,))
                else:
                    cursor.execute("SELECT * FROM notices ORDER BY is_urgent DESC, id DESC")
                rows = [dict(row) for row in cursor.fetchall()]
                self.send_json({"success": True, "notices": rows})

            # 3. Track Application by app_no
            elif path == "/api/applications/track":
                app_no = query.get("app_no", [""])[0].strip()
                if not app_no:
                    return self.send_error_json("Please provide Application ID.")
                cursor.execute("SELECT app_no, full_name, branch, status, admin_remarks, created_at FROM applications WHERE LOWER(app_no) = LOWER(?)", (app_no,))
                row = cursor.fetchone()
                if row:
                    self.send_json({"success": True, "application": dict(row)})
                else:
                    self.send_error_json("Application ID not found. Please verify and try again.", 404)

            # 4. List Applications (Admin Only)
            elif path == "/api/applications":
                branch = query.get("branch", [None])[0]
                status = query.get("status", [None])[0]
                sql = "SELECT * FROM applications WHERE 1=1"
                params = []
                if branch and branch != "All":
                    sql += " AND branch = ?"
                    params.append(branch)
                if status and status != "All":
                    sql += " AND status = ?"
                    params.append(status)
                sql += " ORDER BY id DESC"
                cursor.execute(sql, params)
                rows = [dict(row) for row in cursor.fetchall()]
                self.send_json({"success": True, "applications": rows})

            # 5. Students Directory
            elif path == "/api/students":
                branch = query.get("branch", [None])[0]
                sql = "SELECT * FROM students WHERE 1=1"
                params = []
                if branch and branch != "All":
                    sql += " AND branch = ?"
                    params.append(branch)
                sql += " ORDER BY branch, roll_no"
                cursor.execute(sql, params)
                rows = [dict(row) for row in cursor.fetchall()]
                self.send_json({"success": True, "students": rows})

            # 6. Faculty Directory
            elif path == "/api/faculty":
                cursor.execute("SELECT * FROM faculty ORDER BY is_hod DESC, id ASC")
                rows = [dict(row) for row in cursor.fetchall()]
                self.send_json({"success": True, "faculty": rows})

            # 7. Enquiries (Admin Only)
            elif path == "/api/enquiries":
                cursor.execute("SELECT * FROM enquiries ORDER BY id DESC")
                rows = [dict(row) for row in cursor.fetchall()]
                self.send_json({"success": True, "enquiries": rows})

            # 7.1 Gallery Photos
            elif path == "/api/gallery":
                category = query.get("category", [None])[0]
                if category and category != "All":
                    cursor.execute("SELECT * FROM gallery_photos WHERE category = ? ORDER BY id DESC", (category,))
                else:
                    cursor.execute("SELECT * FROM gallery_photos ORDER BY id ASC")
                rows = [dict(row) for row in cursor.fetchall()]
                self.send_json({"success": True, "photos": rows})

            # 8. Check Auth Session
            elif path == "/api/auth/check":
                is_auth = self.is_admin_authenticated()
                self.send_json({"authenticated": is_auth})

            else:
                self.send_error_json("Unknown API endpoint", 404)

        finally:
            conn.close()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if not path.startswith("/api/"):
            return self.send_error_json("Invalid POST route", 404)

        try:
            payload = self.parse_json_body()
        except Exception:
            return self.send_error_json("Invalid JSON body in request")

        conn = get_db()
        cursor = conn.cursor()

        try:
            # 1. Admin Login
            if path == "/api/auth/login":
                username = payload.get("username", "").strip()
                password = payload.get("password", "").strip()

                if not username or not password:
                    return self.send_error_json("Username and password are required")

                pwd_hash = hash_pass(password)
                cursor.execute("SELECT id, username, full_name, role FROM admin_users WHERE username = ? AND password_hash = ?", (username, pwd_hash))
                user = cursor.fetchone()

                if user:
                    token = secrets.token_hex(24)
                    ACTIVE_SESSIONS.add(token)
                    return self.send_json({
                        "success": True,
                        "token": token,
                        "user": dict(user),
                        "message": "Login successful"
                    })
                else:
                    return self.send_error_json("Invalid username or password", 401)

            # 2. Admin Logout
            elif path == "/api/auth/logout":
                auth_header = self.headers.get("Authorization", "")
                if auth_header.startswith("Bearer "):
                    token = auth_header[7:].strip()
                    ACTIVE_SESSIONS.discard(token)
                return self.send_json({"success": True, "message": "Logged out successfully"})

            # 2.1 Admin Change Password & Username
            elif path == "/api/auth/change-password":
                if not self.is_admin_authenticated():
                    return self.send_error_json("Unauthorized. Please log in first.", 401)
                new_username = payload.get("new_username", "").strip()
                new_password = payload.get("new_password", "").strip()
                if not new_password or len(new_password) < 4:
                    return self.send_error_json("Password must be at least 4 characters")

                new_hash = hash_pass(new_password)
                if new_username:
                    cursor.execute("UPDATE admin_users SET username = ?, password_hash = ?", (new_username, new_hash))
                else:
                    cursor.execute("UPDATE admin_users SET password_hash = ?", (new_hash,))
                conn.commit()
                return self.send_json({"success": True, "message": "Credentials updated successfully!"})

            # 3. Public Student Online Admission Application
            elif path == "/api/applications":
                full_name = payload.get("full_name", "").strip()
                father_name = payload.get("father_name", "").strip()
                dob = payload.get("dob", "").strip()
                gender = payload.get("gender", "Male").strip()
                category = payload.get("category", "General").strip()
                email = payload.get("email", "").strip()
                phone = payload.get("phone", "").strip()
                address = payload.get("address", "").strip()
                district = payload.get("district", "Bahraich").strip()
                pincode = payload.get("pincode", "").strip()
                branch = payload.get("branch", "").strip()
                high_school_board = payload.get("high_school_board", "UP Board").strip()
                high_school_percent = float(payload.get("high_school_percent", 0.0))
                inter_percent = payload.get("intermediate_percent")
                jeecup_roll = payload.get("jeecup_roll_no", "")
                jeecup_rank = payload.get("jeecup_rank")

                if not full_name or not father_name or not phone or not branch or high_school_percent <= 0:
                    return self.send_error_json("Missing required admission fields.")

                # Generate unique Application ID: GPMB-2026-XXXX
                cursor.execute("SELECT COUNT(*) FROM applications")
                count = cursor.fetchone()[0] + 1001
                app_no = f"GPMB-2026-{count}"

                cursor.execute("""
                INSERT INTO applications (
                    app_no, full_name, father_name, dob, gender, category, email, phone,
                    address, district, pincode, branch, high_school_board, high_school_percent,
                    intermediate_percent, jeecup_roll_no, jeecup_rank, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending Review')
                """, (app_no, full_name, father_name, dob, gender, category, email, phone,
                      address, district, pincode, branch, high_school_board, high_school_percent,
                      inter_percent, jeecup_roll, jeecup_rank))
                conn.commit()

                return self.send_json({
                    "success": True,
                    "app_no": app_no,
                    "message": "Application submitted successfully! Please save your Application ID for status tracking."
                }, 201)

            # 4. Public Contact / Enquiry Form
            elif path == "/api/enquiries":
                full_name = payload.get("full_name", "").strip()
                email = payload.get("email", "").strip()
                phone = payload.get("phone", "").strip()
                subject = payload.get("subject", "").strip()
                message = payload.get("message", "").strip()

                if not full_name or not phone or not message:
                    return self.send_error_json("Name, phone and message are required.")

                cursor.execute("""
                INSERT INTO enquiries (full_name, email, phone, subject, message)
                VALUES (?, ?, ?, ?, ?)
                """, (full_name, email, phone, subject, message))
                conn.commit()

                return self.send_json({"success": True, "message": "Enquiry received. Our office will contact you soon."})

            # 5. Create Notice (Admin)
            elif path == "/api/notices":
                title = payload.get("title", "").strip()
                category = payload.get("category", "General").strip()
                content = payload.get("content", "").strip()
                is_urgent = 1 if payload.get("is_urgent") else 0
                today_str = date.today().strftime("%d %b %Y")

                if not title or not content:
                    return self.send_error_json("Notice title and content are required")

                cursor.execute("""
                INSERT INTO notices (title, category, content, published_date, is_urgent, posted_by)
                VALUES (?, ?, ?, ?, ?, 'Principal Office')
                """, (title, category, content, today_str, is_urgent))
                conn.commit()
                new_id = cursor.lastrowid
                return self.send_json({"success": True, "id": new_id, "message": "Notice published successfully"})

            # 6. Add Student (Admin)
            elif path == "/api/students":
                roll_no = payload.get("roll_no", "").strip()
                enrollment_no = payload.get("enrollment_no", "").strip()
                full_name = payload.get("full_name", "").strip()
                branch = payload.get("branch", "").strip()
                semester = int(payload.get("semester", 1))
                academic_year = payload.get("academic_year", "2026-2029").strip()
                phone = payload.get("phone", "").strip()
                email = payload.get("email", "").strip()
                fee_status = payload.get("fee_status", "Paid").strip()

                if not roll_no or not full_name or not branch:
                    return self.send_error_json("Roll number, name and branch are required.")

                cursor.execute("""
                INSERT INTO students (roll_no, enrollment_no, full_name, branch, semester, academic_year, phone, email, fee_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (roll_no, enrollment_no, full_name, branch, semester, academic_year, phone, email, fee_status))
                conn.commit()
                return self.send_json({"success": True, "message": "Student registered successfully"})

            # 7. Add Faculty (Admin)
            elif path == "/api/faculty":
                name = payload.get("name", "").strip()
                designation = payload.get("designation", "").strip()
                department = payload.get("department", "").strip()
                qualification = payload.get("qualification", "").strip()
                experience_years = int(payload.get("experience_years", 1))
                email = payload.get("email", "").strip()
                phone = payload.get("phone", "").strip()
                is_hod = 1 if payload.get("is_hod") else 0

                if not name or not designation or not department:
                    return self.send_error_json("Name, designation and department are required.")

                cursor.execute("""
                INSERT INTO faculty (name, designation, department, qualification, experience_years, email, phone, is_hod)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, designation, department, qualification, experience_years, email, phone, is_hod))
                conn.commit()
                return self.send_json({"success": True, "message": "Faculty added successfully"})

            # 8. Add Gallery Photo (Admin)
            elif path == "/api/gallery":
                title = payload.get("title", "").strip()
                category = payload.get("category", "Campus Life").strip()
                image_data = payload.get("image_data", "").strip()
                caption = payload.get("caption", "").strip()

                if not title or not image_data:
                    return self.send_error_json("Title and Image are required")

                cursor.execute("""
                INSERT INTO gallery_photos (title, category, image_data, caption)
                VALUES (?, ?, ?, ?)
                """, (title, category, image_data, caption))
                conn.commit()
                return self.send_json({"success": True, "id": cursor.lastrowid, "message": "Campus photo added successfully"})

            else:
                self.send_error_json("Endpoint not found", 404)

        finally:
            conn.close()

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            payload = self.parse_json_body()
        except Exception:
            return self.send_error_json("Invalid JSON body")

        conn = get_db()
        cursor = conn.cursor()

        try:
            # 1. Update Application Status (Approve / Reject)
            if path == "/api/applications/status":
                app_no = payload.get("app_no")
                new_status = payload.get("status")
                remarks = payload.get("admin_remarks", "")

                if not app_no or not new_status:
                    return self.send_error_json("app_no and status are required")

                cursor.execute("""
                UPDATE applications SET status = ?, admin_remarks = ? WHERE app_no = ?
                """, (new_status, remarks, app_no))
                conn.commit()

                # If Approved, check if student already added, if not auto-register to students table
                if new_status == "Approved":
                    cursor.execute("SELECT * FROM applications WHERE app_no = ?", (app_no,))
                    app_data = cursor.fetchone()
                    if app_data:
                        # Generate roll number
                        branch_code = "10" if "Computer" in app_data["branch"] else ("20" if "Civil" in app_data["branch"] else ("30" if "Mechanical" in app_data["branch"] else "40"))
                        gen_roll = f"26089{branch_code}{app_data['id']:03d}"
                        cursor.execute("SELECT id FROM students WHERE email = ? OR roll_no = ?", (app_data["email"], gen_roll))
                        if not cursor.fetchone():
                            cursor.execute("""
                            INSERT INTO students (roll_no, enrollment_no, full_name, branch, semester, academic_year, phone, email, fee_status)
                            VALUES (?, ?, ?, ?, 1, '2026-2029', ?, ?, 'Paid (Admission)')
                            """, (gen_roll, f"E{gen_roll}", app_data["full_name"], app_data["branch"], app_data["phone"], app_data["email"]))
                            conn.commit()

                return self.send_json({"success": True, "message": f"Application {app_no} updated to {new_status}"})

            # 2. Update Enquiry Status
            elif path == "/api/enquiries/status":
                enquiry_id = payload.get("id")
                new_status = payload.get("status", "Resolved")
                cursor.execute("UPDATE enquiries SET status = ? WHERE id = ?", (new_status, enquiry_id))
                conn.commit()
                return self.send_json({"success": True, "message": "Enquiry status updated"})

            # 3. Update Gallery Photo
            elif path == "/api/gallery":
                photo_id = payload.get("id")
                title = payload.get("title", "").strip()
                category = payload.get("category", "Campus Life").strip()
                caption = payload.get("caption", "").strip()
                if not photo_id:
                    return self.send_error_json("Photo ID is required")
                cursor.execute("UPDATE gallery_photos SET title = ?, category = ?, caption = ? WHERE id = ?", (title, category, caption, photo_id))
                conn.commit()
                return self.send_json({"success": True, "message": "Photo updated successfully"})

            else:
                self.send_error_json("Unknown PUT endpoint", 404)

        finally:
            conn.close()

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        conn = get_db()
        cursor = conn.cursor()

        try:
            if path == "/api/notices":
                notice_id = query.get("id", [None])[0]
                if not notice_id:
                    return self.send_error_json("Notice ID required")
                cursor.execute("DELETE FROM notices WHERE id = ?", (notice_id,))
                conn.commit()
                return self.send_json({"success": True, "message": "Notice deleted"})

            elif path == "/api/students":
                student_id = query.get("id", [None])[0]
                if not student_id:
                    return self.send_error_json("Student ID required")
                cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
                conn.commit()
                return self.send_json({"success": True, "message": "Student deleted"})

            elif path == "/api/faculty":
                faculty_id = query.get("id", [None])[0]
                if not faculty_id:
                    return self.send_error_json("Faculty ID required")
                cursor.execute("DELETE FROM faculty WHERE id = ?", (faculty_id,))
                conn.commit()
                return self.send_json({"success": True, "message": "Faculty deleted"})

            elif path == "/api/gallery":
                photo_id = query.get("id", [None])[0]
                if not photo_id:
                    return self.send_error_json("Photo ID required")
                cursor.execute("DELETE FROM gallery_photos WHERE id = ?", (photo_id,))
                conn.commit()
                return self.send_json({"success": True, "message": "Campus photo deleted"})

            else:
                self.send_error_json("Unknown DELETE endpoint", 404)

        finally:
            conn.close()

    def serve_file(self, full_path):
        if not os.path.exists(full_path):
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"File Not Found")
            return

        ext = os.path.splitext(full_path)[1].lower()
        mime_type = MIME_MAP.get(ext)
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(full_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        try:
            with open(full_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error reading file: {str(e)}".encode("utf-8"))

def run():
    # Make sure DB is ready
    import database
    database.init_db()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), PolytechnicRequestHandler) as httpd:
        print("=" * 70)
        print(" GOVT. POLYTECHNIC MAHASI, BAHRAICH (PPP MODE)")
        print(" 100% Full-Stack Portal with 3D Canvas & SQLite Database")
        print(f" Server running at: http://localhost:{PORT}")
        print(f" Admin Portal at:   http://localhost:{PORT}/admin")
        print(" Admin Credentials: admin / admin123")
        print("=" * 70)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")
            httpd.shutdown()

if __name__ == "__main__":
    run()
