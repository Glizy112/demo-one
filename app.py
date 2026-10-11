# from flask import Flask, request, render_template_string, jsonify
# import secrets

# app = Flask(__name__)

# # State Storage
# LEADERBOARD = {"Prof_Matrix": 12, "Prof_Cipher": 18, "Prof_Rogue": 5}
# REVOKED_TOKENS = set()
# WAF_ENABLED = False

# HTML_ARENA = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Live Security Arena - College Workshop</title>
#     <style>
#         body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 30px; }
#         .container { max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
#         .card { background: #1e293b; padding: 24px; border-radius: 12px; border: 1px solid #334155; }
#         h2 { color: #38bdf8; margin-top: 0; }
#         .score-box { background: #020617; padding: 12px; margin: 10px 0; border-radius: 6px; font-size: 18px; font-weight: bold; display: flex; justify-content: space-between; }
#         .btn { width: 100%; padding: 12px; background: #0284c7; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 10px; }
#         .btn-danger { background: #dc2626; }
#         .badge { background: #e11d48; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
#     </style>
# </head>
# <body>
#     <div style="text-align: center; margin-bottom: 20px;">
#         <h1>🏆 University Teacher of the Year - LIVE VOTING</h1>
#         <p>Scan QR / Visit Target Endpoint & Submit Your Vote!</p>
#     </div>

#     <div class="container">
#         <!-- PUBLIC LEADERBOARD -->
#         <div class="card">
#             <h2>Live Leaderboard</h2>
#             <div id="scores">
#                 {% for prof, votes in leaderboard.items() %}
#                     <div class="score-box"><span>{{ prof }}</span><span style="color:#4ade80;">{{ votes }} Votes</span></div>
#                 {% endfor %}
#             </div>
#             <hr style="border-color:#334155; margin: 20px 0;">
#             <h3>Cast Vote (Normal Interface)</h3>
#             <form action="/vote" method="POST">
#                 <input type="hidden" name="candidate" value="Prof_Rogue">
#                 <input type="hidden" name="count" value="1">
#                 <button type="submit" class="btn">Vote for Prof_Rogue (+1)</button>
#             </form>
#         </div>

#         <!-- ADMIN STAGE CONTROL BOARD -->
#         <div class="card">
#             <h2>Stage Controls (Speaker Only)</h2>
#             <p>WAF Protection: <span class="badge" id="waf-status">{{ "ENABLED" if waf else "DISABLED" }}</span></p>
#             <button class="btn btn-danger" onclick="toggleWAF()">Toggle WAF Defense Layer</button>
#             <button class="btn" onclick="resetBoard()" style="background:#475569;">Reset Leaderboard</button>
#             <h3 style="margin-top:20px;">HTTP POST Payload Reference:</h3>
#             <pre style="background:#020617; padding:10px; color:#38bdf8; font-size:12px;">
# POST /vote
# Content-Type: application/x-www-form-urlencoded

# candidate=Prof_Rogue&count=1
#             </pre>
#         </div>
#     </div>

#     <script>
#         async function toggleWAF() {
#             let res = await fetch('/admin/toggle-waf', { method: 'POST' });
#             let data = await res.json();
#             location.reload();
#         }
#         async function resetBoard() {
#             await fetch('/admin/reset', { method: 'POST' });
#             location.reload();
#         }
#         // Auto refresh leaderboard every 2 seconds
#         setInterval(() => {
#             fetch('/api/scores').then(r => r.json()).then(data => {
#                 let html = '';
#                 for (let [prof, votes] of Object.entries(data)) {
#                     html += `<div class="score-box"><span>${prof}</span><span style="color:#4ade80;">${votes} Votes</span></div>`;
#                 }
#                 document.getElementById('scores').innerHTML = html;
#             });
#         }, 2000);
#     </script>
# </body>
# </html>
# """

# @app.route('/')
# def index():
#     return render_template_string(HTML_ARENA, leaderboard=LEADERBOARD, waf=WAF_ENABLED)

# @app.route('/api/scores')
# def get_scores():
#     return jsonify(LEADERBOARD)

# @app.route('/vote', methods=['POST'])
# def vote():
#     global WAF_ENABLED
#     candidate = request.form.get('candidate', 'Prof_Rogue')
    
