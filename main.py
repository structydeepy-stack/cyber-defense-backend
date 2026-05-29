from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="DEFENSE OPERATIONS CENTER v2.3")

logs = []

def add_log(message: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    logs.append(entry)
    print(entry)

@app.get("/", response_class=HTMLResponse)
async def defense_dashboard():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DEFENSE OPERATIONS CENTER v2.3</title>
    <style>
        :root { --neon-red: #ff0044; --neon-cyan: #00ffff; --neon-green: #00ff88; }
        body { background:#0a0005; color:#ddd; font-family:'Courier New',monospace; }
        .scanline { position:fixed; top:0; left:0; width:100%; height:100%; background:linear-gradient(transparent 50%, rgba(0,255,70,0.04) 50%); background-size:100% 4px; animation:scan 4s linear infinite; pointer-events:none; z-index:1; }
        @keyframes scan { 0%{transform:translateY(-100%);} 100%{transform:translateY(100%);} }
        .glitch { color:var(--neon-red); animation:glitch-skew 4s infinite linear alternate-reverse; }
        .container { max-width:1100px; margin:0 auto; padding:20px; position:relative; z-index:2; }
        .log { background:#050000; border:2px solid var(--neon-red); padding:20px; height:58vh; overflow-y:auto; white-space:pre-wrap; box-shadow:0 0 25px var(--neon-red); }
        button { background:transparent; border:3px solid var(--neon-green); color:var(--neon-green); padding:15px 30px; margin:10px; cursor:pointer; transition:all 0.3s; }
        button:hover { background:var(--neon-green); color:#000; box-shadow:0 0 30px var(--neon-green); }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <h1 class="glitch neon-red" data-text="DEFENSE OPERATIONS CENTER">DEFENSE OPERATIONS CENTER v2.3</h1>
        <div class="log" id="log"></div>
        
        <button onclick="simulateAdvancedAttack()">🛡️ SIMULATE ADVANCED ATTACK</button>
        <button onclick="clearLogs()" style="border-color:#ff8800;color:#ff8800;">CLEAR LOGS</button>
    </div>

    <script>
        async function fetchLogs() { 
            const res = await fetch('/logs'); 
            document.getElementById('log').textContent = await res.text();
            document.getElementById('log').scrollTop = 999999;
        }
        setInterval(fetchLogs, 600);
        fetchLogs();

        async function simulateAdvancedAttack() {
            await fetch('/trigger', { 
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({event: "advanced_persistence_injection"})
            });
            alert("🛡️ Advanced Red Team Attack Simulated!");
        }
        
        async function clearLogs() {
            await fetch('/clear', {method: 'POST'});
        }
    </script>
</body>
</html>"""

@app.get("/logs")
async def get_logs():
    return "\n".join(logs[-200:])

@app.post("/trigger")
async def trigger_from_attacker(request: Request):
    data = await request.json()
    event = data.get("event", "unknown")

    if "injection" in event.lower():
        add_log("🚨 PROCESS INJECTION DETECTED (CreateRemoteThread)", "CRITICAL")
        add_log("EDR Alert: Suspicious memory allocation in target process", "ALERT")
    elif "persistence" in event.lower() or "advanced" in event.lower():
        add_log("🚨 PERSISTENCE MECHANISM DETECTED!", "CRITICAL")
        add_log("Self-copy to hidden location observed", "WARNING")
        add_log("Registry / systemd / cron modification detected", "WARNING")
        add_log("Multiple persistence layers installed", "ALERT")
    else:
        add_log(f"🚨 C2 ACTIVITY DETECTED: {event}", "CRITICAL")

    add_log("🛡️ Containment initiated — Killing suspicious processes", "SUCCESS")
    add_log("Network outbound blocked to C2", "SUCCESS")
    add_log("Forensic snapshot saved for analysis", "INFO")
    add_log("THREAT LEVEL: HIGH", "CRITICAL")

    return {"status": "contained"}

@app.post("/clear")
async def clear_logs():
    global logs
    logs.clear()
    add_log("Logs cleared by SOC Analyst", "INFO")
    return {"status": "cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
