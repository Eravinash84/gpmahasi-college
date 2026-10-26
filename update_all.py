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

# ==============================================================================
# 1. Update index.html
# ==============================================================================
with open(os.path.join(base_dir, "static", "index.html"), "r", encoding="utf-8") as f:
    index_html = f.read()

# 1.1 Replace Hero Right featured image box with 16:9 campus box
hero_box_pattern = re.compile(
    r'(<!-- Featured Real Campus Photo.*?-->\s*)<div style="position:relative;[^>]*height:165px;[^>]*>.*?</div>\s*</div>',
    re.DOTALL
)
new_hero_16_9 = """<!-- Featured Real Campus Photo (16:9 Aspect Ratio) -->
                <div class="campus-16-9-box" style="margin-bottom:18px;">
                    <img id="heroCampusImg" src="/static/assets/campus-main.jpg" alt="Official Campus Building">
                    <div class="campus-16-9-overlay">
                        <div>
                            <strong id="heroCampusTitle" style="font-size:0.85rem; color:#fff; display:block;">🏛️ Official Campus Building</strong>
                            <span id="heroCampusSubtitle" style="font-size:0.72rem; color:#38bdf8;">Multi-Story Academic Wing & Student Campus</span>
                        </div>
                        <span class="badge-pill badge-gold" style="font-size:0.68rem; padding:3px 8px;">16:9 HD</span>
                    </div>
                </div>"""

if hero_box_pattern.search(index_html):
    index_html = hero_box_pattern.sub(new_hero_16_9, index_html, count=1)
    print("[index.html] Replaced Hero featured photo with 16:9 box.")
elif 'class="campus-16-9-box"' in index_html:
    print("[index.html] 16:9 campus box already present.")
else:
    # Try alternative match on hero-glass-card
    alt_pattern = re.compile(r'(<div class="hero-glass-card card-3d">\s*).*?(<div class="card-header-styled")', re.DOTALL)
    index_html = alt_pattern.sub(r'\1' + new_hero_16_9 + r'\n                \2', index_html, count=1)
    print("[index.html] Inserted 16:9 campus box into hero glass card.")

# 1.2 Add "Academic PDFs" to navbar if not there
if '<li><a href="#documents">Academic PDFs</a></li>' not in index_html:
    index_html = index_html.replace(
        '<li><a href="#notices">Notices</a></li>',
        '<li><a href="#notices">Notices & Alerts</a></li>\n                <li><a href="#documents">Academic PDFs</a></li>'
    )
    print("[index.html] Added Academic PDFs link to navbar.")