#     # PARAMETER TAMPERING VULNERABILITY: Accepts user-supplied count!
#     try:
#         count = int(request.form.get('count', 1))
#     except ValueError:
#         count = 1

#     # WAF DEFENSE LAYER
#     if WAF_ENABLED and count > 10:
#         return """<h1 style="color:red; font-family:sans-serif;">🚨 403 FORBIDDEN: WAF Parameter Anomaly Detected (count > 10 blocked)</h1>""", 403

#     if candidate in LEADERBOARD:
#         LEADERBOARD[candidate] += count
#         return f"VOTE ACCEPTED: Added {count} votes to {candidate}!", 200
    
#     return "Invalid Candidate", 400

# @app.route('/admin/toggle-waf', methods=['POST'])
# def toggle_waf():
#     global WAF_ENABLED
#     WAF_ENABLED = not WAF_ENABLED
#     return jsonify({"waf": WAF_ENABLED})

# @app.route('/admin/reset', methods=['POST'])
# def reset():
#     global LEADERBOARD
#     LEADERBOARD = {"Prof_Matrix": 12, "Prof_Cipher": 18, "Prof_Rogue": 5}
#     return jsonify({"status": "reset"})

# if __name__ == '__main__':
#     print("[*] Launching Arena Server on http://0.0.0.0:5000")
#     app.run(host='0.0.0.0', port=5000, debug=True)




from flask import Flask, request, render_template_string, jsonify, make_response
import secrets

app = Flask(__name__)

# Simulated Database Records
STUDENT_DB = {
    f"STU-100{i}": {
        "id": f"STU-100{i}",
        "name": f"Student_{i}",
        "email": f"student_{i}@university.edu",
        "gpa": round(2.5 + (i * 0.15) % 1.5, 2),
        "medical_notes": f"Confidential Record #{i}: Cleared for athletics. Allergy: Item_{i}",
        "ssn_last4": f"{1000 + i*37}"
    } for i in range(1, 21)
}

# Live Telemetry Tracking for Audience Activity
EXFILTRATED_RECORDS = set()
WAF_AUTHORIZATION_PATCH = False

