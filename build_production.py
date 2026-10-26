import os
import re

base_dir = r"C:\Users\Avinash Kumar\.gemini\antigravity\scratch\govt-polytechnic-mahasi"

# Read CSS and JS files
with open(os.path.join(base_dir, "static", "css", "styles.css"), "r", encoding="utf-8") as f:
    css_content = f.read()

with open(os.path.join(base_dir, "static", "js", "three_engine.js"), "r", encoding="utf-8") as f:
    three_content = f.read()

with open(os.path.join(base_dir, "static", "js", "app.js"), "r", encoding="utf-8") as f:
    app_content = f.read()

with open(os.path.join(base_dir, "static", "js", "admin.js"), "r", encoding="utf-8") as f:
    admin_js_content = f.read()

# -----------------
# 1. Update index.html
# -----------------
with open(os.path.join(base_dir, "static", "index.html"), "r", encoding="utf-8") as f:
    index_html = f.read()

# Replace top-notice-bar
old_ticker_pattern = re.compile(r'<div class="top-notice-bar".*?</div>\s*</div>\s*</div>', re.DOTALL)
new_ticker = """<div class="top-notice-bar">
        <div class="container notice-ticker-wrapper">
            <div class="ticker-badge-fixed">
                <span class="pulse-dot"></span>
                <span>⚡ FLASH NEWS</span>
            </div>
            <div class="ticker-viewport">
                <div class="ticker-marquee">
                    ⚡ <strong>ADMISSIONS 2026-27:</strong> Direct & JEECUP Counseling Registrations Open for CSE, Civil, Mechanical & EEE Branches! &nbsp;•&nbsp; 
                    📞 <strong>DIRECT HELPLINE:</strong> Call / WhatsApp: <strong>+91 8423072439 (Er. Avinash Kumar)</strong> &nbsp;•&nbsp; 
                    📢 <strong>BTEUP EXAM UPDATE:</strong> Even Semester Examination Scheme & Admit Cards Released &nbsp;•&nbsp; 
                    🎯 <strong>CAMPUS PLACEMENT:</strong> Special Technical Recruitment Drive Underway &nbsp;•&nbsp; 
                    🏛️ Approved by AICTE, New Delhi & Affiliated to Board of Technical Education Uttar Pradesh (BTEUP Lucknow)
                </div>
            </div>
        </div>
    </div>"""

if old_ticker_pattern.search(index_html):
    index_html = old_ticker_pattern.sub(new_ticker, index_html, count=1)
    print("Replaced ticker with new structure.")
else:
    print("WARNING: Old ticker pattern not matched by regex!")

# Add Faculty to Navbar if not there
if '<li><a href="#faculty">Faculty</a></li>' not in index_html:
    index_html = index_html.replace(
        '<li><a href="#departments">Branches</a></li>',
        '<li><a href="#departments">Branches</a></li>\n                <li><a href="#faculty">Faculty</a></li>'
    )
    print("Added Faculty link to navbar.")

# Add Faculty Section if not there
faculty_section = """
    <!-- Faculty & Academic Staff Section -->
    <section class="section section-alt" id="faculty">
        <div class="container">
            <div class="section-head">
                <span class="section-tag">Eminent Faculty & Leadership</span>
                <h2 class="section-title">Distinguished Professors & Instructors</h2>
                <p class="section-subtitle">
                    Experienced mentors, scholars, and technical specialists dedicated to fostering next-generation engineering talent at G.P. Mahasi.
                </p>
            </div>

            <div class="faculty-grid" id="facultyGrid">
                <!-- Dynamically populated from /api/faculty via loadFacultyPublic() -->
            </div>
        </div>
    </section>
"""

if 'id="faculty"' not in index_html:
    # Insert after departments section
    dept_end = '</section>\n\n    <!-- Notices & Circulars Section -->'
    if dept_end in index_html:
        index_html = index_html.replace(dept_end, f'</section>\n{faculty_section}\n    <!-- Notices & Circulars Section -->')
        print("Inserted faculty section before notices.")
    else:
        # try another insertion point
        index_html = index_html.replace('<section class="section section-alt" id="notices">', f'{faculty_section}\n    <section class="section section-alt" id="notices">')
        print("Inserted faculty section before notices (alt).")

