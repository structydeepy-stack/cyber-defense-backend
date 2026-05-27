from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime

app = FastAPI(title="STRUCTY_DEEPY DEFENSE CORE v0.8.7")

logs = []

def add_log(message: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    logs.append(entry)
    print(entry)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """<!DOCTYPE html>
<html>
<head><title>DEFENSE CORE</title>
<style>
body{background:#0a0005;color:#00ff88;font-family:Courier New;padding:20px;margin:0;}
h1{color:#ff0044;text-shadow:0 0 15px #ff0044;}
.log{background:#050000;border:1px solid #440000;padding:15px;height:70vh;overflow-y:auto;white-space:pre-wrap;}
.alert{color:#ff0044;animation:flash 1.5s infinite;}
@keyframes flash{50%{opacity:0.4;}}
</style>
</head>
<body>
<h1>🛡️ DEFENSE OPERATIONS CENTER — LIVE</h1>
<div class="log" id="log"></div>
<script>
async function fetchLogs(){ 
  const res = await fetch('/logs'); 
  const text = await res.text();
  document.getElementById('log').textContent = text;
  document.getElementById('log').scrollTop = 999999;
}
setInterval(fetchLogs, 1000); fetchLogs();
</script>
</body>
</html>"""

@app.get("/logs")
async def get_logs():
    return "\n".join(logs[-100:])

@app.post("/attack")
async def register_attack(request: Request):
    data = await request.json()
    add_log(f"🚨 PyNcat ATTACK from {request.client.host}", "CRITICAL")
    add_log(f"Persistent: {data.get('persistent', False)} | SSL: {data.get('ssl', False)}", "ALERT")
    add_log("Self-signed cert detected in /tmp", "WARNING")
    add_log("✅ REVERSE SHELL BLOCKED by EDR", "SUCCESS")
    return {"status": "contained"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
