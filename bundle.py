import os

base = r"C:\Users\Avinash Kumar\.gemini\antigravity\scratch\govt-polytechnic-mahasi"

css_path = os.path.join(base, "static", "css", "styles.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

three_path = os.path.join(base, "static", "js", "three_engine.js")
with open(three_path, "r", encoding="utf-8") as f:
    three_content = f.read()

app_path = os.path.join(base, "static", "js", "app.js")
with open(app_path, "r", encoding="utf-8") as f:
    app_content = f.read()

admin_js_path = os.path.join(base, "static", "js", "admin.js")
with open(admin_js_path, "r", encoding="utf-8") as f:
    admin_js_content = f.read()

# Process index.html
with open(os.path.join(base, "static", "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

# Inline CSS
style_block = f"<style>\n{css_content}\n</style>"
if '<link rel="stylesheet" href="/static/css/styles.css">' in html:
    html = html.replace('<link rel="stylesheet" href="/static/css/styles.css">', style_block)
else:
    html = html.replace("</head>", f"{style_block}\n</head>")

# Inline JS
script_block = f"<script>\n{three_content}\n</script>\n<script>\n{app_content}\n</script>"
if '<script src="/static/js/three_engine.js"></script>' in html:
    # remove the two script tags
    html = html.replace('<script src="/static/js/three_engine.js"></script>', "")
    html = html.replace('<script src="/static/js/app.js"></script>', "")
html = html.replace("</body>", f"{script_block}\n</body>")

with open(os.path.join(base, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
with open(os.path.join(base, "static", "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Bundled index.html written. New size: {len(html)} bytes")

# Process admin.html
with open(os.path.join(base, "static", "admin.html"), "r", encoding="utf-8") as f:
    admin_html = f.read()

if '<link rel="stylesheet" href="/static/css/styles.css">' in admin_html:
    admin_html = admin_html.replace('<link rel="stylesheet" href="/static/css/styles.css">', style_block)
else:
    admin_html = admin_html.replace("</head>", f"{style_block}\n</head>")

admin_script_block = f"<script>\n{admin_js_content}\n</script>"
if '<script src="/static/js/admin.js"></script>' in admin_html:
    admin_html = admin_html.replace('<script src="/static/js/admin.js"></script>', "")
admin_html = admin_html.replace("</body>", f"{admin_script_block}\n</body>")

with open(os.path.join(base, "admin.html"), "w", encoding="utf-8") as f:
    f.write(admin_html)
with open(os.path.join(base, "static", "admin.html"), "w", encoding="utf-8") as f:
    f.write(admin_html)
print(f"Bundled admin.html written. New size: {len(admin_html)} bytes")