HTML_PORTAL = """
<!DOCTYPE html>
<html>
<head>
    <title>University Health & Academic API Portal</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 25px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 1100px; margin: 0 auto; }
        .card { background: #1e293b; padding: 24px; border-radius: 12px; border: 1px solid #334155; }
        h1, h2, h3 { color: #38bdf8; margin-top: 0; }
        .btn { width: 100%; padding: 12px; background: #0284c7; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .btn-danger { background: #dc2626; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .bg-red { background: #9f1239; color: #fecdd3; }
        .bg-green { background: #14532d; color: #bbf7d0; }
        pre { background: #020617; padding: 12px; border-radius: 6px; color: #4ade80; font-size: 13px; overflow-x: auto; }
        .record-box { background: #020617; padding: 10px; margin-bottom: 8px; border-radius: 6px; border-left: 4px solid #38bdf8; font-size: 13px; }
    </style>
</head>
<body>
    <div style="text-align: center; margin-bottom: 25px;">
        <h1>🏥 Student Medical & Academic Records Portal</h1>
        <p style="color: #94a3b8;">Real-World REST API Security Demonstration</p>
    </div>

    <div class="grid">
        <!-- AUDIENCE / RED TEAM PORTAL -->
        <div class="card">
            <h2>📱 Your Assigned Record Card</h2>
            <p>Logged in as: <strong>STU-1001 (student_1@university.edu)</strong></p>
            <p style="color: #94a3b8; font-size: 13px;">API Endpoint invoked by frontend JavaScript:</p>
            <pre>GET /api/v1/records/STU-1001</pre>
            <button class="btn" onclick="fetchMyRecord()">Fetch My Record via REST API</button>
            
            <h3 style="margin-top: 20px;">Returned JSON Data:</h3>
            <pre id="api-output">Click button to fetch API response...</pre>

            <hr style="border-color: #334155; margin: 20px 0;">
            <p style="color:#f43f5e; font-size: 13px;"><strong>Audience Challenge:</strong> Modify the URL path in your browser or Burp Suite to request <code>/api/v1/records/STU-1002</code> through <code>STU-1020</code>.</p>
        </div>

        <!-- STAGE TELEMETRY & BLUE TEAM CONTROL -->
        <div class="card">
            <h2>🛡️ Stage SOC Monitor & Defense Board</h2>
            <p>Authorization Enforcement: 
                <span class="badge {{ 'bg-green' if patch else 'bg-red' }}" id="auth-status">
                    {{ 'ENFORCED (Session Bound)' if patch else 'DISABLED (Vulnerable IDOR)' }}
                </span>
            </p>
            <button class="btn btn-danger" onclick="togglePatch()">Toggle API Authorization Middleware</button>
            <button class="btn" onclick="clearLeaks()" style="background:#475569; margin-top:8px;">Clear Exfiltration Log</button>

            <h3 style="margin-top: 20px;">Live Data Leak Exfiltration Meter (<span id="leak-count">0</span> / 20 Records Exposed):</h3>
            <div id="leak-log" style="max-height: 250px; overflow-y: auto;">
                <p style="color: #94a3b8; font-size: 13px;">Awaiting audience API calls...</p>
            </div>
        </div>
    </div>

    <script>
        async function fetchMyRecord() {
            let res = await fetch('/api/v1/records/STU-1001');
            let data = await res.json();
            document.getElementById('api-output').innerText = JSON.stringify(data, null, 2);
        }

        async function togglePatch() {
            await fetch('/admin/toggle-patch', { method: 'POST' });
            location.reload();
        }

        async function clearLeaks() {
            await fetch('/admin/clear-log', { method: 'POST' });
            location.reload();
        }

        // Auto-refresh SOC telemetry on stage every 2 seconds
        setInterval(async () => {
            let res = await fetch('/api/telemetry');
            let data = await res.json();
            document.getElementById('leak-count').innerText = data.count;
            
            let html = '';
            data.leaked_records.forEach(id => {
                html += `<div class="record-box">🚨 <strong>UNAUTHORIZED ACCESS:</strong> ${id} record exposed to cross-user request!</div>`;
            });
            if(data.leaked_records.length > 0) {
                document.getElementById('leak-log').innerHTML = html;
            }
        }, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    resp = make_response(render_template_string(HTML_PORTAL, patch=WAF_AUTHORIZATION_PATCH))
    # Assign authenticating session cookie for STU-1001
    resp.set_cookie('auth_session', 'SESS_USER_STU_1001', httponly=True)
    return resp

@app.route('/api/v1/records/<student_id>')
def get_student_record(student_id):
    global WAF_AUTHORIZATION_PATCH
    
    # Extract authenticating session identity
    session_cookie = request.cookies.get('auth_session', '')
    authenticated_user = "STU-1001" if "STU_1001" in session_cookie else "ANONYMOUS"

    # --- DEFENSE LAYER: BROKEN OBJECT LEVEL AUTHORIZATION (BOLA) FIX ---
    if WAF_AUTHORIZATION_PATCH:
        # Check if requested object owner matches authenticated session user
        if student_id != authenticated_user:
            return jsonify({
                "error": "HTTP 403 FORBIDDEN",
                "message": f"Access Denied: Session user {authenticated_user} is not authorized to view record {student_id}"
            }), 403

    # VULNERABLE LOGIC: Fetches record purely based on path parameter
    if student_id in STUDENT_DB:
        # Log leak telemetry if a user accesses a record other than their own
        if student_id != authenticated_user:
            EXFILTRATED_RECORDS.add(student_id)

        return jsonify(STUDENT_DB[student_id]), 200

    return jsonify({"error": "Record Not Found"}), 404

@app.route('/api/telemetry')
def get_telemetry():
    return jsonify({
        "count": len(EXFILTRATED_RECORDS),
        "leaked_records": list(EXFILTRATED_RECORDS)
    })

@app.route('/admin/toggle-patch', methods=['POST'])
def toggle_patch():
    global WAF_AUTHORIZATION_PATCH
    WAF_AUTHORIZATION_PATCH = not WAF_AUTHORIZATION_PATCH
    return jsonify({"patched": WAF_AUTHORIZATION_PATCH})

@app.route('/admin/clear-log', methods=['POST'])
def clear_log():
    global EXFILTRATED_RECORDS
    EXFILTRATED_RECORDS = set()
    return jsonify({"status": "cleared"})

if __name__ == '__main__':
    print("[*] Launching IDOR API Portal on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)