# Replace gallery section with dynamic gallery
new_gallery = """    <!-- Campus Life & Photo Gallery Section -->
    <section class="section" id="gallery" style="background: rgba(10, 16, 32, 0.6); border-top: 1px solid var(--border-glass); border-bottom: 1px solid var(--border-glass);">
        <div class="container">
            <div class="section-head">
                <span class="section-tag">Campus Life & Infrastructure</span>
                <h2 class="section-title">Official Campus Photo Gallery</h2>
                <p class="section-subtitle">
                    Real photographs of Government Polytechnic Mahasi, Bahraich — Academic blocks, engineering scholars, and campus facilities.
                </p>
                <div style="display:flex; justify-content:center; gap:10px; margin-top:20px; flex-wrap:wrap;">
                    <button class="btn btn-sm btn-outline active" data-gallery-cat="All">All Photos</button>
                    <button class="btn btn-sm btn-outline" data-gallery-cat="Campus">Campus & Building</button>
                    <button class="btn btn-sm btn-outline" data-gallery-cat="Students">Scholars & Students</button>
                    <button class="btn btn-sm btn-outline" data-gallery-cat="Academics">Academic Labs</button>
                    <button class="btn btn-sm btn-outline" data-gallery-cat="Events">Workshops & Events</button>
                </div>
            </div>

            <div class="gallery-grid" id="galleryGrid">
                <!-- Dynamically populated from /api/gallery via loadGallery() -->
            </div>
        </div>
    </section>"""

old_gallery_pattern = re.compile(r'<!-- Campus Life & Photo Gallery Section -->.*?<section class="section" id="gallery".*?</section>', re.DOTALL)
if old_gallery_pattern.search(index_html):
    index_html = old_gallery_pattern.sub(new_gallery, index_html, count=1)
    print("Replaced hardcoded gallery with dynamic gallery.")
else:
    print("WARNING: Old gallery pattern not matched!")

# Replace CSS block
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
new_style = f"<style>\n{css_content}\n</style>"
if style_pattern.search(index_html):
    index_html = style_pattern.sub(new_style, index_html, count=1)
    print("Replaced CSS style block.")
else:
    index_html = index_html.replace("</head>", f"{new_style}\n</head>")
    print("Appended CSS style block before </head>.")

# Replace Script block
# Remove any scripts right before </body>
body_pattern = re.compile(r'(<script>.*?</script>\s*)+</body>', re.DOTALL)
new_scripts = f"<script>\n{three_content}\n</script>\n<script>\n{app_content}\n</script>\n</body>"
if body_pattern.search(index_html):
    index_html = body_pattern.sub(new_scripts, index_html, count=1)
    print("Replaced script blocks before </body>.")
else:
    index_html = index_html.replace("</body>", f"{new_scripts}")
    print("Appended scripts before </body>.")

