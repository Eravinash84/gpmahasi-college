# 🏛️ Government Polytechnic Mahasi, Bahraich (PPP Mode)
### 100% Complete Full-Stack 3D College Portal & Secretariat Management System

---

## 📌 Project Overview
A production-ready, interactive 3D web application and College Management System (CMS) custom-built for **Government Polytechnic Mahasi, Bahraich (PPP Mode)**.

* **Chief System Architect & Developer:** **Er. Avinash Kumar**
* **Helpline & WhatsApp Support:** **+91 8423072439**
* **Director:** Er. Subodh Mishra
* **Principal:** Er. Rajan Singh
* **Approved by:** AICTE (All India Council for Technical Education, New Delhi)
* **Affiliated to:** BTEUP (Board of Technical Education Uttar Pradesh, Lucknow)
* **Operating Model:** Public-Private Partnership (PPP Mode)
* **Diploma Branches (3-Year Programs):**
  1. Computer Science & Engineering (CSE) - 60 Seats
  2. Civil Engineering - 60 Seats
  3. Mechanical Engineering (ME) - 60 Seats
  4. Electrical & Electronics Engineering (EEE) - 60 Seats

---

## 🌟 Key Highlights & Features

### 1. 🎨 Frontend & 3D Interactive Graphics
* **3D Hero Wireframe Tech Core:** Real-time mathematical WebGL/Canvas 3D rendering with glowing geodesic polyhedron, orbiting technical rings, and dynamic floating particles responding to cursor movement.
* **Interactive 3D Department Visualizer:**
  * **CSE:** 3D Holographic Cube Matrix with animated data packets.
  * **Civil:** 3D Warren Structural Truss & Bridge model with joint load pins.
  * **Mechanical:** 3D Interlocking Gear Train Transmission rotating in real-time.
  * **EEE:** 3D Electromagnetic Torus Field & Pulsing Sine Waves.
* **3D Perspective Tilt Cards:** Hovering over leadership and facility cards dynamically tilts them with 3D depth and glare.
* **Mobile Responsive:** Works seamlessly across mobile phones, tablets, laptops, and 4K displays.

### 2. 📝 Student Admissions & Public Portal
* **Live Admission Ticker & Flash News Marquee**
* **Director & Principal Visionary Messages**
* **Online Admission Registration Form:** Collects candidate info, 10th %, JEECUP details, auto-generates unique application IDs (`GPMB-2026-XXXX`), and prints instant admission slips.
* **Real-Time Application Status Tracker:** Candidates can track review status (Pending Review / Approved / Rejected) directly by entering their Application ID.
* **Live Notice Board:** Filterable by Admissions, Examinations, Placements, and Events.
* **Campus Facilities Showcase:** High-tech computer labs, mechanical workshop, surveying stations, smart classrooms, library, and hostel.
* **Direct Grievance / Contact Form**

### 3. 🔐 College Management Admin Secretariat Portal (`/admin`)
* **Secure Authentication:** Session tokens with SHA-256 password hashing.
* **Dashboard Analytics:** Live metrics of total students, applications, approval rates, active notices, and branch distribution charts.
* **Applications Manager:** Filter student applications by branch and status; 1-click **Approve** (which automatically enrolls the student into the active directory with a roll number) or **Reject**.
* **Student Directory CRUD:** Manage enrolled students, semesters, roll numbers, and fee status.
* **Notice Board Manager:** Publish new circulars with priority tags (Urgent/Normal) that immediately sync with the live website.
* **Faculty Directory:** Add, view, and manage department professors, HODs, qualifications, and experience.
* **Enquiry Inbox:** Review queries sent via contact form and mark them resolved.

### 4. 🗄️ Relational Database (SQLite)
* Zero external database setup needed; pre-seeded and ready to use in `polytechnic.db`.
* Includes 6 core tables: `admin_users`, `applications`, `students`, `notices`, `faculty`, `enquiries`.

---

## 🚀 How to Run the Website

### Method 1: 1-Click Launch (Easiest)
Simply double-click on **`start.bat`**.  
It will automatically open your default browser at `http://localhost:8080` and start the server!

### Method 2: Terminal / Command Line
1. Open PowerShell or Command Prompt.
2. Navigate to this folder:
   ```powershell
   cd "C:\Users\Avinash Kumar\.gemini\antigravity\scratch\govt-polytechnic-mahasi"
   ```
3. Run the server:
   ```powershell
   python server.py
   ```
4. Open your browser and visit:
   * **Public Website:** [http://localhost:8080](http://localhost:8080)
   * **Admin Secretariat Portal:** [http://localhost:8080/admin](http://localhost:8080/admin)

---

## 🔑 Default Administrator Credentials
* **Username:** `admin`
* **Password:** `admin123`

*(You can change the credentials in `database.py` or directly update the `admin_users` table).*

---

## 🌐 How to Host Online & Connect Domain

### Step 1: Deploy to Cloud (Free on Render or Railway)
1. Upload this folder to your GitHub repository.
2. Go to **Render.com** or **Railway.app** & create a new **Web Service**.
3. Select Python environment and set:
   * **Build Command:** `python database.py`
   * **Start Command:** `python server.py`
4. Your website will be live 24/7 with a free HTTPS URL!

### Step 2: Link Your Custom Domain (e.g., `gpmahasi.ac.in`)
1. Purchase your domain from GoDaddy, Hostinger, or Namecheap.
2. In your Render / Hosting dashboard, click **Add Custom Domain**.
3. Add the two DNS records shown (CNAME and A Record) into your GoDaddy DNS settings.
4. Your custom domain is now live with automatic SSL security!

---

© 2026 Government Polytechnic Mahasi, Bahraich (PPP Mode).
