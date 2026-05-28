from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import asyncio

app = FastAPI(title="STRUCTY_DEEPY DEFENSE CORE v2.1")

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
    <title>DEFENSE OPERATIONS CENTER</title>
    <style>
        :root {
            --neon-red: #ff0044;
            --neon-cyan: #00ffff;
            --neon-green: #00ff88;
            --blood: #8b0000;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #0a0005;
            color: #ddd;
            font-family: 'Courier New', monospace;
        }
        .scanline {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(transparent 50%, rgba(0,255,70,0.04) 50%);
            background-size: 100% 4px;
            pointer-events: none;
            animation: scan 4s linear infinite;
            z-index: 1;
            opacity: 0.7;
        }
        @keyframes scan { 0%{transform:translateY(-100%);} 100%{transform:translateY(100%);} }
        
        .glitch {
            position: relative;
            color: var(--neon-red);
            animation: glitch-skew 4s infinite linear alternate-reverse;
        }
        .neon-red { color: var(--neon-red); text-shadow: 0 0 15px var(--neon-red); }
        .neon-cyan { color: var(--neon-cyan); text-shadow: 0 0 15px var(--neon-cyan); }
        .neon-green { color: var(--neon-green); text-shadow: 0 0 15px var(--neon-green); }
        
        .container { max-width: 1100px; margin: 0 auto; padding: 20px; position: relative; z-index: 2; }
        .log {
            background: #050000;
            border: 2px solid var(--neon-red);
            padding: 20px;
            height: 58vh;
            overflow-y: auto;
            white-space: pre-wrap;
            box-shadow: 0 0 25px var(--neon-red);
            font-size: 1.05rem;
        }
        button {
            background: transparent;
            border: 3px solid var(--neon-green);
            color: var(--neon-green);
            padding: 15px 30px;
            font-size: 1.2rem;
            margin: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        button:hover {
            background: var(--neon-green);
            color: #000;
            box-shadow: 0 0 30px var(--neon-green);
        }
        .warning-banner {
            background: linear-gradient(90deg, #ff0000, #ff8800);
            color: #000;
            padding: 12px;
            font-weight: bold;
            margin: 15px 0;
            animation: glitch 1s infinite;
        }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <header>
            <h1 class="glitch neon-red" data-text="DEFENSE OPERATIONS CENTER">DEFENSE OPERATIONS CENTER</h1>
            <div class="warning-banner">THREAT LEVEL: CRITICAL — MONITORING FOR PYNCAT PERSISTENCE</div>
        </header>
        
        <div class="log" id="log"></div>
        
        <button onclick="simulateAttack()">🛡️ SIMULATE PYNCAT ATTACK</button>
        <button onclick="clearLogs()" style="border-color:#ff8800;color:#ff8800;">CLEAR LOGS</button>
    </div>

    <script>
        async function fetchLogs() {
            const res = await fetch('/logs');
            const text = await res.text();
            document.getElementById('log').textContent = text;
            document.getElementById('log').scrollTop = 999999;
        }
        setInterval(fetchLogs, 700);
        fetchLogs();

        async function simulateAttack() {
            await fetch('/attack', { method: 'POST' });
            alert("🚨 Simulated PyNcat Attack Triggered!");
        }
        
        async function clearLogs() {
            await fetch('/clear', { method: 'POST' });
        }
    </script>
</body>
</html>"""

@app.get("/logs")
async def get_logs():
    return "\n".join(logs[-150:])

@app.post("/attack")
async def register_attack():
    add_log("🚨 INCOMING CONNECTION DETECTED — Possible PyNcat Reverse Shell", "CRITICAL")
    add_log("SSL Handshake from external IP", "ALERT")
    add_log("Self-signed certificate detected (/tmp/pyncat_cert.pem)", "WARNING")
    add_log("Persistent reconnection behavior observed (exponential backoff)", "WARNING")
    add_log("🛡️ EDR Rule Triggered — Blocking outbound C2 traffic", "SUCCESS")
    add_log("Process python3 quarantined", "SUCCESS")
    add_log("Containment successful. Threat neutralized.", "neon-green")
    return {"status": "attack_detected_and_blocked"}

@app.post("/clear")
async def clear_logs():
    global logs
    logs.clear()
    add_log("Logs cleared by operator", "INFO")
    return {"status": "cleared"}

@app.get("/status")
async def get_status():
    return {"status": "active"}  # You can make this smarter later

@app.post("/trigger")
async def trigger_from_attacker(request: Request):
    data = await request.json()
    event = data.get("event", "unknown")
    
    add_log(f"🚨 EXTERNAL TRIGGER from Attacker C2: {event}", "CRITICAL")
    add_log("SSL Connection + Persistent Behavior Detected", "ALERT")
    add_log("Self-signed cert in /tmp flagged", "WARNING")
    add_log("🛡️ Containment Activated — Blocking C2 Channel", "SUCCESS")
    return {"status": "alert_processed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