with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
with open(os.path.join(base_dir, "static", "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print(f"index.html successfully updated and bundled. New size: {len(index_html)} bytes")


# -----------------
# 2. Update admin.html
# -----------------
with open(os.path.join(base_dir, "static", "admin.html"), "r", encoding="utf-8") as f:
    admin_html = f.read()

# Add Gallery nav item if not there
gallery_nav_item = """            <div class="admin-nav-item" data-tab="tabFaculty">
                <span>👨‍🏫</span> Faculty Directory
            </div>

            <div class="admin-nav-item" data-tab="tabGallery">
                <span>📸</span> Campus Photos Manager
            </div>"""

if 'data-tab="tabGallery"' not in admin_html:
    admin_html = admin_html.replace(
        """            <div class="admin-nav-item" data-tab="tabFaculty">
                <span>👨‍🏫</span> Faculty Directory
            </div>""",
        gallery_nav_item
    )
    print("Added Campus Photos Manager to admin nav.")

# Add Gallery tab content if not there
gallery_tab_content = """            <!-- TAB: CAMPUS PHOTOS MANAGER -->
            <div id="tabGallery" class="admin-tab-content" style="display:none;">
                <div style="display:grid; grid-template-columns: 1fr 1.3fr; gap:26px;">
                    <!-- Add Photo Form -->
                    <div style="background:var(--bg-card); border:1px solid var(--border-glass); border-radius:var(--radius-lg); padding:26px;">
                        <h3 style="font-size:1.15rem; color:#fff; margin-bottom:18px;">Upload Campus Photo</h3>
                        <form id="addPhotoForm">
                            <div class="form-group" style="margin-bottom:14px;">
                                <label class="form-label">Photo Title *</label>
                                <input type="text" id="newPhotoTitle" class="form-input" placeholder="e.g. Main Multi-Story Academic Wing" required>
                            </div>
                            <div class="form-group" style="margin-bottom:14px;">
                                <label class="form-label">Category *</label>
                                <select id="newPhotoCategory" class="form-select" required>
                                    <option value="Campus">Campus & Building</option>
                                    <option value="Students">Scholars & Students</option>
                                    <option value="Academics">Academic Labs & Classrooms</option>
                                    <option value="Events">Workshops & Events</option>
                                </select>
                            </div>
                            <div class="form-group" style="margin-bottom:14px;">
                                <label class="form-label">Description / Caption</label>
                                <input type="text" id="newPhotoCaption" class="form-input" placeholder="e.g. State-of-the-art administrative & lecture halls">
                            </div>
                            <div class="form-group" style="margin-bottom:14px;">
                                <label class="form-label">Select Image File (Direct Upload) *</label>
                                <input type="file" id="newPhotoFileInput" class="form-input" accept="image/*" style="padding:8px;">
                                <small style="color:#94a3b8; font-size:0.75rem; display:block; margin-top:4px;">Uploads from phone/PC are automatically optimized & saved to database.</small>
                            </div>
                            <div class="form-group" style="margin-bottom:14px;">
                                <label class="form-label">Or Image URL (Optional)</label>
                                <input type="url" id="newPhotoUrlInput" class="form-input" placeholder="https://example.com/photo.jpg">
                            </div>
                            
                            <!-- Live Preview Box -->
                            <div id="photoPreviewContainer" style="display:none; margin-bottom:16px; border:1px dashed var(--primary-light); border-radius:10px; padding:10px; text-align:center;">
                                <p style="font-size:0.75rem; color:#38bdf8; margin-bottom:6px;">Image Preview</p>
                                <img id="photoPreviewImg" src="" alt="Preview" style="max-width:100%; max-height:180px; border-radius:6px; object-fit:contain;">
                            </div>

                            <button type="submit" id="btnUploadPhoto" class="btn btn-primary" style="width:100%;">
                                🚀 Publish Photo to Website
                            </button>
                        </form>
                    </div>

                    <!-- Manage Current Photos -->
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
                            <h3 style="font-size:1.15rem; color:#fff; margin:0;">Live Campus Gallery Photos</h3>
                            <button class="btn btn-sm btn-outline" onclick="loadGalleryAdmin()">🔄 Refresh</button>
                        </div>
                        <div id="adminGalleryList" style="display:flex; flex-direction:column; gap:12px; max-height:680px; overflow-y:auto; padding-right:6px;">
                            <!-- Populated dynamically by loadGalleryAdmin() -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 6: PUBLIC ENQUIRIES -->"""

if 'id="tabGallery"' not in admin_html:
    admin_html = admin_html.replace(
        "<!-- TAB 6: PUBLIC ENQUIRIES -->",
        gallery_tab_content
    )
    print("Added Campus Photos Manager tab content to admin.html.")

# Replace CSS block in admin
if style_pattern.search(admin_html):
    admin_html = style_pattern.sub(new_style, admin_html, count=1)
    print("Replaced CSS style block in admin.html.")
else:
    admin_html = admin_html.replace("</head>", f"{new_style}\n</head>")

# Replace Script block in admin
admin_scripts = f"<script>\n{admin_js_content}\n</script>\n</body>"
if body_pattern.search(admin_html):
    admin_html = body_pattern.sub(admin_scripts, admin_html, count=1)
    print("Replaced script blocks in admin.html.")
else:
    admin_html = admin_html.replace("</body>", f"{admin_scripts}")

with open(os.path.join(base_dir, "admin.html"), "w", encoding="utf-8") as f:
    f.write(admin_html)
with open(os.path.join(base_dir, "static", "admin.html"), "w", encoding="utf-8") as f:
    f.write(admin_html)
print(f"admin.html successfully updated and bundled. New size: {len(admin_html)} bytes")