# 1.3 Enhance Notices Section with Live New Notifications and Academic Documents Downloads
new_notices_section = """    <!-- Notices, Live Notifications & PDF Documents Section -->
    <section class="section section-alt" id="notices">
        <div class="container">
            <div class="section-head">
                <span class="section-tag">Announcements & Live Circulars</span>
                <h2 class="section-title">Notice Board & Official Circulars</h2>
                <p class="section-subtitle">
                    Stay updated with real-time BTEUP board circulars, examination schemes, admission notifications, and downloadable academic documents.
                </p>
            </div>

            <!-- Prominent Live New Notifications Feed -->
            <div style="margin-bottom: 25px;">
                <h3 style="font-size: 1.15rem; color:#fff; display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
                    <span style="font-size: 1.3rem;">🔔</span> Latest New Notifications & Alerts
                    <span class="live-badge" style="font-size: 0.65rem;"><span class="live-dot"></span>LIVE FEED</span>
                </h3>
                <div class="notification-feed" id="newNotificationFeed">
                    <!-- Populated dynamically via loadNotices() -->
                </div>
            </div>

            <!-- Category Filters -->
            <div class="notice-tabs" style="margin-bottom: 20px;">
                <button class="notice-tab-btn active" data-category="All">All Circulars</button>
                <button class="notice-tab-btn" data-category="New" style="color:#ef4444; font-weight:700;">🔴 Live Alerts</button>
                <button class="notice-tab-btn" data-category="Admissions">Admissions</button>
                <button class="notice-tab-btn" data-category="Examination">Examinations</button>
                <button class="notice-tab-btn" data-category="Placement">Placements</button>
                <button class="notice-tab-btn" data-category="Academic">Academic</button>
            </div>

            <!-- Dynamic Notices List from Database -->
            <div class="notices-list" id="noticesList">
                <div style="text-align:center; padding:30px; color:var(--text-muted);">
                    Loading official notices from database...
                </div>
            </div>

            <!-- Download Official Academic PDFs & Syllabus Section -->
            <div id="documents" style="margin-top: 50px; padding-top: 35px; border-top: 1px solid var(--border-glass);">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; margin-bottom:20px;">
                    <div>
                        <span class="section-tag" style="margin-bottom:6px; display:inline-block;">Downloads & Resources</span>
                        <h3 style="font-size: 1.4rem; color: #fff; margin:0; display:flex; align-items:center; gap:8px;">
                            <span>📄</span> Official Academic PDFs & Downloads
                        </h3>
                        <p style="color:var(--text-secondary); font-size:0.86rem; margin:4px 0 0 0;">
                            Official prospectus, semester syllabus, examination date-sheets, and scholarship forms verified by Secretariat.
                        </p>
                    </div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap;">
                        <button class="btn btn-sm btn-outline active" data-doc-cat="All">All Documents</button>
                        <button class="btn btn-sm btn-outline" data-doc-cat="Admissions">Prospectus</button>
                        <button class="btn btn-sm btn-outline" data-doc-cat="Examination">Exam Scheme</button>
                        <button class="btn btn-sm btn-outline" data-doc-cat="Syllabus">Syllabus</button>
                        <button class="btn btn-sm btn-outline" data-doc-cat="Fee & Guidelines">Scholarship/Fees</button>
                    </div>
                </div>

                <div class="document-grid" id="documentGrid">
                    <!-- Populated dynamically via loadDocuments() -->
                </div>
            </div>
        </div>
    </section>"""

notices_pattern = re.compile(r'<!-- Notices.*?-->\s*<section class="section section-alt" id="notices".*?</section>', re.DOTALL)
if notices_pattern.search(index_html):
    index_html = notices_pattern.sub(new_notices_section, index_html, count=1)
    print("[index.html] Replaced Notices section with Live Notifications & PDF Downloads.")
else:
    alt_notices_pattern = re.compile(r'<section class="section section-alt" id="notices".*?</section>', re.DOTALL)
    index_html = alt_notices_pattern.sub(new_notices_section, index_html, count=1)
    print("[index.html] Replaced Notices section (alt pattern).")

# 1.4 Inline CSS
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
new_style = f"<style>\n{css_content}\n</style>"
if style_pattern.search(index_html):
    index_html = style_pattern.sub(lambda m: new_style, index_html, count=1)
else:
    index_html = index_html.replace("</head>", f"{new_style}\n</head>")

# 1.5 Inline JS
body_pattern = re.compile(r'(<script>.*?</script>\s*)+</body>', re.DOTALL)
new_scripts = f"<script>\n{three_content}\n</script>\n<script>\n{app_content}\n</script>\n</body>"
if body_pattern.search(index_html):
    index_html = body_pattern.sub(lambda m: new_scripts, index_html, count=1)
else:
    index_html = index_html.replace("</body>", f"{new_scripts}")

