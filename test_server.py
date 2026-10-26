"""
Test runner to verify all endpoints and database operations
"""
import urllib.request
import json
import time
import subprocess
import sys

def test_endpoints():
    base = "http://localhost:8080"
    
    # Test 1: Home page
    print("Testing GET / ...")
    req = urllib.request.urlopen(f"{base}/")
    assert req.status == 200
    html = req.read().decode("utf-8")
    assert "Govt. Polytechnic Mahasi" in html
    assert "Subodh Mishra" in html
    assert "Rajan Singh" in html
    print("✓ GET / passed")

    # Test 2: Admin page
    print("Testing GET /admin ...")
    req = urllib.request.urlopen(f"{base}/admin")
    assert req.status == 200
    admin_html = req.read().decode("utf-8")
    assert "Secretariat" in admin_html
    print("✓ GET /admin passed")

    # Test 3: API Stats
    print("Testing GET /api/stats ...")
    req = urllib.request.urlopen(f"{base}/api/stats")
    assert req.status == 200
    stats = json.loads(req.read().decode("utf-8"))
    assert stats["success"] is True
    print(f"✓ Stats returned: {stats['stats']['total_students']} students, {stats['stats']['total_applications']} apps")

    # Test 4: API Notices
    print("Testing GET /api/notices ...")
    req = urllib.request.urlopen(f"{base}/api/notices")
    assert req.status == 200
    notices = json.loads(req.read().decode("utf-8"))
    assert notices["success"] is True
    assert len(notices["notices"]) > 0
    print(f"✓ Loaded {len(notices['notices'])} notices successfully")

    # Test 5: API Login
    print("Testing POST /api/auth/login ...")
    login_data = json.dumps({"username": "admin", "password": "admin123"}).encode("utf-8")
    req = urllib.request.Request(f"{base}/api/auth/login", data=login_data, headers={"Content-Type": "application/json"}, method="POST")
    res = urllib.request.urlopen(req)
    assert res.status == 200
    login_res = json.loads(res.read().decode("utf-8"))
    assert login_res["success"] is True
    token = login_res["token"]
    print(f"✓ Login successful! Token: {token[:10]}...")

    # Test 6: Submit new student application
    print("Testing POST /api/applications ...")
    app_data = json.dumps({
        "full_name": "Deepak Verma",
        "father_name": "R. P. Verma",
        "dob": "2007-04-10",
        "gender": "Male",
        "category": "OBC",
        "email": "deepak.verma@test.com",
        "phone": "9876543299",
        "address": "Mahasi Chauraha",
        "district": "Bahraich",
        "pincode": "271824",
        "branch": "Computer Science & Engineering",
        "high_school_board": "UP Board",
        "high_school_percent": 86.4,
        "jeecup_roll_no": "2609999",
        "jeecup_rank": 2400
    }).encode("utf-8")
    req = urllib.request.Request(f"{base}/api/applications", data=app_data, headers={"Content-Type": "application/json"}, method="POST")
    res = urllib.request.urlopen(req)
    assert res.status == 201
    app_res = json.loads(res.read().decode("utf-8"))
    assert app_res["success"] is True
    new_app_no = app_res["app_no"]
    print(f"✓ Application submitted successfully with ID: {new_app_no}")

    # Test 7: Track application
    print(f"Testing GET /api/applications/track?app_no={new_app_no} ...")
    req = urllib.request.urlopen(f"{base}/api/applications/track?app_no={new_app_no}")
    assert req.status == 200
    track_res = json.loads(req.read().decode("utf-8"))
    assert track_res["success"] is True
    assert track_res["application"]["full_name"] == "Deepak Verma"
    print(f"✓ Tracker verified application status: {track_res['application']['status']}")

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! 100% OPERATIONAL.")

if __name__ == "__main__":
    test_endpoints()