with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
with open(os.path.join(base_dir, "static", "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print(f"[SUCCESS] index.html updated. Size: {len(index_html)} bytes")


# ==============================================================================
# 2. Update admin.html
# ==============================================================================
with open(os.path.join(base_dir, "static", "admin.html"), "r", encoding="utf-8") as f:
    admin_html = f.read()

# 2.1 Add Documents Manager to sidebar nav if not there
if 'data-tab="tabDocuments"' not in admin_html:
    admin_html = admin_html.replace(
        """            <div class="admin-nav-item" data-tab="tabGallery">
                <span>📸</span> Campus Photos Manager
            </div>""",
        """            <div class="admin-nav-item" data-tab="tabGallery">
                <span>📸</span> Campus Photos Manager
            </div>

            <div class="admin-nav-item" data-tab="tabDocuments">
                <span>📄</span> PDF Documents Manager
            </div>"""
    )
    print("[admin.html] Added tabDocuments to nav.")

# 2.2 Add 16:9 Featured Official Campus Building Photo Editor inside tabGallery
featured_building_editor = """            <!-- TAB: CAMPUS PHOTOS MANAGER -->
            <div id="tabGallery" class="admin-tab-content" style="display:none;">
                
                <!-- 16:9 Official Campus Building Photo Editor -->
                <div style="background:var(--bg-card); border:1px solid var(--border-glow); border-radius:var(--radius-lg); padding:24px; margin-bottom:26px; box-shadow:var(--shadow-card);">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
                        <div>
                            <h3 style="font-size:1.25rem; color:#fff; margin:0; display:flex; align-items:center; gap:8px;">
                                <span>🏛️</span> Official Campus Building Photo (16:9 Aspect Ratio)
                            </h3>
                            <p style="font-size:0.82rem; color:var(--text-secondary); margin:4px 0 0 0;">
                                This photo appears on the public website homepage in exact 16:9 widescreen format.
                            </p>
                        </div>
                        <span class="badge-pill badge-gold" style="font-size:0.75rem;">16:9 HD Ratio</span>
                    </div>

                    <form id="formFeaturedBuilding">
                        <div style="display:grid; grid-template-columns: 1.1fr 1fr; gap:22px; align-items:center;">
                            <div>
                                <div class="form-group" style="margin-bottom:12px;">
                                    <label class="form-label">Banner Title *</label>
                                    <input type="text" id="featBuildingTitle" class="form-input" value="🏛️ Official Campus Building" required>
                                </div>
                                <div class="form-group" style="margin-bottom:12px;">
                                    <label class="form-label">Subtitle / Description</label>
                                    <input type="text" id="featBuildingSubtitle" class="form-input" value="Multi-Story Academic Wing & Student Campus">
                                </div>
                                <div class="form-group" style="margin-bottom:14px;">
                                    <label class="form-label">Upload New Photo (Auto-crops to 16:9 HD)</label>
                                    <input type="file" id="featBuildingFileInput" class="form-input" accept="image/*">
                                    <small style="color:#94a3b8; font-size:0.75rem; display:block; margin-top:4px;">Any photo uploaded from mobile/PC is automatically cropped & scaled to 16:9 (1280x720) ratio.</small>
                                </div>
                                <button type="submit" id="btnSaveFeatBuilding" class="btn btn-primary" style="width:100%;">
                                    💾 Save Official Building Photo (16:9)
                                </button>
                            </div>

                            <!-- Live 16:9 Preview -->
                            <div>
                                <p style="font-size:0.8rem; color:#38bdf8; margin-bottom:8px; font-weight:600;">Current 16:9 Homepage Photo:</p>
                                <div class="campus-16-9-box">
                                    <img id="featBuildingCurrentImg" src="/static/assets/campus-main.jpg" alt="Featured Building">
                                </div>
                                <div id="featBuildingPreviewContainer" style="display:none; margin-top:10px;">
                                    <p style="font-size:0.75rem; color:#10b981; font-weight:600;">New 16:9 Cropped Preview:</p>
                                    <div class="campus-16-9-box">
                                        <img id="featBuildingPreviewImg" src="" alt="New Preview">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>"""

if 'id="formFeaturedBuilding"' not in admin_html:
    admin_html = admin_html.replace(
        '<!-- TAB: CAMPUS PHOTOS MANAGER -->\n            <div id="tabGallery" class="admin-tab-content" style="display:none;">',
        featured_building_editor
    )
    print("[admin.html] Added 16:9 Featured Campus Building editor.")

# 2.3 Add Documents Manager tab content if not there
documents_tab_content = """            <!-- TAB: PDF DOCUMENTS & CIRCULARS MANAGER -->
            <div id="tabDocuments" class="admin-tab-content" style="display:none;">
                <div style="display:grid; grid-template-columns: 1fr 1.6fr; gap:26px;">
                    <!-- Upload PDF Form -->
                    <div style="background:var(--bg-card); border:1px solid var(--border-glass); border-radius:var(--radius-lg); padding:26px;">
                        <h3 style="font-size:1.2rem; color:#fff; margin-bottom:12px;">Upload Academic PDF</h3>
                        <p style="font-size:0.82rem; color:var(--text-secondary); margin-bottom:18px;">
                            Upload official syllabus, prospectus, exam schemes, and forms. Students can download directly with 1 click.
                        </p>
                        <form id="addDocumentForm">
                            <div class="form-group" style="margin-bottom:14px;">
                                <label class="form-label">Document Title *</label>
                                <input type="text" id="docTitle" class="form-input" placeholder="e.g. Diploma Admission Prospectus 2026-27" required>
                            </div>
                            <div class="form-group" style="margin-bottom:14px;">
                                <label class="form-label">Category *</label>
                                <select id="docCategory" class="form-select" required>
                                    <option value="Admissions">Admissions & Prospectus</option>
                                    <option value="Examination">Examination & Datesheets</option>
                                    <option value="Syllabus">Curriculum & Syllabus</option>
                                    <option value="Fee & Guidelines">Fee Structure & Guidelines</option>
                                    <option value="General Circular">General Notice & Orders</option>
                                </select>
                            </div>
                            <div class="form-group" style="margin-bottom:14px;">
                                <label class="form-label">Description / Summary</label>
                                <textarea id="docDescription" class="form-textarea" rows="3" placeholder="Brief summary of document content, eligibility or instructions..."></textarea>
                            </div>
                            <div class="form-group" style="margin-bottom:16px;">
                                <label class="form-label">Select PDF File (.pdf) *</label>
                                <input type="file" id="docFileInput" class="form-input" accept=".pdf,application/pdf" required>
                                <div id="docFileInfo" style="display:none; margin-top:6px; font-size:0.8rem; color:#38bdf8;"></div>
                            </div>
                            <button type="submit" id="btnUploadDoc" class="btn btn-primary" style="width:100%;">
                                🚀 Upload & Publish PDF Document
                            </button>
                        </form>
                    </div>

                    <!-- Document List Table -->
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                            <h3 style="font-size:1.2rem; color:#fff; margin:0;">Published PDF Documents</h3>
                            <button class="btn btn-sm btn-outline" onclick="loadDocumentsAdmin()">🔄 Refresh List</button>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Document Title</th>
                                        <th>Category</th>
                                        <th>Size</th>
                                        <th>Uploaded</th>
                                        <th>Downloads</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="adminDocTbody">
                                    <!-- Populated dynamically via loadDocumentsAdmin() -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>"""

if 'id="tabDocuments"' not in admin_html:
    admin_html = admin_html.replace(
        "<!-- TAB 6: PUBLIC ENQUIRIES -->",
        f"{documents_tab_content}\n\n            <!-- TAB 6: PUBLIC ENQUIRIES -->"
    )
    print("[admin.html] Added tabDocuments content.")

# 2.4 Add PDF attachment & urgent checkbox in publishNoticeForm
if 'id="newNoticePdf"' not in admin_html:
    admin_html = admin_html.replace(
        '<input type="checkbox" id="newNoticeUrgent" style="width:18px; height:18px;">',
        """<div class="form-group" style="margin-bottom:12px;">
                                    <label class="form-label">Attach PDF Document (Optional)</label>
                                    <input type="file" id="newNoticePdf" class="form-input" accept=".pdf,application/pdf">
                                    <small style="color:#94a3b8; font-size:0.75rem;">Students can download this PDF directly from the notice board.</small>
                                </div>
                                <input type="checkbox" id="newNoticeUrgent" style="width:18px; height:18px;">"""
    )
    print("[admin.html] Added PDF attachment option to notice form.")

# 2.5 Inline CSS in admin
if style_pattern.search(admin_html):
    admin_html = style_pattern.sub(lambda m: new_style, admin_html, count=1)
else:
    admin_html = admin_html.replace("</head>", f"{new_style}\n</head>")

# 2.6 Inline JS in admin
admin_scripts = f"<script>\n{admin_js_content}\n</script>\n</body>"
if body_pattern.search(admin_html):
    admin_html = body_pattern.sub(lambda m: admin_scripts, admin_html, count=1)
else:
    admin_html = admin_html.replace("</body>", f"{admin_scripts}")

with open(os.path.join(base_dir, "admin.html"), "w", encoding="utf-8") as f:
    f.write(admin_html)
with open(os.path.join(base_dir, "static", "admin.html"), "w", encoding="utf-8") as f:
    f.write(admin_html)
print(f"[SUCCESS] admin.html updated. Size: {len(admin_html)} bytes")
